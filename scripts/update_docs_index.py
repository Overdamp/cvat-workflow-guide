#!/usr/bin/env python3
"""Generate a deterministic Markdown index; --check supports CI."""
from pathlib import Path
import argparse
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'DOCS-INDEX.md'
GROUPS = ['คู่มือหลัก', 'คู่มือใช้งานและ API', 'ฐานข้อมูล', 'ระบบทดลองและตัวอย่าง', 'เอกสารประวัติ / ลิงก์ย้าย', 'เอกสารอื่นและไฟล์ใหม่']
KNOWN = {
 'docs/08_CVAT-HANDS-ON-LOCAL-DATASET-TH.md': (1, 'ทดลองทีละขั้นด้วยภาพจริงจาก dataset ในเครื่อง luke'),
 'docs/09_CVAT-POSTMAN-WORKFLOW-GUIDE-TH.md': (1, 'ทดลอง REST API ผ่าน Postman แบบเรียงลำดับ'),
 'docs/07_CVAT-API-WORKFLOW-QUICKSTART-TH.md': (1, 'คำสั่ง curl ตั้งแต่สร้าง Project จนดึงผล; PoC สิทธิ์เท่ากัน'),
 'README.md': (0, 'จุดเริ่มต้นและสถานะโครงการ'),
 'docs/03_CVAT-MINIO-BACKEND-END-TO-END-TH.md': (0, 'ข้อกำหนดหลักสำหรับ Backend; MinIO/API/SDK/Webhook/DB/Auth'),
 'docs/01_AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md': (0, 'ภาพรวมผลิตภัณฑ์และสถาปัตยกรรมเป้าหมาย'),
 'docs/04_CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md': (0, 'Integration contract และความสอดคล้องระหว่างบริการ'),
 'docs/05_CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md': (1, 'กติกา workflow/queue; schema เป็นข้อเสนอ'),
 'docs/06_CVAT-WORKFLOW-OPERATIONS-GUIDE-TH.md': (1, 'ขั้นตอนของ Annotator/Reviewer/Coordinator'),
 'docs/11_CVAT-JOB-STATUS-API-GUIDE-TH.md': (1, 'อ่านสถานะและสร้างรายงานผ่าน API'),
 'docs/16_BACKEND-DEVELOPER-HANDOFF-TH.md': (0, 'เอกสารส่งต่องาน Backend; API/DB/Auth/MinIO/Webhook'),
 'docs/18_ANNOTATION-EDITOR-FEATURE-MATRIX-TH.md': (0, 'เทียบฟีเจอร์หน้า annotate โดยใช้ Roboflow เป็น baseline'),
}

def render():
    sections = {group: [] for group in GROUPS}
    for p in sorted(ROOT.rglob('*.md')):
        relative = p.relative_to(ROOT)
        if p == INDEX or 'DAILY-REPORT-' in p.name or any(part.startswith('.') or part in {'node_modules', 'venv'} for part in relative.parts):
            continue
        name = relative.as_posix()
        lines = p.read_text(encoding='utf-8').splitlines()
        title = next((line[2:].strip() for line in lines if line.startswith('# ')), p.stem)
        if name in KNOWN:
            group, description = KNOWN[name]
        elif 'archive' in relative.parts or p.name == 'CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md':
            group, description = 4, 'ประวัติ / ทางไปเอกสารที่ย้ายแล้ว ไม่ใช่ implementation contract'
        elif p.name.startswith('CVAT-DATABASE-'):
            group, description = 2, 'Reference/monitoring; ตรวจวันที่ snapshot ก่อนใช้'
        elif relative.parts[0] in {'prototype', 'examples'}:
            group, description = 3, 'ตรวจข้อจำกัดและผลทดสอบในเอกสาร'
        else:
            group, description = 5, 'ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์'
        title = title.replace('|', '\\|')
        sections[GROUPS[group]].append(f'| [{title}]({quote(name)}) | `{name}` | {description} |')
    out = ['# สารบัญคู่มือ CVAT + AI Platform', '',
           'สร้างจากไฟล์ Markdown ใน repository ด้วย `python3 scripts/update_docs_index.py` ห้ามแก้ตารางด้วยมือ', '',
           'เริ่มพัฒนา: README → คู่มือ Backend End-to-End → Workflow/API → Prototype ตามหน้าที่ของผู้อ่าน', '',
           'ไฟล์ใหม่จะปรากฏโดยอัตโนมัติ ไม่ต้องเพิ่มรายการชื่อไฟล์ในสคริปต์; กลุ่มเอกสารอื่นใช้สำหรับไฟล์ที่ยังไม่ได้ระบุหมวด', '']
    for group, rows in sections.items():
        if rows:
            out += [f'## {group}', '', '| เอกสาร | ไฟล์ | การใช้งาน |', '|---|---|---|', *rows, '']
    return '\n'.join(out) + '\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    content = render()
    if args.check:
        if not INDEX.exists() or INDEX.read_text(encoding='utf-8') != content:
            sys.exit('สารบัญยังไม่อัปเดต: python3 scripts/update_docs_index.py')
    else:
        INDEX.write_text(content, encoding='utf-8')
        print('Updated DOCS-INDEX.md')
