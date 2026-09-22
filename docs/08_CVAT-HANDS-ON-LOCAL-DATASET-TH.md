# ทดลอง CVAT API ทีละขั้นด้วยภาพจาก dataset ในเครื่อง

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

จัดทำ 22 กันยายน 2026 สำหรับเครื่อง luke ใช้ Bash Terminal เดียวตลอดขั้นตอน

> **เอกสารทดลองเท่านั้น:** คู่มือนี้ upload ภาพจาก path local เข้า CVAT เพื่อพิสูจน์ REST API ไม่ใช่รูปแบบ ingestion หลักของ production และไม่ควรนำ artifacts ใน `RUN_DIR` ไปเก็บเป็นฐานข้อมูลถาวร

สร้าง Project ใหม่และใช้ภาพ 2 รูปจาก dataset เดิม ไม่แก้ไฟล์ต้นฉบับ ไม่มีการเปลี่ยนสิทธิ์บัญชีหรือแยก QA ใช้ admin2 หรือบัญชีที่มีสิทธิ์สร้างงานใน ptt-demo ก่อน ตัวอย่างใช้ภาพจริงเพื่อวาดเอง จึงยังไม่นำเข้า YOLO labels เดิม

สิ่งที่ต้องกรอกเองมีเพียง CVAT PAT; IDs และ paths จะคำนวณให้ เก็บผลทดลองไว้ใน artifacts ซึ่ง Git ignore แล้ว ไม่เก็บ Token ลงไฟล์

## 1. เตรียมเครื่องมือและโฟลเดอร์ผลลัพธ์

คัดลอกทั้งกล่องนี้ลง Terminal:

```bash
cd /home/luke/cvat/cvat-workflow-guide
set -euo pipefail
command -v curl
command -v jq
command -v python3
export CVAT_BASE_URL='http://localhost:8080'
export CVAT_ORG='ptt-demo'
export DATASET_DIR='/home/luke/ai_training/codex_ptt_inspection/datasets/overall-ptt-object-detection.v11i.yolov11'
mkdir -p artifacts
export RUN_DIR="$(mktemp -d "$PWD/artifacts/api-test-XXXXXX")"
printf 'ผลทดลองอยู่ที่: %s\n' "$RUN_DIR"
curl --fail-with-body -sS "$CVAT_BASE_URL/api/server/health/?format=json"
```

หากคำสั่งใดล้มเหลว ให้หยุดแก้สาเหตุก่อน อย่ารันส่วนถัดไป Health ควรตอบ working หากขึ้น connection refused ให้เปิด CVAT ก่อน

## 2. ใส่ Token และตรวจบัญชี

Login ที่ http://localhost:8080 ใช้เมนู Access tokens ของบัญชีสร้าง PAT ที่เขียนข้อมูลได้ แล้วกลับมา Terminal รัน:

```bash
read -r -s -p 'วาง CVAT PAT แล้วกด Enter: ' CVAT_ACCESS_TOKEN
printf '\n'
export CVAT_ACCESS_TOKEN
api() {
  curl --fail-with-body --silent --show-error \
    --connect-timeout 10 --max-time 180 \
    -H "Authorization: Bearer $CVAT_ACCESS_TOKEN" "$@"
}
api "$CVAT_BASE_URL/api/users/self" | jq '{id,username}'
api "$CVAT_BASE_URL/api/projects?org=$CVAT_ORG&page_size=1" | jq '{count}'
```

ตัวอักษร Token ไม่แสดงตอนวาง เป็นเรื่องปกติ 401 = Token ผิด/หมดอายุ; 403 = บัญชีไม่มีสิทธิ์ในองค์กร ไม่ใช้ Token ของ Keycloak แทน

## 3. เลือกภาพจริง 2 รูปและเตรียม labels อัตโนมัติ

สคริปต์อ่านชื่อ 26 classes จาก data.yaml ที่มีอยู่ โดยรองรับรูปแบบ names เป็น list บรรทัดเดียวของ dataset นี้ ไม่ใช่ YAML parser ทั่วไป:

```bash
python3 - <<'PY'
import ast, json, os
from pathlib import Path
root = Path(os.environ['DATASET_DIR'])
out = Path(os.environ['RUN_DIR'])
images = sorted(p for p in (root/'train/images').iterdir()
                if p.suffix.lower() in {'.jpg','.jpeg','.png'})[:2]
assert len(images) == 2, 'ไม่พบภาพ train อย่างน้อย 2 รูป'
line = next(x for x in (root/'data.yaml').read_text().splitlines()
            if x.startswith('names:'))
names = ast.literal_eval(line.split(':',1)[1].strip())
assert isinstance(names,list) and all(isinstance(x,str) for x in names)
(out/'images.json').write_text(json.dumps([str(p) for p in images]))
project = {'name':'API-hands-on-'+out.name,
           'labels':[{'name':n,'type':'rectangle'} for n in names]}
(out/'project-input.json').write_text(json.dumps(project))
print('เลือกภาพ:',*[str(p) for p in images],sep='\n')
print('Classes:',len(names))
PY
IMAGE_1=$(jq -er '.[0]' "$RUN_DIR/images.json")
IMAGE_2=$(jq -er '.[1]' "$RUN_DIR/images.json")
```

ใช้เพียง path ของภาพต้นฉบับ ไม่มีการ copy dataset ทั้งชุด การส่งเข้า CVAT ขั้นต่อไปจะมี media สำเนาของงานนั้น

## 4. สร้าง Project ใหม่

```bash
api -X POST "$CVAT_BASE_URL/api/projects?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' \
  --data-binary "@$RUN_DIR/project-input.json" > "$RUN_DIR/project.json"
PROJECT_ID=$(jq -er '.id' "$RUN_DIR/project.json")
printf 'Project ID: %s\n' "$PROJECT_ID"
```

รัน POST นี้ครั้งเดียวต่อรอบ ถ้า timeout ให้ตรวจหน้า Projects และไฟล์ผลก่อน retry เพื่อไม่สร้างซ้ำ

## 5. สร้าง Task

```bash
jq -n --argjson pid "$PROJECT_ID" \
  '{name:"two-images-api-test",project_id:$pid,segment_size:20}' \
  > "$RUN_DIR/task-input.json"
api -X POST "$CVAT_BASE_URL/api/tasks?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' \
  --data-binary "@$RUN_DIR/task-input.json" > "$RUN_DIR/task.json"
TASK_ID=$(jq -er '.id' "$RUN_DIR/task.json")
printf 'Task ID: %s\n' "$TASK_ID"
```

ใช้ labels จาก Project ไม่ต้องส่ง labels ใน Task อีก

## 6. ส่งภาพและรอ CVAT เตรียมงาน

```bash
api -X POST "$CVAT_BASE_URL/api/tasks/$TASK_ID/data?org=$CVAT_ORG" \
  -F 'image_quality=85' \
  -F "client_files[0]=@$IMAGE_1" \
  -F "client_files[1]=@$IMAGE_2" > "$RUN_DIR/upload.json"
RQ_ID=$(jq -er '.rq_id' "$RUN_DIR/upload.json")
RQ_ENCODED=$(jq -rn --arg id "$RQ_ID" '$id|@uri')
READY=false
for attempt in $(seq 1 120); do
  api "$CVAT_BASE_URL/api/requests/$RQ_ENCODED?org=$CVAT_ORG" \
    > "$RUN_DIR/request.json"
  STATUS=$(jq -r '.status' "$RUN_DIR/request.json")
  printf 'Processing: %s\n' "$STATUS"
  case "$STATUS" in
    finished) READY=true; break ;;
    failed) cat "$RUN_DIR/request.json"; break ;;
    queued|started) sleep 2 ;;
    *) printf 'สถานะไม่รู้จัก ให้ตรวจ request.json\n'; break ;;
  esac
done
if [ "$READY" != true ]; then
  printf 'ยังไม่สำเร็จ หยุดที่ขั้นนี้และตรวจ request.json ก่อน\n'
  exit 1
fi
```

หากต้องรอเพิ่มให้รันเฉพาะส่วน polling เดิม ไม่ POST ภาพซ้ำลง Task

## 7. อ่าน Job แล้วเปิดใน browser

งานนี้มี 2 ภาพและ segment_size=20 จึงคาดว่าจะมี annotation Job เดียว คำสั่งตรวจจำนวนก่อนเลือก ไม่เงียบข้ามหน้าที่เหลือ:

```bash
api "$CVAT_BASE_URL/api/jobs?task_id=$TASK_ID&org=$CVAT_ORG&page_size=100" \
  > "$RUN_DIR/jobs.json"
jq -e '.next == null and ([.results[]|select(.type=="annotation")]|length)==1' \
  "$RUN_DIR/jobs.json" >/dev/null
JOB_ID=$(jq -er '.results[]|select(.type=="annotation")|.id' "$RUN_DIR/jobs.json")
api "$CVAT_BASE_URL/api/tasks/$TASK_ID/data/meta?org=$CVAT_ORG" \
  > "$RUN_DIR/media-meta.json"
jq -n --argjson project "$PROJECT_ID" --argjson task "$TASK_ID" --argjson job "$JOB_ID" \
  '{project_id:$project,task_id:$task,job_id:$job}' > "$RUN_DIR/ids.json"
api -X PATCH "$CVAT_BASE_URL/api/jobs/$JOB_ID?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' \
  --data '{"stage":"annotation","state":"in progress"}' | jq '{id,stage,state}'
printf '\nเปิดลิงก์นี้: %s/tasks/%s/jobs/%s\n' "$CVAT_BASE_URL" "$TASK_ID" "$JOB_ID"
```

คัดลอก URL ที่พิมพ์ออกมาเปิดใน browser Login บัญชีที่มีสิทธิ์กับ Project นี้ **วาด rectangle อย่างน้อย 1 กรอบบนภาพแรก** และเลือก class ที่เหมาะสม แล้วดูภาพที่สอง จากนั้นกด **Save** และรอจนบันทึกสำเร็จ

ขั้นตอนวาด/Save ต้องทำใน CVAT เอง Terminal เปลี่ยน state ไม่ได้ Save สิ่งที่ยังค้างใน browser

