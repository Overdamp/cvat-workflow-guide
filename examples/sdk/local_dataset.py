"""SDK hands-on: create an isolated two-image task, then read saved annotations."""
import argparse
import ast
import getpass
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from cvat_sdk import make_client
from cvat_sdk.core.proxies.tasks import ResourceType

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = Path('/home/luke/ai_training/codex_ptt_inspection/datasets/overall-ptt-object-detection.v11i.yolov11')


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['create', 'read', 'complete'])
    parser.add_argument('--run', type=Path, help='Existing run folder printed by create')
    parser.add_argument('--dataset', type=Path, default=DEFAULT_DATASET)
    parser.add_argument('--url', default=os.getenv('CVAT_BASE_URL', 'http://localhost:8080'))
    parser.add_argument('--org', default=os.getenv('CVAT_ORG', 'ptt-demo'))
    args = parser.parse_args()
    if args.action != 'create' and args.run is None:
        parser.error('read/complete requires --run')
    token = os.getenv('CVAT_ACCESS_TOKEN') or getpass.getpass('CVAT PAT (hidden): ')
    with make_client(args.url, access_token=token) as client:
        client.organization_slug = args.org
        if args.action == 'create':
            images = sorted(p for p in (args.dataset / 'train/images').iterdir()
                            if p.suffix.lower() in {'.jpg', '.jpeg', '.png'})[:2]
            if len(images) != 2:
                raise ValueError('Need two images')
            # This dataset uses a one-line Python-compatible names list.
            line = next(x for x in (args.dataset / 'data.yaml').read_text().splitlines()
                        if x.startswith('names:'))
            names = ast.literal_eval(line.split(':', 1)[1].strip())
            if not isinstance(names, list) or not all(isinstance(x, str) for x in names):
                raise ValueError('Unexpected class names format')
            run = ROOT / 'artifacts' / ('sdk-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
            run.mkdir(parents=True, exist_ok=False)
            state = {'url': args.url, 'org': args.org, 'images': [str(p) for p in images]}
            save(run / 'state.json', state)
            print('Run folder:', run, flush=True)
            project = client.projects.create({'name': run.name, 'labels': [
                {'name': name, 'type': 'rectangle'} for name in names]})
            state['project_id'] = project.id
            save(run / 'state.json', state)
            task = client.tasks.create({'name': 'sdk-two-images', 'project_id': project.id, 'segment_size': 20})
            state['task_id'] = task.id
            save(run / 'state.json', state)
            # Save IDs before upload so failed uploads do not lose resource references.
            task.upload_data(resources=images, resource_type=ResourceType.LOCAL,
                             params={'image_quality': 85}, wait_for_completion=True)
            jobs = [job for job in task.get_jobs() if job.type == 'annotation']
            if len(jobs) != 1:
                raise ValueError('Expected one annotation job; inspect the new task')
            job = jobs[0]
            state['job_id'] = job.id
            save(run / 'state.json', state)
            job.update({'stage': 'annotation', 'state': 'in progress'})
            print(f'Open: {args.url}/tasks/{task.id}/jobs/{job.id}')
            print('Draw rectangles and Save in CVAT, then run read --run', run)
        else:
            run = args.run.resolve()
            state = json.loads((run / 'state.json').read_text())
            if state['url'].rstrip('/') != args.url.rstrip('/') or state['org'] != args.org:
                raise ValueError('URL/org must match the original run')
            task = client.tasks.retrieve(state['task_id'])
            job = client.jobs.retrieve(state['job_id'])
            if job.task_id != task.id:
                raise ValueError('Job/task mismatch')
            if args.action == 'complete':
                answer = input(f'Saved in CVAT? Set Job {job.id} annotation/completed? Type yes: ')
                if answer != 'yes':
                    print('Cancelled')
                    return
                job.update({'stage': 'annotation', 'state': 'completed'})
                print('Job:', job.id, 'stage:', job.stage, 'state:', job.state)
                return
            annotations = job.get_annotations().to_dict()
            meta = task.get_meta().to_dict()
            labels = [label.to_dict() for label in task.get_labels()]
            save(run / 'annotations.json', annotations)
            save(run / 'media-meta.json', meta)
            save(run / 'labels.json', labels)
            if meta['start_frame'] != 0 or meta.get('frame_filter') or len(meta['frames']) != 2:
                raise ValueError('Mapping supports only this two-image task without frame filter')
            names = {label['id']: label['name'] for label in labels}
            rows = []
            for shape in annotations['shapes']:
                frame = shape['frame']
                if frame < 0 or frame >= len(meta['frames']):
                    raise ValueError('Frame outside metadata')
                image = meta['frames'][frame]
                rows.append({'shape_id': shape['id'], 'frame': frame, 'image_name': image['name'],
                             'label': names[shape['label_id']], 'type': shape['type'],
                             'points': shape['points'], 'rotation': shape.get('rotation', 0)})
            save(run / 'mapped-shapes.json', rows)
            print(json.dumps(rows, ensure_ascii=False, indent=2))
            print('Counts:', {key: len(annotations[key]) for key in ['shapes', 'tags', 'tracks']})
            print('Output:', run)


if __name__ == '__main__':
    main()
