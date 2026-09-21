# ทางเลือกเมื่อ Backend ทำหน้า Annotation เอง

เอกสารนี้ใช้สำหรับกรณีที่ PTT AI Platform ต้องการแสดงหน้า annotation อยู่ใน frontend ของตนเอง โดยไม่ฝัง CVAT UI ทั้งหน้า และให้ backend ของ platform เป็นผู้ควบคุม authentication, งาน, database และการบันทึกผล

## ข้อสรุป

สำหรับ flow ปัจจุบัน แนะนำให้เริ่มจาก **Label Studio Frontend** หรือ **Annotorious**

- **Label Studio Frontend** เหมาะเมื่ออยากได้ labeling UI ที่ปรับแต่งได้หลายชนิดข้อมูลและมี callback ให้ผูกกับ backend ของเรา
- **Annotorious** เหมาะเมื่อเฟสแรกเป็นภาพนิ่งและ bounding box/polygon ต้องการ component ขนาดเล็กใน React/JavaScript
- หากต้องการ workflow ตรวจสอบหลายคน, issue, job assignment, history และ QA ครบเหมือนที่ทดสอบไว้ ควรใช้ CVAT ต่อไป แล้วให้ platform ฝังหรือเปิด CVAT ผ่าน link/proxy แทนการสร้าง editor เอง

การสร้าง frontend เองทำให้ประสบการณ์ผู้ใช้เป็นของเราเต็มที่ แต่ backend ต้องรับผิดชอบเองเรื่อง autosave, concurrency, version, undo/redo, validation, review, audit log, annotation locking และการแปลง format

## 5 ทางเลือกที่เหมาะกับการทำ frontend เอง

| ทางเลือก | ประเภท | จุดเด่น | เชื่อม backend ของเรา | เหมาะกับ flow นี้ | ภาระที่ต้องพัฒนาเอง |
| --- | --- | --- | --- | --- | --- |
| **Label Studio Frontend (LSF)** | React frontend package | Backend-agnostic, configurable labeling interface, มี callback และนำไป embed ในแอปได้ | สูงมาก: frontend เรียก API ของเราเองได้ | Image, text, audio และหลายชนิดข้อมูล | Data model, save/version, permission, review, storage adapter |
| **Annotorious** | JavaScript image-annotation library | ฝังในหน้าเว็บง่าย รองรับ rectangle/polygon/point และต่อ OpenSeadragon สำหรับภาพใหญ่ | สูง: เรากำหนด JSON และ API เอง | ภาพนิ่ง, object detection, segmentation เบื้องต้น | Toolbar, label selector, persistence, QA, keyboard workflow, collaboration |
| **react-image-annotate** | React component | มีตัวอย่าง UI สำหรับ polygon, bounding box, point และ tag | สูง: รับ state/props แล้วส่งผลกลับ backend | React PoC ที่ต้องการ editor สำเร็จรูปบางส่วน | ตรวจ maintenance, ปรับ UI, autosave, data contract, review |
| **VGG Image Annotator (VIA3)** | Standalone HTML/JavaScript app | น้ำหนักเบา รันใน browser ได้ รองรับ image/audio/video และไม่มี backend บังคับ | ปานกลาง: ต้องเขียน adapter/import-export หรือ fork UI | Offline/local หรือ batch เล็ก | Auth, API, multi-user, locking, review และ sync กับ MinIO |
| **MakeSense.ai** | Web application สำหรับ fork/ปรับแต่ง | มี UI labeling พร้อม export และเป็น GPLv3 | ปานกลางถึงต่ำ: เหมาะกับการ fork มากกว่า component | ทีมเล็กและ workflow ง่าย | แยก UI ออกจาก storage/auth, ทำ API integration, ดูแล fork และ license |

