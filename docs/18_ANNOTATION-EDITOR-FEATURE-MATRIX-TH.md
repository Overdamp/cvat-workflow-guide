# ตารางเปรียบเทียบเครื่องมือในหน้า Annotate: Roboflow, CVAT และ Label Studio

เอกสารนี้ใช้ **Roboflow Annotate เป็น baseline** เพื่อดูว่าฟีเจอร์ที่ผู้ใช้เห็นในหน้า annotation มีอยู่ใน CVAT และ Label Studio อย่างไร เหมาะสำหรับใช้ตัดสินใจในที่ประชุมและคุยกับทีม backend/frontend

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

## วิธีอ่านตาราง

| สัญลักษณ์ | ความหมาย |
|---|---|
| ✅ | มีในตัวและใช้งานได้โดยตรง |
| ◐ | มี แต่ต้องตั้งค่า, ใช้ปลั๊กอิน/โมเดล, หรือทำ workflow เพิ่ม |
| △ | ทำได้ด้วยการพัฒนา frontend/integration เอง |
| — | ไม่มีในตัว หรือไม่ใช่ความสามารถหลักของเครื่องมือ |

คำว่า “มี” หมายถึงมีความสามารถในระบบ ไม่ได้หมายความว่าหน้าตาและ shortcut จะเหมือน Roboflow ทุกจุด ควรทดสอบกับเวอร์ชันที่ deploy จริงก่อนสรุป requirement

## 1. เครื่องมือและการวาด annotation ในหน้า Annotate

| ความสามารถที่อ้างอิงจาก Roboflow | Roboflow | CVAT | Label Studio | หมายเหตุสำหรับโครงการ |
|---|---:|---:|---:|---|
| เลือก/ย้าย/ปรับขนาดวัตถุ | ✅ | ✅ | ✅ | ฟังก์ชันพื้นฐานของทั้งสามระบบ |
| Bounding box / rectangle | ✅ | ✅ | ✅ | ใช้เป็นรูปแบบหลักของ object detection |
| Polygon | ✅ | ✅ | ✅ | ใช้กับวัตถุรูปร่างไม่เป็นสี่เหลี่ยม |
| Brush mask / segmentation mask | ✅ | ✅ | ✅ | CVAT รองรับการทำ mask และการแก้รูปร่างใน editor |
| Smart Polygon / กึ่งอัตโนมัติ | ✅ | ◐ | ◐ | ต้องต่อ model/auto-annotation เช่น SAM หรือบริการ inference |
| Ellipse | —/◐ | ✅ | ✅ | Roboflow ไม่ใช่รูปแบบหลักที่ใช้ทั่วไปใน flow นี้ |
| Point / keypoint | ✅ | ✅ | ✅ | ใช้กับ pose, จุดวัด หรือจุดอ้างอิง |
| Skeleton / กำหนดลำดับ keypoint | ◐ | ✅ | ◐ | CVAT มี skeleton labels; Label Studio ทำได้ผ่าน labeling config |
| Polyline / line | ◐ | ✅ | ✅ | เหมาะกับท่อ สาย หรือแนวเส้น |
| Cuboid / 3D box | ◐ | ✅ | ◐ | ต้องตรวจความต้องการ 3D จริงก่อนเลือกใช้ |
| Image classification / tag | ✅ | ✅ | ✅ | CVAT ใช้ tags/labels; Label Studio ใช้ choices/classification |
| Attribute ต่อวัตถุ | ✅ | ✅ | ✅ | เช่น สี สภาพ หรือค่าความผิดปกติ |
| Relation ระหว่างวัตถุ | ◐ | ✅ | ✅ | เช่น “เชื่อมต่อกับ”, “อยู่บน” |
| ตัวเลือก class และสี label | ✅ | ✅ | ✅ | schema ต้องตรงกันระหว่าง backend, CVAT และฐานข้อมูลหลัก |
| Zoom / pan | ✅ | ✅ | ✅ | จำเป็นกับภาพความละเอียดสูงจาก MinIO |
| Rotate ภาพหรือวัตถุ | ✅ | ✅ | ✅ | ตรวจสอบผลต่อพิกัดก่อนนำไป train |
| Undo / redo | ✅ | ✅ | ✅ | มีใน editor แต่ shortcut อาจต่างกัน |
| Copy / paste / duplicate | ✅ | ✅ | ◐ | ความสามารถขึ้นกับ editor/configuration |
| Repeat label / ทำซ้ำแบบเร็ว | ✅ | ✅ | ◐ | Roboflow มีเครื่องมือช่วยทำงานซ้ำ; LS ต้องออกแบบ config/UX เพิ่มบางส่วน |
| Keyboard shortcuts | ✅ | ✅ | ✅ | ต้องทำคู่มือ shortcut แยกตามเครื่องมือ |
| แสดงชื่อไฟล์และขนาดภาพ | ✅ | ✅ | ✅ | ใช้ตรวจสอบ mapping กับ `image_id` ใน platform |
| หลายภาพในงานเดียว | ✅ | ✅ | ✅ | CVAT ใช้ task/job; LS ใช้ project/tasks |
| วิดีโอและ frame navigation | ✅ | ✅ | ✅ | CVAT เด่นเรื่อง video/frame job |
| Tracking / interpolation | ◐ | ✅ | ◐ | สำคัญเมื่อมี video; LS ต้องเลือก template/config ให้เหมาะ |
| Autosave / บันทึกระหว่างทำ | ✅ | ✅ | ✅ | ต้องกำหนด policy เรื่อง retry และสถานะงานใน backend |
| Skip / flag image | ✅ | ✅ | ◐ | ถ้าไม่มี native ให้เก็บสถานะใน platform backend |
| แสดง prediction overlay | ✅ | ✅ | ✅ | ใช้ pre-annotation/model-assisted labeling |
| Model-assisted labeling | ✅ | ✅ | ◐ | CVAT มี auto-annotation; LS ต่อ ML backend/model ได้ |
| SAM/segmentation assist | ✅ | ◐ | ◐ | ต้อง deploy model และกำหนดสิทธิ์/ต้นทุน inference |
| Confidence score | ✅ | ◐ | ◐ | มาจาก prediction/model ไม่ใช่ค่าที่ annotator วาดเอง |

