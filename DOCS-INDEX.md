# สารบัญคู่มือ CVAT + AI Platform

สร้างจากไฟล์ Markdown ใน repository ด้วย `python3 scripts/update_docs_index.py` ห้ามแก้ตารางด้วยมือ

เริ่มพัฒนา: README → คู่มือ Backend End-to-End → Workflow/API → Prototype ตามหน้าที่ของผู้อ่าน

ไฟล์ใหม่จะปรากฏโดยอัตโนมัติ ไม่ต้องเพิ่มรายการชื่อไฟล์ในสคริปต์; กลุ่มเอกสารอื่นใช้สำหรับไฟล์ที่ยังไม่ได้ระบุหมวด

## คู่มือหลัก

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [CVAT + AI Platform — คู่มือภาษาไทย](README.md) | `README.md` | จุดเริ่มต้นและสถานะโครงการ |
| [แนวทางออกแบบ AI Platform ที่ใช้ CVAT เป็น Annotation Service](docs/01_AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md) | `docs/01_AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md` | ภาพรวมผลิตภัณฑ์และสถาปัตยกรรมเป้าหมาย |
| [คู่มือ Backend: MinIO → CVAT → Annotation/QA → Platform Database](docs/03_CVAT-MINIO-BACKEND-END-TO-END-TH.md) | `docs/03_CVAT-MINIO-BACKEND-END-TO-END-TH.md` | ข้อกำหนดหลักสำหรับ Backend; MinIO/API/SDK/Webhook/DB/Auth |
| [แนวทางเชื่อม CVAT เข้ากับแพลตฟอร์มอุตสาหกรรม](docs/04_CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md) | `docs/04_CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md` | Integration contract และความสอดคล้องระหว่างบริการ |
| [Backend Developer Handoff: เชื่อม Platform กับ CVAT](docs/16_BACKEND-DEVELOPER-HANDOFF-TH.md) | `docs/16_BACKEND-DEVELOPER-HANDOFF-TH.md` | เอกสารส่งต่องาน Backend; API/DB/Auth/MinIO/Webhook |
| [ตารางเปรียบเทียบเครื่องมือในหน้า Annotate: Roboflow, CVAT และ Label Studio](docs/18_ANNOTATION-EDITOR-FEATURE-MATRIX-TH.md) | `docs/18_ANNOTATION-EDITOR-FEATURE-MATRIX-TH.md` | เทียบฟีเจอร์หน้า annotate โดยใช้ Roboflow เป็น baseline |

## คู่มือใช้งานและ API

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [CVAT Developer Guideline: ระบบจัดคิว Annotation, QA และ Dataset Release](docs/05_CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md) | `docs/05_CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md` | กติกา workflow/queue; schema เป็นข้อเสนอ |
| [คู่มือปฏิบัติการ CVAT: Workflow Annotation และ QA](docs/06_CVAT-WORKFLOW-OPERATIONS-GUIDE-TH.md) | `docs/06_CVAT-WORKFLOW-OPERATIONS-GUIDE-TH.md` | ขั้นตอนของ Annotator/Reviewer/Coordinator |
| [API Workflow แบบง่าย: สั่ง CVAT ตั้งแต่สร้างงานจนรับผล](docs/07_CVAT-API-WORKFLOW-QUICKSTART-TH.md) | `docs/07_CVAT-API-WORKFLOW-QUICKSTART-TH.md` | คำสั่ง curl ตั้งแต่สร้าง Project จนดึงผล; PoC สิทธิ์เท่ากัน |
| [ทดลอง CVAT API ทีละขั้นด้วยภาพจาก dataset ในเครื่อง](docs/08_CVAT-HANDS-ON-LOCAL-DATASET-TH.md) | `docs/08_CVAT-HANDS-ON-LOCAL-DATASET-TH.md` | ทดลองทีละขั้นด้วยภาพจริงจาก dataset ในเครื่อง luke |
| [ทดลองสั่ง CVAT ผ่าน Postman](docs/09_CVAT-POSTMAN-WORKFLOW-GUIDE-TH.md) | `docs/09_CVAT-POSTMAN-WORKFLOW-GUIDE-TH.md` | ทดลอง REST API ผ่าน Postman แบบเรียงลำดับ |
| [เรียก CVAT API เพื่อดูสถานะงานและคิว QA](docs/11_CVAT-JOB-STATUS-API-GUIDE-TH.md) | `docs/11_CVAT-JOB-STATUS-API-GUIDE-TH.md` | อ่านสถานะและสร้างรายงานผ่าน API |

## ระบบทดลองและตัวอย่าง

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [Sanitized REST API output example](examples/api-results/README.md) | `examples/api-results/README.md` | ตรวจข้อจำกัดและผลทดสอบในเอกสาร |
| [ตัวอย่างรายงานจาก CVAT Workflow](examples/reports/README.md) | `examples/reports/README.md` | ตรวจข้อจำกัดและผลทดสอบในเอกสาร |
| [Platform ทดลองเชื่อม CVAT จริง](prototype/README.md) | `prototype/README.md` | ตรวจข้อจำกัดและผลทดสอบในเอกสาร |

## เอกสารประวัติ / ลิงก์ย้าย

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [คู่มือ Q&A: CVAT และแนวทางออกแบบระบบจัดการงาน Annotation / QA](docs/archive/CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md) | `docs/archive/CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md` | ประวัติ / ทางไปเอกสารที่ย้ายแล้ว ไม่ใช่ implementation contract |

## เอกสารอื่นและไฟล์ใหม่

| เอกสาร | ไฟล์ | การใช้งาน |
|---|---|---|
| [ดูแลและเพิ่มคู่มือ](CONTRIBUTING.md) | `CONTRIBUTING.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |
| [สารบัญเอกสารสำหรับ Developer](docs/00_DOCUMENT-INDEX-TH.md) | `docs/00_DOCUMENT-INDEX-TH.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |
| [ตารางตัดสินใจเลือก Annotation Tool](docs/02_ANNOTATION-TOOL-SELECTION-MATRIX-TH.md) | `docs/02_ANNOTATION-TOOL-SELECTION-MATRIX-TH.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |
| [ทดลอง Python SDK ด้วย dataset เดิม](docs/10_CVAT-SDK-HANDS-ON-TH.md) | `docs/10_CVAT-SDK-HANDS-ON-TH.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |
| [CVAT Database Schema และแนวทาง Monitoring สำหรับ Developer](docs/12_CVAT-DATABASE-SCHEMA-MONITORING-GUIDE-TH.md) | `docs/12_CVAT-DATABASE-SCHEMA-MONITORING-GUIDE-TH.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |
| [CVAT PostgreSQL Schema Reference](docs/13_CVAT-DATABASE-SCHEMA-REFERENCE-TH.md) | `docs/13_CVAT-DATABASE-SCHEMA-REFERENCE-TH.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |
| [ทางเลือกเมื่อ Backend ทำหน้า Annotation เอง](docs/14_CUSTOM-ANNOTATION-FRONTEND-OPTIONS-TH.md) | `docs/14_CUSTOM-ANNOTATION-FRONTEND-OPTIONS-TH.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |
| [แนวทางเลือก Label Studio Frontend (LSF)](docs/15_LABEL-STUDIO-FRONTEND-INTEGRATION-GUIDE-TH.md) | `docs/15_LABEL-STUDIO-FRONTEND-INTEGRATION-GUIDE-TH.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |
| [ย้ายเอกสาร Q&A แล้ว](docs/17_CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md) | `docs/17_CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md` | ตรวจขอบเขตและสถานะในไฟล์; จัดกลุ่มเพิ่มได้ในสคริปต์ |

