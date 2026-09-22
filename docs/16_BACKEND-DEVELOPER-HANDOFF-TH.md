# Backend Developer Handoff: เชื่อม Platform กับ CVAT

เอกสารนี้สรุปสิ่งที่ Backend Developer ต้องเข้าใจและนำไปออกแบบต่อสำหรับ PTT AI Platform ที่ใช้ CVAT เป็น annotation service โดย Platform เป็นเจ้าของ business workflow และ database หลัก ส่วน CVAT เป็นระบบสำหรับทำ annotation และ review

## 1. ข้อสรุปที่ต้องยึดร่วมกัน

- MinIO เก็บภาพต้นฉบับและ object metadata
- CVAT เก็บ Project, Task, Job, labels, annotation และ workflow ภายในของเครื่องมือ
- Platform Database เก็บ business data, mapping, assignment, revision, audit และ dataset release
- Backend ติดต่อ CVAT ผ่าน REST API, Python SDK และ Webhook
- ห้ามเขียน SQL เพื่อแก้ข้อมูลใน CVAT PostgreSQL โดยตรง
- Keycloak ใช้ยืนยันตัวตนของ Platform; backend-to-CVAT ใช้ CVAT PAT/service account แยกกันจนกว่าจะตรวจ OIDC token delegation ของ deployment จริง
- Export ZIP/COCO/YOLO เป็น release artifact หรือ manual option ไม่ใช่ช่องทาง sync สถานะหลัก

## 2. ภาพรวม data flow

```text
ภาพเข้า MinIO
    ↓
Backend บันทึก image ใน Platform DB
    ↓
Backend สร้าง CVAT Project/Task ผ่าน REST API หรือ SDK
    ↓
CVAT สร้าง Job และผู้ใช้ทำ annotation
    ↓
CVAT ส่ง Webhook event หรือ Backend ทำ reconciliation
    ↓
Backend เรียก CVAT API อ่านสถานะและ annotation ล่าสุด
    ↓
Backend validate + map label/frame/points
    ↓
Platform DB บันทึก annotation revision แบบ idempotent
    ↓
ผ่าน review แล้วสร้าง Dataset Release
```

สำหรับ local PoC อาจ upload ไฟล์จาก path โดยตรงได้ แต่ production ควรใช้ MinIO/cloud storage หรือ ingestion service และต้องทดสอบว่า CVAT worker download/cache ไฟล์อย่างไร ไม่ควรอ้างว่า remote URL เป็น zero-copy โดยอัตโนมัติ

## 3. Mapping ที่ต้องเก็บใน Platform DB

อย่างน้อยควรเก็บ mapping เหล่านี้:

| Platform | CVAT | ความหมาย |
|---|---|---|
| `platform_project_id` | `cvat_project_id` | project เดียวกันในสองระบบ |
| `platform_image_id` | `task_id` + `frame` | ภาพต้นฉบับกับ frame ใน CVAT |
| `annotation_session_id` | `cvat_job_id` | งานที่ผู้ใช้กำลังทำ |
| `platform_label_id` | `cvat_label_id` | label schema ที่ map กัน |
| `annotation_revision` | annotation snapshot/time | รุ่นของผลลัพธ์ที่บันทึกแล้ว |
| `dataset_release_id` | export request/artifact reference | release ที่ผ่าน approval |

อย่าใช้ชื่อ Project, Task หรือชื่อไฟล์เป็น primary key เพราะชื่อเปลี่ยนได้และอาจซ้ำกันระหว่าง CVAT instances

## 4. CVAT API ที่ backend ใช้

API reference:

- [CVAT Documentation](https://docs.cvat.ai/docs/)
- [Interactive API Docs](https://app.cvat.ai/api/docs/)
- Local instance: `http://localhost:8080/api/docs/`

ตัวอย่างลำดับคำสั่ง:

```http
GET /api/users/self
POST /api/projects
POST /api/tasks
POST /api/tasks/{task_id}/data
GET /api/requests/{request_id}
GET /api/jobs?task_id={task_id}
GET /api/tasks/{task_id}/data/meta
GET /api/jobs/{job_id}/annotations
PATCH /api/jobs/{job_id}
POST /api/tasks/{task_id}/dataset/export
```

ใช้ Bearer PAT ฝั่ง backend:

```http
Authorization: Bearer <CVAT_PAT>
```

PAT ต้องอยู่ใน secret manager/environment ของ backend ห้ามส่งไป browser, log หรือ commit ใน repository

## 5. การสร้าง Project และ Task

สร้าง Project เพียงครั้งเดียวต่อ label schema ที่ใช้งาน:

```json
{
  "name": "PTT Object Detection",
  "labels": [
    {"name": "flange", "type": "rectangle"},
    {"name": "analog-gauge", "type": "rectangle"}
  ]
}
```

สร้าง Task โดยอ้าง Project:

```json
{
  "name": "inspection-batch-001",
  "project_id": 3,
  "segment_size": 20
}
```

บันทึก response ID ลง Platform DB ทันทีหลังได้รับ `201`. หาก timeout ให้ค้นหาจาก idempotency key/name หรือ correlation ID ก่อนสร้างใหม่ เพื่อป้องกัน Project/Task ซ้ำ

## 6. การส่งภาพจาก MinIO

ทางเลือกสำหรับ PoC:

```json
{
  "image_quality": 85,
  "remote_files": [
    "https://minio.example/inspection/img-101.jpg?<signed-query>",
    "https://minio.example/inspection/img-102.jpg?<signed-query>"
  ]
}
```

ข้อกำหนด:

- presigned URL ต้องเข้าถึงได้จาก CVAT worker ไม่ใช่แค่ browser
- URL ต้องไม่หมดอายุก่อน request processing เสร็จ
- ห้ามเก็บ URL ที่ sign แล้วเป็นข้อมูลถาวร
- เก็บ bucket/key/version/checksum แทน
- ไม่ส่ง MinIO access key ไป frontend
- ตรวจ cache/copy behavior ของ CVAT deployment จริง

เมื่อ upload เป็น asynchronous ให้เก็บ `request_id` และ poll จน `finished` หรือรับ event แล้วตรวจสถานะซ้ำ

## 7. อ่าน annotation และ map กลับภาพ

CVAT response ตัวอย่าง:

```json
{
  "version": 0,
  "shapes": [
    {
      "id": 246,
      "frame": 0,
      "label_id": 35,
      "type": "rectangle",
      "points": [980.0, 426.25, 1167.5, 622.5],
      "rotation": 0.0,
      "attributes": []
    }
  ],
  "tags": [],
  "tracks": []
}
```

Backend ต้อง:

1. เรียก labels API เพื่อ map `label_id` เป็นชื่อ label
2. เรียก media metadata เพื่อ map `frame` เป็นภาพจริง
3. ตรวจ width/height และชนิด shape
4. แปลงเป็น schema กลางของ Platform
5. บันทึก `cvat_shape_id`, `task_id`, `job_id` เป็น source reference

ตัวอย่าง schema กลาง:

```json
{
  "platform_image_id": "img-999",
  "source": {
    "cvat_instance": "cvat-local",
    "task_id": 55,
    "job_id": 81,
    "shape_id": 246
  },
  "label": "analog-gauge",
  "geometry": {
    "type": "rectangle",
    "xyxy": [980.0, 426.25, 1167.5, 622.5]
  },
  "revision_id": "rev-0003"
}
```

อย่าใช้ชื่อ Task แทนชื่อภาพ และอย่า assume ว่า webhook payload มี annotation ทั้งชุด

## 8. Webhook และ reconciliation

Webhook ใช้เป็น trigger ไม่ใช่ source of truth:

```text
CVAT Webhook → Backend inbox → ตรวจ signature/event → อ่าน resource ผ่าน API → upsert DB
```

Backend ต้องรองรับ:

- event ซ้ำ
- event มาช้า
- event สลับลำดับ
- worker หรือ receiver restart
- API อ่านข้อมูลไม่สำเร็จชั่วคราว

ใช้ signature/secret ตาม deployment จริง, เก็บ raw event ที่จำเป็น และสร้าง idempotency key จาก resource ID + revision/digest เมื่อเหมาะสม ทำ periodic reconciliation เพื่อแก้กรณี webhook หาย

## 9. Database schema ขั้นต่ำ

### `images`

```text
id
object_bucket
object_key
object_version
width
height
checksum
status
```

### `cvat_resources`

```text
platform_project_id
cvat_project_id
cvat_task_id
cvat_job_id
instance_id
```

### `annotation_revisions`

```text
id
platform_image_id
cvat_job_id
revision
source_digest
created_by
status
payload_json
created_at
```

### `annotations`

```text
id
revision_id
platform_image_id
label
shape_type
frame
geometry_json
attributes_json
cvat_shape_id
```

### `audit_events`

```text
id
actor_id
action
entity_type
entity_id
payload_json
occurred_at
```

## 10. Keycloak และสิทธิ์

- ผู้ใช้ frontend login ผ่าน Keycloak ของ Platform
- Backend ตรวจ token, organization/project membership และ assignment
- Backend ไม่ส่ง CVAT PAT ให้ผู้ใช้
- CVAT browser SSO กับ CVAT REST API authentication เป็นคนละเรื่อง
- ถ้า deployment รองรับ OIDC/SAML จึงค่อยเชื่อม SSO ตาม edition/version จริง
- PoC ให้ผู้ใช้ใน Organization มีสิทธิ์ระดับเดียวกันได้ แต่ควรกำหนดหนึ่งคนต่อ Job เพื่อป้องกันการแก้ชนกัน
- อย่าให้ผู้ใช้ทุกคนเป็น global administrator

## 11. Idempotency, retry และ transaction

ระบบต้องสมมติว่า network error อาจเกิดหลัง CVAT ทำงานสำเร็จแล้ว ดังนั้น:

1. สร้าง command record ก่อนเรียก CVAT
2. เก็บ correlation/idempotency key
3. เมื่อ timeout ให้ query resource เดิมก่อน retry POST
4. ใช้ bounded retry สำหรับ 429/5xx
5. อ่าน resource หลังเขียนเพื่อยืนยันผล
6. บันทึก annotation ด้วย `source_digest` หรือ unique constraint
7. ใช้ transaction ใน Platform DB เท่านั้น ไม่พยายามทำ distributed transaction ครอบ CVAT

ถ้า annotation ถูกแก้หรือลบใน CVAT การ sync รอบใหม่ต้อง replace/upsert revision ตาม policy ไม่ใช่ INSERT เพิ่มอย่างเดียว

## 12. Export และไฟล์ชั่วคราว

Production ไม่ควรสร้าง ZIP ทุกครั้งที่ต้องการดูสถานะหรือดึงกรอบ ให้ใช้ annotation API/SDK แล้วบันทึกลง Platform DB

Export ใช้เมื่อ:

- สร้าง Dataset Release
- ส่งเข้า training pipeline
- ส่งมอบให้ระบบภายนอก
- ทำ backup ตาม retention policy
- ทำ Optional Manual Flow เพื่อ debug/migration

ไฟล์ JSON เช่น `annotations.json`, `labels.json`, `media-meta.json` และ `mapped-shapes.json` เป็น artifacts ชั่วคราวจากการทดลอง Backend ควรอ่านเข้า memory/temporary storage แล้วลบหลัง transaction สำเร็จ ห้ามลบข้อมูลต้นฉบับใน CVAT หรือ MinIO ก่อนตรวจ commit

## 13. สิ่งที่ไม่ควรทำ

- ไม่เขียน SQL แก้ CVAT PostgreSQL โดยตรง
- ไม่ใช้ export ZIP เป็น status API
- ไม่ assume remote URL เป็น zero-copy
- ไม่ถือ webhook payload เป็น annotation source of truth
- ไม่ใช้ Keycloak JWT แทน CVAT PAT โดยไม่ตรวจรองรับ
- ไม่ส่ง PAT หรือ MinIO secret ไป frontend
- ไม่สร้าง Project/Task ใหม่ทุกครั้งที่ dashboard refresh
- ไม่ INSERT annotation ซ้ำเมื่อ retry
- ไม่ลบ Task อัตโนมัติทันทีหลัง sync โดยไม่ตรวจ retention, QA, lineage และ backup

## 14. สิ่งที่ควรส่งมอบจาก Backend

- API contract ของ Platform
- database migration/schema
- CVAT client service ที่มี retry/pagination
- webhook receiver + durable inbox
- annotation mapper และ validation
- idempotency/unique constraints
- audit event และ status transition
- MinIO presigned URL service
- export/release service
- test fixture จาก `artifacts/api-test-*` โดยตัด token และข้อมูลอ่อนไหวออก

## 15. คู่มือและข้อมูลประกอบ

- [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)
- [CVAT Documentation](https://docs.cvat.ai/docs/)
- [CVAT API Docs](https://app.cvat.ai/api/docs/)
- [Backend End-to-End](03_CVAT-MINIO-BACKEND-END-TO-END-TH.md)
- [REST API Quickstart](07_CVAT-API-WORKFLOW-QUICKSTART-TH.md)
- [Postman Workflow](09_CVAT-POSTMAN-WORKFLOW-GUIDE-TH.md)
- [Python SDK Hands-on](10_CVAT-SDK-HANDS-ON-TH.md)
- [Database Monitoring](12_CVAT-DATABASE-SCHEMA-MONITORING-GUIDE-TH.md)
- [Schema Reference](13_CVAT-DATABASE-SCHEMA-REFERENCE-TH.md)