## 2. Workflow ทีมและการตรวจคุณภาพ

| ความสามารถ | Roboflow | CVAT | Label Studio | สิ่งที่ต้องออกแบบใน platform |
|---|---:|---:|---:|---|
| Project / dataset | ✅ | ✅ | ✅ | ใช้ `project_id`, dataset/release ID ของระบบหลักเป็นตัวอ้างอิง |
| Task / job แบ่งงาน | ✅ | ✅ | ✅ | CVAT แบ่ง task เป็น jobs และกำหนด assignee ได้ |
| Batch | ✅ | ✅/◐ | ◐ | CVAT ใช้ task/jobs; batching อัตโนมัติต้องทำ orchestration เพิ่ม |
| Assign งานให้ผู้ใช้ | ✅ | ✅ | ✅ | MVP นี้ให้สิทธิ์เท่ากันได้ แต่ backend ควรเก็บ assignee/status |
| คำสั่งงาน/annotation instructions | ✅ | ✅ | ✅ | เก็บ guideline version ใน platform เพื่อ audit |
| Progress ต่อคน/งาน | ✅ | ✅ | ✅ | ดึง job/task status ผ่าน REST API แล้วสรุปใน dashboard |
| Comment / issue | ✅ | ✅ | ✅ | เชื่อม issue ไปยัง `task_id`, `job_id`, `frame`, `shape_id` |
| ส่งกลับแก้ไข (rework) | ✅ | ✅ | ✅/◐ | กำหนด state เช่น `in_progress`, `review`, `rework`, `approved` |
| Approve / reject | ✅ | ✅ | ◐ | CVAT มี review workflow; LS ต้องทำด้วย project workflow หรือ platform layer |
| Timeline / activity history | ✅ | ✅ | ◐ | เก็บ audit event ใน backend เพิ่ม อย่าอ่าน DB ภายใน CVAT โดยตรง |
| Revert / version history | ✅ | ✅/◐ | ◐ | ต้องกำหนด retention และวิธี restore annotation ที่ชัดเจน |
| Consensus / หลายคนทำภาพเดียวกัน | ✅ | ✅ | ◐ | ใช้เมื่อต้องการวัด agreement; อาจต้องทำ aggregation เอง |
| Quality metrics / QA | ✅ | ✅ | ✅/◐ | ควรกำหนด metric ที่ platform ไม่ผูกกับ UI ของเครื่องมือ |
| Dataset version / release | ✅ | ✅/◐ | ◐ | Roboflow เด่นด้าน release; CVAT/LS ควรให้ backend สร้าง immutable release |
| Queue / ลำดับงาน | ✅ | ◐ | ◐ | จัดคิวที่ backend แล้วส่งงานเข้า CVAT/LS ตามลำดับ |

