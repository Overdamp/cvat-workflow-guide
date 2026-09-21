# สารบัญคู่มือ CVAT + AI Platform

สร้างจากไฟล์ Markdown ใน repository ด้วย `python3 scripts/update_docs_index.py` ห้ามแก้ตารางด้วยมือ

เริ่มพัฒนา: README → คู่มือ Backend End-to-End → Workflow/API → Prototype ตามหน้าที่ของผู้อ่าน

ไฟล์ใหม่จะปรากฏโดยอัตโนมัติ ไม่ต้องเพิ่มรายการชื่อไฟล์ในสคริปต์; กลุ่มเอกสารอื่นใช้สำหรับไฟล์ที่ยังไม่ได้ระบุหมวด

## คู่มือหลัก

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [CVAT + AI Platform — คู่มือภาษาไทย](README.md) | `README.md` | จุดเริ่มต้นและสถานะโครงการ |
| [แนวทางออกแบบ AI Platform ที่ใช้ CVAT เป็น Annotation Service](docs/AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md) | `docs/AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md` | ภาพรวมผลิตภัณฑ์และสถาปัตยกรรมเป้าหมาย |
| [คู่มือ Backend: MinIO → CVAT → Annotation/QA → Platform Database](docs/CVAT-MINIO-BACKEND-END-TO-END-TH.md) | `docs/CVAT-MINIO-BACKEND-END-TO-END-TH.md` | ข้อกำหนดหลักสำหรับ Backend; MinIO/API/SDK/Webhook/DB/Auth |
| [แนวทางเชื่อม CVAT เข้ากับแพลตฟอร์มอุตสาหกรรม](docs/CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md) | `docs/CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md` | Integration contract และความสอดคล้องระหว่างบริการ |

## คู่มือใช้งานและ API

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [API Workflow แบบง่าย: สั่ง CVAT ตั้งแต่สร้างงานจนรับผล](docs/CVAT-API-WORKFLOW-QUICKSTART-TH.md) | `docs/CVAT-API-WORKFLOW-QUICKSTART-TH.md` | คำสั่ง curl ตั้งแต่สร้าง Project จนดึงผล; PoC สิทธิ์เท่ากัน |
| [CVAT Developer Guideline: ระบบจัดคิว Annotation, QA และ Dataset Release](docs/CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md) | `docs/CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md` | กติกา workflow/queue; schema เป็นข้อเสนอ |
| [ทดลอง CVAT API ทีละขั้นด้วยภาพจาก dataset ในเครื่อง](docs/CVAT-HANDS-ON-LOCAL-DATASET-TH.md) | `docs/CVAT-HANDS-ON-LOCAL-DATASET-TH.md` | ทดลองทีละขั้นด้วยภาพจริงจาก dataset ในเครื่อง luke |
| [เรียก CVAT API เพื่อดูสถานะงานและคิว QA](docs/CVAT-JOB-STATUS-API-GUIDE-TH.md) | `docs/CVAT-JOB-STATUS-API-GUIDE-TH.md` | อ่านสถานะและสร้างรายงานผ่าน API |
| [คู่มือปฏิบัติการ CVAT: Workflow Annotation และ QA](docs/CVAT-WORKFLOW-OPERATIONS-GUIDE-TH.md) | `docs/CVAT-WORKFLOW-OPERATIONS-GUIDE-TH.md` | ขั้นตอนของ Annotator/Reviewer/Coordinator |

## ฐานข้อมูล

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [CVAT Database Schema และแนวทาง Monitoring สำหรับ Developer](docs/CVAT-DATABASE-SCHEMA-MONITORING-GUIDE-TH.md) | `docs/CVAT-DATABASE-SCHEMA-MONITORING-GUIDE-TH.md` | Reference/monitoring; ตรวจวันที่ snapshot ก่อนใช้ |
| [CVAT PostgreSQL Schema Reference](docs/CVAT-DATABASE-SCHEMA-REFERENCE-TH.md) | `docs/CVAT-DATABASE-SCHEMA-REFERENCE-TH.md` | Reference/monitoring; ตรวจวันที่ snapshot ก่อนใช้ |

## ระบบทดลองและตัวอย่าง

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [ตัวอย่างรายงานจาก CVAT Workflow](examples/reports/README.md) | `examples/reports/README.md` | ตรวจข้อจำกัดและผลทดสอบในเอกสาร |
| [Platform ทดลองเชื่อม CVAT จริง](prototype/README.md) | `prototype/README.md` | ตรวจข้อจำกัดและผลทดสอบในเอกสาร |

## เอกสารประวัติ / ลิงก์ย้าย

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [ย้ายเอกสาร Q&A แล้ว](docs/CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md) | `docs/CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md` | ประวัติ / ทางไปเอกสารที่ย้ายแล้ว ไม่ใช่ implementation contract |
| [คู่มือ Q&A: CVAT และแนวทางออกแบบระบบจัดการงาน Annotation / QA](docs/archive/CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md) | `docs/archive/CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md` | ประวัติ / ทางไปเอกสารที่ย้ายแล้ว ไม่ใช่ implementation contract |

## เอกสารอื่นและไฟล์ใหม่

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [ดูแลและเพิ่มคู่มือ](CONTRIBUTING.md) | `CONTRIBUTING.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |

