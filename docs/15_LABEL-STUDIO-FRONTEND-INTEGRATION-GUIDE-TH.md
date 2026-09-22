# แนวทางเลือก Label Studio Frontend (LSF)

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

เอกสารนี้อธิบายแนวทางกรณีที่ PTT AI Platform ต้องการนำ **Label Studio Frontend (LSF)** มาใช้เป็น editor ในหน้าเว็บของตนเอง โดยให้ platform backend เป็นผู้ควบคุม authentication, database, workflow, review และการจัดเก็บผลลัพธ์

LSF เป็น frontend package ที่เขียนด้วย React และออกแบบให้ embed ในแอปพลิเคชันได้ โดย backend ของเราเป็นผู้จัดการข้อมูลหลัก เอกสารทางการ: [Label Studio Frontend repository](https://github.com/HumanSignal/label-studio-frontend) และ [Frontend reference](https://labelstud.io/guide/frontend_reference)

## 1. เมื่อใดควรเลือก LSF

เลือก LSF เมื่อ:

- ต้องการให้หน้า annotation อยู่ใน platform ของเราเอง
- ต้องการใช้ Keycloak login เดิมโดยไม่ให้ผู้ใช้เข้า CVAT แยก
- ต้องการให้ backend database เดิมเป็นแหล่งข้อมูลหลัก
- ต้องการดึงภาพจาก MinIO ผ่าน presigned URL
- ต้องการกำหนดหน้าตาและ workflow เอง
- ทีมพร้อมพัฒนา autosave, revision, review, audit และ conflict handling

ถ้าต้องการ assignment, review, issue, QA, history และ multi-user workflow ครบโดยไม่สร้างเอง ควรใช้ CVAT เป็น annotation engine ต่อไป

## 2. สถาปัตยกรรมที่เสนอ

```text
ผู้ใช้เปิด Platform
        │
        ├── Login ผ่าน Keycloak
        │       └── Platform access token
        ▼
Platform Frontend
        ├── Label Studio Frontend (editor)
        └── เรียก Platform Backend API
                         │
                         ├── ตรวจ user / role / assignment
                         ├── อ่าน metadata จาก Platform DB
                         ├── ขอ presigned URL จาก MinIO
                         ├── บันทึก annotation revision
                         ├── จัดการ review และ audit
                         └── สร้าง dataset release

MinIO ── เก็บภาพต้นฉบับ
PostgreSQL ── เก็บ metadata, annotation และ workflow state
```

LSF ไม่ควรติดต่อ PostgreSQL, MinIO credential หรือ Keycloak client secret โดยตรง

## 3. Workflow ตั้งแต่ต้นจนจบ

1. ผู้ใช้ login ผ่าน Keycloak
2. Frontend ขอ annotation session จาก backend
3. Backend ตรวจ project membership และ assignment
4. Backend อ่าน `object_key` ของภาพจาก database
5. Backend สร้าง presigned GET URL จาก MinIO อายุสั้น
6. Frontend ส่งภาพและ label schema ให้ LSF
7. ผู้ใช้สร้างหรือแก้ bounding box/polygon/point
8. Frontend เก็บ state ระหว่างแก้ไขและ autosave ตามช่วงเวลา
9. Backend validate และบันทึก revision
10. ผู้ใช้กด Submit
11. Reviewer ตรวจและเลือก `approved` หรือ `changes_requested`
12. Backend สร้าง dataset release เมื่อผ่านการตรวจ

## 4. API ที่ backend ต้องพัฒนา

### โหลด annotation session

```http
GET /api/annotation-sessions/{session_id}
Authorization: Bearer <platform-keycloak-token>
```

ตัวอย่าง response:

```json
{
  "session_id": "sess_123",
  "status": "in_progress",
  "revision": 3,
  "image": {
    "id": "img_999",
    "name": "008835.jpg",
    "width": 1920,
    "height": 1080,
    "url": "https://minio.example/presigned-url"
  },
  "labels": [
    {"id": "flange", "name": "flange", "color": "#4f8cff"},
    {"id": "analog-gauge", "name": "analog-gauge", "color": "#e67e22"}
  ],
  "annotations": []
}
```

### บันทึก annotation

```http
PUT /api/annotation-sessions/{session_id}/annotations
Authorization: Bearer <platform-keycloak-token>
If-Match: "revision-3"
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

### Submit งาน

```http
POST /api/annotation-sessions/{session_id}/submit
Authorization: Bearer <platform-keycloak-token>
Content-Type: application/json
```

```json
{
  "revision": 4,
  "comment": "ตรวจ annotation ครบแล้ว"
}
```

### Review งาน

```http
POST /api/annotation-sessions/{session_id}/review
Authorization: Bearer <platform-keycloak-token>
Content-Type: application/json
```

```json
{
  "decision": "approved",
  "comment": "ผ่านการตรวจสอบ"
}
```

## 5. การจัดการ revision และผู้ใช้หลายคน

ทุกครั้งที่บันทึกควรสร้าง revision หรือใช้ optimistic locking:

```text
ผู้ใช้ A โหลด revision 3
ผู้ใช้ B โหลด revision 3
ผู้ใช้ A บันทึกสำเร็จ → revision 4
ผู้ใช้ B ส่งข้อมูลโดยอ้าง revision 3 → Backend ตอบ 409 Conflict
```

เมื่อเกิด `409 Conflict` frontend ต้องโหลดข้อมูล revision ล่าสุดและให้ผู้ใช้เลือก merge หรือแก้ใหม่ ห้ามเขียนทับข้อมูลโดยอัตโนมัติ

## 6. ตาราง database ที่ควรมี

### `images`

| คอลัมน์ | หน้าที่ |
|---|---|
| `id` | รหัสภาพใน platform |
| `object_key` | path ของ object ใน MinIO |
| `width`, `height` | ขนาดภาพจริง |
| `checksum` | ตรวจไฟล์ซ้ำหรือไฟล์เปลี่ยน |
| `created_at` | วันที่นำเข้า |

### `annotation_sessions`

| คอลัมน์ | หน้าที่ |
|---|---|
| `id` | รหัส session |
| `image_id` | อ้างอิงภาพ |
| `project_id` | อ้างอิง project |
| `assignee_id` | ผู้รับผิดชอบ |
| `status` | `queued`, `in_progress`, `submitted`, `approved`, `changes_requested` |
| `current_revision` | revision ล่าสุด |

### `annotation_revisions`

| คอลัมน์ | หน้าที่ |
|---|---|
| `id` | รหัส revision |
| `session_id` | อ้างอิง session |
| `revision` | เลข revision เพิ่มขึ้นทีละหนึ่ง |
| `created_by` | ผู้บันทึก |
| `payload_json` | snapshot ของ annotation |
| `created_at` | เวลาบันทึก |

### `annotations`

เก็บข้อมูลที่ normalize แล้วสำหรับ query และ training:

```text
id
revision_id
label
shape_type
frame
x1, y1, x2, y2
geometry_json
attributes_json
```

### `audit_events`

เก็บประวัติ เช่น `session_created`, `autosaved`, `submitted`, `approved`, `changes_requested` และ `exported`

## 7. Keycloak

- Keycloak ออก token ให้ platform frontend
- Backend ตรวจ token และสิทธิ์ของผู้ใช้
- LSF ไม่ควรเก็บ client secret
- Backend เป็นผู้ตรวจ project membership และ assignment
- อย่าส่ง MinIO access key ไป browser
- ใช้ presigned URL อายุสั้นสำหรับอ่านภาพ
- หากยังเชื่อม CVAT อยู่ ให้ CVAT ใช้ PAT/service account สำหรับ backend แยกจาก Keycloak browser token

## 8. MinIO

Backend ควรส่งข้อมูลภาพให้ frontend ในรูปแบบนี้:

```json
{
  "object_key": "ptt-demo/images/008835.jpg",
  "url": "https://minio.example/presigned-url",
  "expires_at": "2026-09-22T12:00:00Z"
}
```

แนวทางนี้ทำให้:

- ภาพต้นฉบับอยู่ที่ MinIO เพียงชุดเดียว
- backend ไม่ต้องรับส่งไฟล์ขนาดใหญ่ทุกครั้ง
- presigned URL หมดอายุได้
- annotation database ไม่เก็บไฟล์ภาพซ้ำ

## 9. การฝัง LSF ใน React

โครงสร้างเชิงแนวคิด:

```jsx
function AnnotationPage({ sessionId }) {
  const [session, setSession] = useState(null);

  useEffect(() => {
    fetch(`/api/annotation-sessions/${sessionId}`, {
      headers: { Authorization: `Bearer ${keycloak.token}` },
    })
      .then((response) => response.json())
      .then(setSession);
  }, [sessionId]);

  if (!session) return <div>Loading...</div>;

  return (
    <LabelStudioFrontend
      image={session.image.url}
      labels={session.labels}
      annotations={session.annotations}
      onChange={(annotations) => {
        // update local editor state
      }}
      onSave={(annotations) =>
        fetch(`/api/annotation-sessions/${sessionId}/annotations`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${keycloak.token}`,
            "Content-Type": "application/json",
            "If-Match": `"revision-${session.revision}"`,
          },
          body: JSON.stringify({
            base_revision: session.revision,
            annotations,
          }),
        })
      }
    />
  );
}
```

ชื่อ props และ callback ต้องตรวจให้ตรงกับ LSF version ที่ติดตั้งจริง ตัวอย่างนี้แสดงเฉพาะแนวทางการแยกความรับผิดชอบระหว่าง editor กับ backend

## 10. Validation ที่ backend ต้องทำ

- label ต้องอยู่ใน project schema
- `points` ต้องตรงกับชนิด shape
- พิกัดต้องอยู่ภายใน `width` และ `height`
- ตรวจว่า image checksum ตรงกับ revision
- ตรวจผู้ใช้และ assignment
- ตรวจ revision ป้องกันการเขียนทับ
- normalize coordinate ให้ใช้รูปแบบเดียวทั้งระบบ
- reject payload ที่ใหญ่หรือมี field ที่ไม่อนุญาต

## 11. แผน PoC

เริ่มจาก 20 ภาพและ 3–5 labels:

1. ฝัง LSF ในหน้า React หนึ่งหน้า
2. โหลด presigned URL จาก MinIO
3. แสดง label จาก backend
4. สร้าง rectangle และ polygon
5. save/reload annotation
6. ทดสอบผู้ใช้สองคนแก้ภาพเดียวกัน
7. submit และ review
8. อ่านข้อมูลจาก DB แล้วสร้าง YOLO/COCO export
9. ตรวจว่าภาพไม่ถูก copy เข้า database หรือ frontend build

เกณฑ์ผ่าน PoC:

- ผู้ใช้ login ผ่าน Keycloak ได้
- backend แยกสิทธิ์ได้ถูกต้อง
- ภาพอ่านจาก MinIO ด้วย URL อายุสั้น
- annotation reload แล้วตำแหน่งไม่เปลี่ยน
- revision conflict ไม่ทำให้ข้อมูลหาย
- ผลลัพธ์แปลงเป็น format training ได้

## 12. ข้อดีและความเสี่ยง

### ข้อดี

- ประสบการณ์ผู้ใช้เป็นของ platform เอง
- ใช้ database, Keycloak และ MinIO เดิม
- ไม่ต้องให้ผู้ใช้เปิด CVAT แยก
- กำหนด API และ data contract ได้เอง

### ความเสี่ยง

- ต้องพัฒนา workflow ที่ CVAT มีให้แล้ว
- ต้องดูแล LSF version และ dependency
- ต้องออกแบบ autosave, locking, review และ audit เอง
- ต้องทดสอบการรองรับ annotation shape ที่ต้องใช้จริง

## 13. ข้อเสนอแนะสุดท้าย

ให้ใช้ LSF เป็นทางเลือกสำหรับ **custom annotation page** เมื่อ product ต้องการควบคุม UI และ workflow เอง หากเป้าหมายหลักคือให้ทีม annotate ได้เร็วและมี review/assignment/issue พร้อมใช้ ให้ใช้ CVAT ต่อไปแล้วเชื่อมผ่าน REST API/SDK

แนวทางที่ปลอดภัยคือทำ LSF เป็น PoC แยก โดยไม่ลบ workflow CVAT เดิม จนกว่าจะพิสูจน์ได้ว่าการพัฒนา review, concurrency, audit และ export มีต้นทุนต่ำกว่าการใช้ CVAT