## 3. API, storage, auth และการนำไปต่อกับ platform

| ความสามารถ | Roboflow | CVAT | Label Studio | แนวทางของโครงการนี้ |
|---|---:|---:|---:|---|
| REST API | ✅ | ✅ | ✅ | ใช้สร้าง project/task/job, อ่านสถานะ และดึง annotations |
| OpenAPI/Swagger | ✅/◐ | ✅ | ✅/◐ | CVAT เปิดที่ `/api/docs/` และ `/api/swagger`; ใช้ตรวจ schema ก่อนเขียน client |
| Python SDK | ✅/◐ | ✅ | ✅/◐ | CVAT มี `cvat-sdk`; ใช้ใน worker/backend ได้ |
| CLI | ✅ | ✅ | ◐ | ใช้สำหรับ manual export/debug ไม่ใช่ data path หลัก |
| Webhook/event | ✅ | ✅ | ✅/◐ | ใช้เป็นสัญญาณว่างานเปลี่ยนสถานะ แล้ว backend GET ผลลัพธ์ล่าสุด |
| S3/MinIO/cloud storage | ✅ | ✅ | ✅ | ให้ backend เป็นเจ้าของ object และส่ง URL/remote storage ตาม policy |
| Presigned URL | ✅ | ◐ | ◐ | ต้องทดสอบอายุ URL และการ cache/download ของเครื่องมือจริง |
| Self-hosted | —/◐ | ✅ | ✅ | CVAT Community และ Label Studio OSS เหมาะกับข้อมูลโรงงานที่ต้องควบคุมเอง |
| ฝัง editor ใน platform | ◐ | ◐ | △ | CVAT/LS ปกติเปิดเป็นบริการแยก; การ iframe ต้องจัดการ auth, CSP และ reverse proxy |
| OIDC / Keycloak browser SSO | ✅/◐ | ◐ | ✅/◐ | ตั้ง SSO สำหรับผู้ใช้แยกจาก service API token; ต้องทดสอบ version/config จริง |
| Service account / PAT สำหรับ backend | ✅ | ✅ | ✅/◐ | เก็บ secret ใน secret manager; ห้ามใส่ token ใน repo หรือ URL |
| JSON annotation API | ✅ | ✅ | ✅ | production path ควรดึงผลผ่าน API แล้ว normalize ใน backend |
| COCO / YOLO export | ✅ | ✅ | ✅ | ใช้เป็น export/training artifact หรือ manual fallback |
| Training pipeline ในตัว | ✅ | — | — | CVAT/LS ทำ annotation; training/inference อยู่ใน platform ของเรา |
| Database ของเครื่องมือ | managed | PostgreSQL | PostgreSQL | ไม่เขียนตรงเข้า DB ภายใน; ใช้ API/Webhook แล้วเก็บ final result ใน DB หลัก |

## 4. สรุปตาม baseline ของ Roboflow