## 8. ดึงกรอบมาตรวจ ก่อนระบุเสร็จ

```bash
api "$CVAT_BASE_URL/api/jobs/$JOB_ID/annotations?org=$CVAT_ORG" \
  > "$RUN_DIR/annotations.json"
jq '{version,shape_count:(.shapes|length),tag_count:(.tags|length),track_count:(.tracks|length)}' \
  "$RUN_DIR/annotations.json"
jq '.shapes[]|{id,frame,label_id,type,points}' "$RUN_DIR/annotations.json"
```

shape_count ต้องมากกว่าศูนย์ตามการทดลองที่กำหนด หากเป็นศูนย์ให้ตรวจว่ากด Save ใน Job ที่ถูกต้องก่อน ไม่ใช่ข้อกำหนดทั่วไปว่าทุกภาพต้องมีวัตถุ

## 9. ระบุงานเสร็จและอ่านยืนยัน

```bash
jq -e '(.shapes|length)>0' "$RUN_DIR/annotations.json" >/dev/null
api -X PATCH "$CVAT_BASE_URL/api/jobs/$JOB_ID?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' \
  --data '{"stage":"annotation","state":"completed"}' > "$RUN_DIR/completed-job.json"
api "$CVAT_BASE_URL/api/jobs/$JOB_ID?org=$CVAT_ORG" \
  | jq '{id,task_id,stage,state}'
```

ผลควรเป็น annotation/completed หมายถึงเสร็จใน flow แบบง่าย ไม่ใช่การรับรอง QA แยกคน

## 10. อ่าน labels และจับคู่ภาพ/พิกัด

```bash
api "$CVAT_BASE_URL/api/labels?task_id=$TASK_ID&org=$CVAT_ORG&page_size=100" \
  > "$RUN_DIR/labels-page.json"
jq -e '.next==null' "$RUN_DIR/labels-page.json" >/dev/null
jq '.results' "$RUN_DIR/labels-page.json" > "$RUN_DIR/labels.json"
api "$CVAT_BASE_URL/api/jobs/$JOB_ID/annotations?org=$CVAT_ORG" \
  > "$RUN_DIR/annotations.json"
python3 - <<'PY'
import json, os
from pathlib import Path
p=Path(os.environ['RUN_DIR'])
ann=json.loads((p/'annotations.json').read_text())
meta=json.loads((p/'media-meta.json').read_text())
labels={x['id']:x['name'] for x in json.loads((p/'labels.json').read_text())}
# ใช้เฉพาะ task ภาพนิ่ง 2 รูปที่สร้างตามคู่มือนี้: frame เริ่ม 0 ไม่มี filter
assert meta['start_frame']==0 and not meta.get('frame_filter'), 'ต้องปรับ frame mapping'
frames=meta['frames']
assert len(frames)==2
rows=[]
for shape in ann['shapes']:
    frame=shape['frame']
    assert 0<=frame<len(frames)
    rows.append({'frame':frame,'image_name':frames[frame]['name'],
                 'width':frames[frame]['width'],'height':frames[frame]['height'],
                 'label':labels[shape['label_id']], 'type':shape['type'],
                 'points':shape['points'], 'rotation':shape.get('rotation',0)})
(p/'mapped-shapes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps(rows,ensure_ascii=False,indent=2))
print('ผลทั้งหมด:',p)
PY
unset CVAT_ACCESS_TOKEN
```

ผลอยู่ใน RUN_DIR ที่แสดงตอนเริ่ม: ids.json, media-meta.json, annotations.json, labels.json และ mapped-shapes.json ไฟล์หลังเป็นตัวอย่างแปลงข้อมูลให้เข้าใจง่าย ไม่ใช่ release contract สำหรับ geometry ทุกชนิด ไม่ได้เขียนลง Platform DB

ไม่ต้อง export ZIP เพื่ออ่านกรอบ และไม่มีคำสั่งลบ Project/Task อัตโนมัติ สามารถกลับมาเปิดงานที่สร้างไว้ต่อได้

## ข้อจำกัด/วิธีตรวจ

ตรวจว่ามี dataset จริงและเครื่องมือ curl/jq/python3 ในเครื่องนี้แล้ว ตัวอย่างคำสั่งตรวจ syntax แต่ยังไม่ได้ execute สร้าง Project/Task และ annotate ครบวงจรระหว่างเขียนคู่มือ ต้องมี PAT ที่ใช้งานได้และผู้ใช้ Save ใน editor ก่อนขั้น 8–10

ถ้าปิด Terminal ให้เปิดใหม่ ตั้งค่า BASE_URL/ORG/PAT และฟังก์ชัน api ตามขั้น 1–2 โดยชี้ RUN_DIR ไปโฟลเดอร์ผลเดิม แล้วอ่าน IDs จาก ids.json อย่ารัน POST สร้างงานใหม่โดยไม่ได้ตั้งใจ

[API workflow สำหรับ Backend](07_CVAT-API-WORKFLOW-QUICKSTART-TH.md) · [สารบัญ](00_DOCUMENT-INDEX-TH.md)
