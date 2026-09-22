# CVAT + AI Platform — คู่มือภาษาไทย

[สารบัญเอกสารสำหรับ Developer](docs/00_DOCUMENT-INDEX-TH.md) · [สารบัญไฟล์อัตโนมัติ](DOCS-INDEX.md) · [วิธีเพิ่มเอกสารและอัปเดตสารบัญ](CONTRIBUTING.md)

## เริ่มอ่านตามหน้าที่

**ทดลองเองบนเครื่อง luke:** [คำสั่งทีละขั้นพร้อม dataset path จริง](docs/08_CVAT-HANDS-ON-LOCAL-DATASET-TH.md)

**ทดลองผ่าน Postman:** [Postman Workflow Guide](docs/09_CVAT-POSTMAN-WORKFLOW-GUIDE-TH.md) และ [Collection ที่ import ได้](examples/postman/CVAT-API-Workflow.postman_collection.json)


**เริ่มลงมือเรียก API แบบง่าย โดยผู้ใช้สิทธิ์เท่ากัน:** [API Workflow Quickstart พร้อม curl](docs/07_CVAT-API-WORKFLOW-QUICKSTART-TH.md)

**อ้างอิง API แบบ interactive:** [CVAT API Docs](https://app.cvat.ai/api/docs/) หรือใช้ `http://localhost:8080/api/docs/` เมื่อทดสอบ CVAT local

**เอกสาร CVAT ทางการทั้งหมด:** [CVAT Documentation](https://docs.cvat.ai/docs/)


1. Backend Developer: [MinIO → CVAT → Platform Database](docs/03_CVAT-MINIO-BACKEND-END-TO-END-TH.md)
2. ออกแบบผลิตภัณฑ์: [AI Platform Architecture](docs/01_AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md)
3. ออกแบบความสอดคล้องของบริการ: [Integration Contract](docs/04_CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md)
4. ออกแบบคิว/QA: [Developer Workflow](docs/05_CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md)
5. Annotator/Reviewer/Coordinator: [คู่มือปฏิบัติการ](docs/06_CVAT-WORKFLOW-OPERATIONS-GUIDE-TH.md)
6. Dashboard/reporting: [Job Status API](docs/11_CVAT-JOB-STATUS-API-GUIDE-TH.md)
7. ทดลองเว็บฝัง CVAT: [วิธีรัน Prototype](prototype/README.md)
8. เปรียบเทียบฟีเจอร์หน้า Annotate: [Roboflow vs CVAT vs Label Studio](docs/18_ANNOTATION-EDITOR-FEATURE-MATRIX-TH.md)

## แนวทางปัจจุบัน

Platform เชื่อม CVAT ผ่าน REST API/SDK; Webhook เป็นสัญญาณให้ดึงข้อมูลล่าสุดร่วมกับ reconciliation MinIO เก็บต้นฉบับ และ Platform เก็บ mapping/metadata กับ annotation revision ตามความต้องการ การฝึกอ้าง release ที่ตรวจแล้ว โดย export package เมื่อ consumer จำเป็นต้องใช้

ฐานข้อมูล CVAT เป็นข้อมูลภายในของบริการ อ่านเพื่อ DBA/monitoring ได้ แต่ไม่เขียน SQL แทน API การใช้ MinIO/Remote URL ไม่รับประกัน zero-copy และ browser SSO ไม่ทำให้ Keycloak token ใช้แทน CVAT PAT อัตโนมัติ

## สถานะที่บันทึกไว้

ทบทวนเอกสาร 22 กันยายน 2026 ไม่ได้ตรวจสถานะระบบสดใหม่ในวันทบทวน

- ทดลอง CVAT 2.75.1 วันที่ 16–17 กันยายน: ptt-demo / ptt2 (#3) / train (#2) / Job #2 มี 20 ภาพ ตรวจรับแล้ว ผล export 241 annotations / 26 classes
- มี prototype local proxy ที่ http://localhost:5175/platform/ อ่าน API และส่งคำสั่ง workflow จริง ใช้ CVAT session ดูขอบเขตการทดสอบใน README ของ prototype
- MinIO integration, durable webhook inbox, Platform release service และ Keycloak SSO ยังเป็นแบบออกแบบ ไม่ได้ยืนยันว่าติดตั้งครบวงจร

## ฐานข้อมูลและหลักฐานย้อนหลัง

- [Database monitoring](docs/12_CVAT-DATABASE-SCHEMA-MONITORING-GUIDE-TH.md)
- [Schema snapshot วันที่ 17 กันยายน](docs/13_CVAT-DATABASE-SCHEMA-REFERENCE-TH.md) ไม่ใช่ schema สด
- [ตัวอย่างรายงาน](examples/reports/README.md) เป็น snapshot ที่ปรับสำหรับเผยแพร่ ไม่ใช่ live status
- [สารบัญเอกสารสำหรับ Developer](docs/00_DOCUMENT-INDEX-TH.md)
- [Q&A ประวัติการทดลอง](docs/17_CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md)

## โครงสร้าง

```text
docs/                คู่มือที่ดูแลต่อเนื่องและ reference
docs/archive/        ประวัติการทดลอง
prototype/           เว็บทดลอง + proxy และคู่มือรัน
examples/reports/    รายงานตัวอย่าง
scripts/             ตัวสร้างสารบัญ
DOCS-INDEX.md        สารบัญที่สร้างอัตโนมัติ
CONTRIBUTING.md      วิธีดูแลเอกสาร
```

ชื่อผู้ใช้ IDs และ paths เป็นตัวอย่าง ต้องตรวจสิทธิ์และ schema กับ instance จริงก่อนใช้ เอกสารนี้เป็นคู่มือโครงการ ไม่ใช่เอกสารทางการของ CVAT