แหล่งอ้างอิง: [Label Studio Frontend](https://github.com/HumanSignal/label-studio-frontend) เป็น React frontend ที่ระบุว่าสามารถ embed และ backend-agnostic ได้, [Label Studio frontend reference](https://labelstud.io/guide/frontend_reference), [Annotorious](https://annotorious.dev/getting-started/) เป็น JavaScript library สำหรับเพิ่ม image annotation ให้เว็บ, [react-image-annotate](https://github.com/UniversalDataTool/react-image-annotate), [VIA3](https://github.com/ox-vgg/via), และ [MakeSense](https://www.makesense.ai/)

## ตารางให้คะแนนตามระบบของเรา

คะแนน 1–5: 5 = ตรงกับความต้องการและมีทางเชื่อมชัดเจน, 3 = ทำได้แต่ต้องเขียน adapter, 1 = ไม่ใช่จุดประสงค์ของเครื่องมือ

| ปัจจัย | LSF | Annotorious | react-image-annotate | VIA3 | MakeSense | CVAT UI (ใช้เป็น baseline) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ฝังในหน้า platform | **5** | **5** | 4 | 2 | 2 | 2 |
| ควบคุม API/database เอง | **5** | **5** | **5** | 3 | 2 | 1 |
| Bounding box/polygon | 5 | **5** | **5** | 4 | 5 | **5** |
| Image ใหญ่/zoom | 4 | **5** (OpenSeadragon) | 3 | 3 | 3 | **5** |
| Multi-user/review/issue | 2 | 1 | 1 | 1 | 2 | **5** |
| Text/audio/multimodal | **5** | 1 | 1 | 4 | 1 | 3 |
| ความเร็วในการทำ PoC | 4 | **5** | 4 | 4 | 4 | 3 |
| ภาระดูแลระยะยาว | 3 | 4 | 3 | 4 | 2 | 3 |

คะแนนนี้เป็นการประเมินเชิงออกแบบ ไม่ใช่ benchmark ความเร็วหรือความถูกต้องของแต่ละโครงการ ควรทำ prototype กับภาพจริง 20–100 ภาพก่อนตัดสินใจ

## สถาปัตยกรรมที่ควรใช้กับ frontend editor

```text
Browser + Keycloak login
        │ access token ของ platform
        ▼
Platform Backend API
        ├── ตรวจสิทธิ์และ job assignment
        ├── อ่าน metadata จาก platform DB
        ├── ขอ presigned GET URL จาก MinIO
        ├── ส่ง annotation task/session ให้ frontend
        └── บันทึก revision ลง platform DB
                 │
                 └── MinIO เก็บภาพต้นฉบับ (ไม่ส่งไฟล์ผ่าน backend ถ้าไม่จำเป็น)
```

Frontend annotation tool ไม่ควรคุยกับ PostgreSQL, MinIO credential หรือ CVAT database โดยตรง

1. ผู้ใช้ล็อกอินผ่าน Keycloak ที่ platform และได้ access token ของ platform
2. Frontend เรียก `GET /api/annotation-sessions/{id}` ไปยัง backend
3. Backend ตรวจสิทธิ์ แล้วส่ง image metadata และ presigned URL อายุสั้นจาก MinIO
4. Frontend โหลดรูปจาก URL และแสดง editor
5. เมื่อผู้ใช้กด save ให้ส่ง normalized annotation JSON ไป `PUT /api/annotation-sessions/{id}/annotations`
6. Backend ตรวจ schema, image dimensions, label และ version จากนั้นบันทึก transaction ลง DB
7. เมื่อกด submit ให้ backend เปลี่ยนสถานะเป็น `submitted` และสร้าง audit event
8. Reviewer เปิด revision ที่ส่งแล้วและเปลี่ยนสถานะเป็น `approved` หรือ `changes_requested`

## API contract ขั้นต่ำที่ backend ควรเตรียม

```http
GET /api/annotation-sessions/{session_id}
Authorization: Bearer <platform-keycloak-token>
```

```json
{
  "session_id": "sess_123",
  "image": {
    "id": "img_999",
    "name": "008835.jpg",
    "width": 1920,
    "height": 1080,
    "url": "https://minio.example/presigned-url"
  },
  "labels": [{"id": "flange", "name": "flange", "color": "#4f8cff"}],
  "revision": 3,
  "status": "in_progress"
}
```

```http
PUT /api/annotation-sessions/{session_id}/annotations
If-Match: "revision-3"
Authorization: Bearer <platform-keycloak-token>
Content-Type: application/json
```

```json
{
  "base_revision": 3,
  "annotations": [
    {
      "client_id": "shape-1",
      "type": "rectangle",
      "label": "flange",
      "frame": 0,
      "points": [817.5, 680.0, 1075.0, 948.75],
      "attributes": {}
    }
  ]
}
```

Backend ต้องตอบ `409 Conflict` เมื่อ revision เปลี่ยนระหว่างที่มีผู้ใช้อื่นแก้ไข เพื่อป้องกันการเขียนทับข้อมูลโดยไม่ตั้งใจ

## โครงสร้างข้อมูลที่ควรเก็บ

| ตาราง | หน้าที่ | ตัวอย่างคอลัมน์ |
| --- | --- | --- |
| `images` | mapping ภาพกับ MinIO | `id`, `object_key`, `width`, `height`, `checksum` |
| `annotation_sessions` | งานและผู้รับผิดชอบ | `id`, `image_id`, `assignee_id`, `status`, `current_revision` |
| `annotation_revisions` | snapshot ที่แก้ไขแต่ละครั้ง | `id`, `session_id`, `revision`, `created_by`, `payload_json`, `created_at` |
| `annotations` | ข้อมูลที่ normalize สำหรับ query/train | `revision_id`, `label`, `shape_type`, `x1`, `y1`, `x2`, `y2` หรือ geometry JSONB |
| `audit_events` | ประวัติการทำงาน | `actor_id`, `action`, `entity_id`, `occurred_at` |

ไม่ควรเก็บ presigned URL ถาวรใน DB และไม่ควรเก็บภาพซ้ำใน annotation database เก็บเพียง object key/checksum และสร้าง URL ใหม่เมื่อจำเป็น

## Keycloak และสิทธิ์

- Keycloak ออก token ให้ platform frontend/backend ตาม client ของ platform
- Backend เป็นผู้ตรวจ role, project membership และ job assignment
- Frontend annotation library ไม่ต้องรู้ client secret ของ Keycloak
- ถ้า frontend ต้องเรียก MinIO โดยตรง ให้ backend ออก presigned URL อายุสั้นแทนการส่ง access key
- หากยังใช้ CVAT เป็นระบบ annotation หลัก ให้ backend ใช้ CVAT PAT/service account แยกจาก browser token ตามคู่มือเดิม

## คำแนะนำการเลือก

| สถานการณ์ | ตัวเลือก |
| --- | --- |
| ต้องการทำ PoC React ที่ควบคุม API เองเร็วที่สุด | **Annotorious** |
| ต้องการ editor หลายชนิดข้อมูลและ UI configurable | **Label Studio Frontend** |
| ต้องการ React component ที่มี editor image สำเร็จรูป | **react-image-annotate** |
| ต้องการเครื่องมือ standalone/offline และทีมพร้อมเขียน adapter | **VIA3** |
| ต้องการ fork แอป labeling ทั้งตัวและยอมดูแล GPLv3 | **MakeSense.ai** |
| ต้องการ QA, assignment, issue และ workflow หลายผู้ใช้ครบ | **ใช้ CVAT ต่อไป** |

สำหรับระบบจริงของเรา ควรเริ่ม prototype ด้วย Annotorious หรือ Label Studio Frontend แล้วทดสอบ 5 เรื่องก่อนตัดสินใจ: การโหลดภาพจาก MinIO, การ save/reload, concurrent edit, การ map Keycloak user และการสร้าง export YOLO/COCO จาก backend DB หากต้องพัฒนา review/assignment เองมากเกินไป ให้กลับไปใช้ CVAT เป็น annotation engine แล้วใช้ platform เป็น orchestration layer

