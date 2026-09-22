# Daily Report — 22 September 2026

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

## 1. Today’s Goals

- กำหนดเครื่องมือ annotation ที่เหมาะกับสถาปัตยกรรม PTT AI Platform
- เปรียบเทียบแนวทางใช้ CVAT เต็มระบบกับการสร้าง frontend annotation เอง
- สรุป workflow และคำสั่ง REST API/Python SDK สำหรับส่งให้ Backend Developer

## 2. Completed Tasks ✅

- จัดทำตารางเปรียบเทียบ CVAT, Label Studio, V7 Darwin, Labelbox, LabelMe, doccano, Supervisely และ FiftyOne
- จัดกลุ่มเครื่องมือแบบ open source/self-hosted กับ managed/commercial
- จัดทำคู่มือทางเลือก frontend annotation ได้แก่ Label Studio Frontend, Annotorious, react-image-annotate, VIA3 และ MakeSense.ai
- ยืนยันแนวทางหลัก: MinIO เก็บภาพ, CVAT ทำ annotation, Backend database เก็บผลลัพธ์และสถานะธุรกิจ
- สรุปการใช้ REST API, Python SDK, PAT และ webhook สำหรับควบคุม CVAT
- อัปเดตสารบัญและ push เอกสารขึ้น GitHub repository

## 3. Ongoing Tasks 🔄

- ประเมินการเชื่อม Keycloak/OIDC กับ deployment และ role mapping จริง
- ทดสอบ MinIO presigned URL กับ task ขนาดใหญ่และสิทธิ์การเข้าถึงแบบหมดอายุ
- กำหนด schema ของ annotation revision, audit event และ dataset release ใน platform database

## 4. Issues / Concerns ⚠️

- Keycloak browser SSO กับ backend CVAT API token เป็นคนละส่วน ไม่ควรส่ง Keycloak JWT ไปใช้แทน CVAT PAT โดยไม่ตรวจการรองรับของ deployment
- หากสร้าง frontend annotation เอง จะต้องพัฒนา autosave, revision, concurrency, review, issue, locking และ audit log เอง
- Remote storage ช่วยลดการเก็บไฟล์ซ้ำ แต่ต้องทดสอบว่า service ใดดาวน์โหลดหรือ cache ภาพใน deployment จริง
- CVAT SDK และ server ควรใช้ major/minor version ที่เข้ากันได้

## 5. Answers for Review / Meeting

### Q: Which annotation tools are appropriate for this project?

**A:**

เครื่องมือที่เหมาะสมแบ่งเป็นสองกลุ่ม:

1. **CVAT Community** — ตัวเลือกหลักสำหรับโครงการ เพราะเป็น open source/self-hosted, รองรับ computer vision workflow แบบ Project/Task/Job, review/issue, multi-user, REST API, Python SDK, webhook, MinIO/S3 และ format เช่น YOLO/COCO
2. **Label Studio OSS** — ทางเลือกเมื่อ platform ต้องรองรับ image, text, audio หรือ multimodal และต้องการปรับ labeling interface ได้มาก
3. **FiftyOne** — ใช้เสริมสำหรับ dataset curation, quality analysis และ model evaluation ไม่ควรใช้แทน annotation workflow หลัก
4. **doccano** — เหมาะสำหรับบริการเสริมด้าน NLP/text annotation
5. **Label Studio Frontend หรือ Annotorious** — เหมาะเมื่อ backend ต้องสร้างหน้า annotation ใน platform เองและยอมรับภาระพัฒนา workflow เพิ่ม

V7 Darwin, Labelbox และ Roboflow เหมาะสำหรับการเปรียบเทียบ managed platform แต่ไม่ใช่ตัวเลือกหลักเมื่อเกณฑ์สำคัญคือ open source และการควบคุมข้อมูลภายในองค์กร

### Q: Give me the annotation tools comparison table.

**A:**