Roboflow รวม annotation editor, assignment, QA, dataset versioning และ training workflow ไว้ในผลิตภัณฑ์เดียว จึงเหมาะเป็น **รายการความสามารถที่ควรมีในผลิตภัณฑ์ปลายทาง** แต่ไม่ได้แปลว่าต้องย้ายทุกอย่างมาอยู่ใน CVAT หรือ Label Studio

สำหรับสถาปัตยกรรมของโครงการนี้ให้แบ่งความรับผิดชอบดังนี้

| ส่วน | ผู้รับผิดชอบ |
|---|---|
| วาดและแก้ annotation | CVAT เป็นตัวเลือกหลัก; Label Studio เป็นทางเลือกเมื่อ schema/custom UI สำคัญกว่า |
| คิว, assignment, สิทธิ์, dashboard | Backend/platform ของเรา |
| รูปต้นฉบับและ metadata | MinIO + database หลักของเรา |
| สถานะงานและ audit | Backend ของเรา ดึง event/API จากเครื่องมือ |
| ผล annotation ที่ผ่านการตรวจ | Database หลักของเรา โดยผูก `image_id`, `task_id`, `job_id`, `tool`, `schema_version` |
| Training/release | Pipeline ของเรา; export COCO/YOLO เป็น artifact ตาม version |
| Login ผู้ใช้ | Keycloak/OIDC สำหรับ browser; service account/PAT สำหรับ backend-to-tool |

## 5. คำแนะนำสำหรับการตัดสินใจ

### เลือก CVAT เมื่อ

- ต้องการ self-hosted/open-source annotation engine ที่มี object, video, tracking, review และ API ครบ
- ทีม backend พร้อมสร้าง queue, dashboard, release และ policy ให้เป็นของ platform เอง
- ต้องการลด vendor lock-in และเก็บข้อมูลโรงงานไว้ในระบบของเรา

### เลือก Label Studio เมื่อ

- ต้องการ labeling config ที่ปรับแต่งได้มาก และมีงาน image/text/audio/multimodal ในระบบเดียว
- ต้องการทำ frontend workflow เฉพาะทางโดยใช้ labeling interface เป็นฐาน
- ยอมรับว่าคิว, QA, release และ integration หลายส่วนต้องประกอบเพิ่มใน platform

### ใช้ Roboflow เป็น benchmark เมื่อ

- ต้องการกำหนดรายการ UX ที่ดี เช่น Smart Assist, progress, issue/rework, release และ training handoff
- ต้องการเทียบ effort ที่ต้องพัฒนาเพิ่มใน CVAT/Label Studio
- ไม่ได้หมายความว่าต้องนำข้อมูล production ไปเก็บซ้ำในบริการ managed

**ข้อเสนอสำหรับ PoC ปัจจุบัน:** ใช้ CVAT เป็น annotation engine, ให้ backend จัดการคิวและสถานะโดยทุกคนมีสิทธิ์เท่ากันก่อน, ใช้ MinIO เป็น source ของภาพ, ใช้ REST API/SDK เป็นทางหลัก และเก็บผลสุดท้ายใน database ของ platform ส่วน export ZIP/COCO/YOLO ให้เป็น manual fallback สำหรับ debug หรือ release เท่านั้น

## แหล่งอ้างอิงทางการ

- [Roboflow Annotate](https://docs.roboflow.com/roboflow/roboflow-jp/anotto/use-roboflow-annotate)
- [Roboflow team collaboration](https://docs.roboflow.com/annotate/team-collaboration)
- [Roboflow supported annotation formats](https://docs.roboflow.com/annotate/annotate-upload-data)
- [CVAT Documentation](https://docs.cvat.ai/docs/)
- [CVAT API documentation](https://app.cvat.ai/api/docs/)
- [Label Studio labeling guide](https://labelstud.io/guide/labeling)
- [Label Studio setup and projects](https://labelstud.io/guide/setup)
- [Label Studio export](https://labelstud.io/guide/export)