| Tool | Open source/self-host | เหมาะกับ | API/Integration | ข้อจำกัดสำหรับโครงการนี้ |
|---|---|---|---|---|
| **CVAT Community** | ใช่ | Image/video/3D computer vision และ workflow ทีม | REST API, SDK, CLI, webhook, cloud storage | ต้องดูแล Docker, backup, upgrade และ monitoring |
| **Label Studio OSS** | ใช่ | Image, text, audio, multimodal | API, SDK, webhook, external storage, embeddable frontend | ต้องออกแบบ workflow CV และ QA ให้ตรงกับงานเอง |
| **FiftyOne** | ใช่ | Dataset inspection, curation, model evaluation | Python SDK และ integrations | ไม่ใช่ระบบ assignment/review หลัก |
| **doccano** | ใช่ | Text classification และ sequence labeling | REST API/client | ไม่เหมาะกับ bounding box/segmentation ภาพ |
| **Label Studio Frontend** | ใช้เป็น frontend package | สร้าง annotation page เองใน React | Backend-agnostic callbacks | Backend ต้องสร้าง persistence, review, revision และ auth flow |
| **Annotorious** | ใช่ | ฝัง rectangle/polygon/point ในเว็บ | JavaScript API, OpenSeadragon | เป็น editor component ไม่ใช่ระบบจัดการงานครบชุด |
| **VIA3** | ใช่ | Offline/local image, audio, video annotation | ต้องเขียน adapter เอง | ไม่มี multi-user backend workflow ในตัว |
| **LabelMe** | ใช่ | Local image annotation | ไฟล์ JSON/local workflow | ไม่เหมาะกับ server workflow และ collaboration |
| **V7 / Labelbox / Roboflow** | ส่วนใหญ่เป็น managed/commercial | SaaS และ AI data platform | มี API/SDK ตามแผนบริการ | data residency, ราคา, vendor lock-in และการควบคุม infra |

**Decision:** เลือก **CVAT Community** เป็น annotation engine หลัก และใช้ Label Studio Frontend/Annotorious เฉพาะกรณีที่ต้องสร้างหน้า custom โดยตรงใน platform

### Q: Workflow of CVAT and how to use REST API to control it.

**A:**

```text
MinIO/object storage
  ↓
Backend สร้าง Project/Task ผ่าน CVAT REST API
  ↓
CVAT สร้าง Job และมอบหมายให้ annotator
  ↓
Annotator เปิด Job และบันทึก annotation
  ↓
Reviewer ตรวจงาน แก้ issue/comment และเปลี่ยนสถานะ
  ↓
Webhook แจ้ง Backend เมื่อเกิด event สำคัญ
  ↓
Backend เรียก annotation API เพื่ออ่านผลจริง
  ↓
Upsert ลง platform database และสร้าง dataset release
```

คำสั่งหลักที่ backend ใช้:

```bash
# ตั้งค่า token และ helper
export CVAT_BASE_URL=http://localhost:8080
export CVAT_ACCESS_TOKEN='ใส่-CVAT-PAT-ที่นี่'
api() {
  curl --fail-with-body --silent --show-error \
    -H "Authorization: Bearer $CVAT_ACCESS_TOKEN" "$@"
}

# ตรวจผู้ใช้และ server
api "$CVAT_BASE_URL/api/users/self" | jq
api "$CVAT_BASE_URL/api/server/health/?format=json" | jq

# อ่าน projects
api "$CVAT_BASE_URL/api/projects?page_size=100" | jq

# สร้าง task (ตัวอย่าง payload ต้องปรับ label/schema ให้ตรง project)
curl --fail-with-body --silent --show-error -X POST \
  "$CVAT_BASE_URL/api/tasks" \
  -H "Authorization: Bearer $CVAT_ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"name":"batch-001","labels":[{"name":"flange"},{"name":"analog-gauge"}]}' | jq

# อ่าน jobs และสถานะ
api "$CVAT_BASE_URL/api/jobs?task_id=$TASK_ID&page_size=100" | jq
api "$CVAT_BASE_URL/api/jobs/$JOB_ID" | jq '{id,stage,state,assignee}'

# อ่าน metadata ของภาพและ annotation ของ job
api "$CVAT_BASE_URL/api/tasks/$TASK_ID/data/meta" > media-meta.json
api "$CVAT_BASE_URL/api/jobs/$JOB_ID/annotations" > annotations.json

# เปลี่ยนสถานะ job เมื่อ workflow อนุญาต
curl --fail-with-body --silent --show-error -X PATCH \
  "$CVAT_BASE_URL/api/jobs/$JOB_ID" \
  -H "Authorization: Bearer $CVAT_ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"stage":"validation","state":"in progress"}' | jq
```

การสร้าง task และอัปโหลดภาพจริงต้องใช้ endpoint ที่ตรงกับวิธี data ingestion ของ deployment หากภาพอยู่ใน MinIO ให้ใช้ cloud storage/remote file configuration ที่รองรับ และอย่าฝัง MinIO secret ใน browser

Webhook ใช้เป็น **สัญญาณ** ว่ามีการเปลี่ยนแปลง ไม่ควรถือว่า payload webhook เป็น annotation ชุดสุดท้ายเสมอไป Backend ควรรับ event, ตรวจลายเซ็น/secret, เรียก `GET /api/jobs/{job_id}/annotations` อีกครั้ง แล้วทำ idempotent upsert ลงฐานข้อมูลของ platform

### Q: How to use the Python SDK to control it?

**A:**

ติดตั้ง SDK ที่มี major/minor version สอดคล้องกับ CVAT server:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install cvat-sdk
```

ตัวอย่างอ่าน projects, tasks, jobs และ annotations:

```python
import os
from cvat_sdk import make_client

server = os.environ.get("CVAT_BASE_URL", "http://localhost:8080")
token = os.environ["CVAT_ACCESS_TOKEN"]
task_id = int(os.environ["TASK_ID"])

with make_client(server, access_token=token) as client:
    for project in client.projects.list():
        print(project.id, project.name)

    task = client.tasks.retrieve(task_id)
    print("task:", task.id, task.name)

    for job in task.get_jobs():
        print("job:", job.id, job.status, job.stage)
        annotations = job.get_annotations()
        print("shapes:", len(annotations.shapes))
```

ตัวอย่างสร้าง task ด้วย SDK ควรตรวจ signature ของ SDK รุ่นที่ติดตั้งก่อน เพราะ API ของ server และ SDK ต้องใช้รุ่นที่เข้ากันได้ ใน PoC นี้ใช้ project ที่มี labels อยู่แล้ว:

```python
from cvat_sdk import make_client

with make_client(server, access_token=token) as client:
    task = client.tasks.create({
        "name": "batch-001",
        "project_id": int(os.environ["PROJECT_ID"]),
    })
    print("created task", task.id)
```

ใน production ควรห่อ SDK ไว้ใน service ของ backend และไม่ให้ frontend เรียก CVAT โดยตรง Backend ควรทำหน้าที่ map `platform_image_id` กับ `cvat_task_id/cvat_job_id`, จัดการ retry, pagination, webhook idempotency และบันทึก revision ก่อนส่งผลไป training pipeline

## 6. Notes / Reflections ✍️

- CVAT เหมาะเป็น annotation engine เพราะลดการพัฒนา workflow เองและทีมมีผลการทดสอบจริงแล้ว
- Custom frontend เหมาะเมื่อประสบการณ์ผู้ใช้สำคัญกว่าความครบของ review/assignment และทีมพร้อมสร้างระบบ annotation state เอง
- การ export ควรใช้สำหรับ dataset release ไม่ใช่ใช้เป็นกลไกหลักในการ sync สถานะทุกครั้ง

## References

- [CVAT API Docs](https://app.cvat.ai/api/docs/)
- [CVAT Developer Documentation](https://docs.cvat.ai/docs/api_sdk/)
- [CVAT Server API](https://docs.cvat.ai/docs/api_sdk/api/)
- [CVAT Python SDK](https://docs.cvat.ai/docs/api_sdk/sdk/)
- [Custom Annotation Frontend Options](./14_CUSTOM-ANNOTATION-FRONTEND-OPTIONS-TH.md)
- [Annotation Tool Selection Matrix](./02_ANNOTATION-TOOL-SELECTION-MATRIX-TH.md)
