# CVAT Workflow Guide — ภาษาไทย

คู่มือการใช้และเชื่อมต่อ CVAT สำหรับงาน Annotation → QA → แก้ไข → ตรวจรับ → Export และแนวทางออกแบบ Workflow Platform

เอกสารอ้างอิงจากการทดลองจริงชุดภาพ 20 ภาพใน CVAT พร้อมการเปิด Issue, ส่งกลับแก้, ตรวจซ้ำ และตรวจสอบ export โดยรายงานตัวอย่างมี 241 annotations และ 26 class definitions ปรับให้สอดคล้องกับบริบทปัจจุบัน: CVAT 2.75.1, Docker Compose, Organization `ptt-demo`, Project `ptt2` (#3), Task `train` (#2), Job #2 และแนวทางเชื่อม Platform ผ่าน REST API/Webhook

## เริ่มอ่าน

สำหรับ Backend Developer ที่เชื่อม MinIO, API/SDK, Webhook, Keycloak และฐานข้อมูล: เริ่มที่ [คู่มือ End-to-End ฉบับ 18 กันยายน 2026](docs/CVAT-MINIO-BACKEND-END-TO-END-TH.md) ซึ่งแก้ข้อเข้าใจผิดเรื่อง remote storage, webhook payload และ token authentication จากบทสนทนาก่อนหน้า

| ผู้อ่าน / เป้าหมาย | เอกสาร |
|---|---|
| คนทำ Annotation, Reviewer และ Coordinator | [คู่มือปฏิบัติการ](docs/CVAT-WORKFLOW-OPERATIONS-GUIDE-TH.md) |
| ต้องการเข้าใจคำศัพท์และปัญหาที่พบจริง | [Q&A และแนวทางออกแบบระบบ](docs/CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md) |
| Developer ออกแบบ workflow และ reporting | [Developer Guideline](docs/CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md) |
| Architect / Developer เชื่อม CVAT กับ Platform | [Platform Integration Guideline](docs/CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md) |
| ออกแบบ AI Platform แบบ Roboflow ที่ใช้ CVAT | [AI Platform + CVAT Architecture](docs/AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md) |
| Developer ดู PostgreSQL schema และ monitor database | [Database Schema & Monitoring Guide](docs/CVAT-DATABASE-SCHEMA-MONITORING-GUIDE-TH.md) |
| ดูโครงสร้าง PostgreSQL ทุกตาราง | [Complete Database Schema Reference](docs/CVAT-DATABASE-SCHEMA-REFERENCE-TH.md) |
| ตั้งค่า SSO ด้วย Keycloak/OIDC | [AI Platform + CVAT Architecture — Keycloak](docs/AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md#31-ใช้-keycloak-ทำ-sso-ร่วมกับ-platform) |

แนะนำอ่านคู่มือปฏิบัติการก่อน แล้วอ่าน Developer Guideline และ AI Platform Architecture ตามลำดับ หากจะทำระบบจริงให้ดูเรื่อง edition/SSO, webhook deduplication, API consistency และ release snapshots ก่อนเริ่มเขียน integration

## ตัวอย่างรายงาน

วิธีดึงสถานะปัจจุบันด้วย curl/PAT และ Python พร้อม pagination: [คู่มือ Job Status API](docs/CVAT-JOB-STATUS-API-GUIDE-TH.md)

- [สถานะก่อนและหลังส่ง QA](examples/reports/job-status-before-after.csv)
- [สถานะหลังตรวจรับ](examples/reports/job-status-final.csv)
- [ผลตรวจสอบ export](examples/reports/export-validation.json)
- [คำอธิบาย field และข้อจำกัด](examples/reports/README.md)

รายงานเป็น snapshot จากการทดลองและปรับ path/checksum สำหรับเผยแพร่ ไม่ใช่ข้อมูลสด ไม่ใช่ระบบ export รายงานที่ติดตั้งพร้อมใช้ และไม่รวมภาพต้นฉบับหรือ ZIP dataset

## ขอบเขต Repository

```text
 docs/                  คู่มือและเอกสารอ้างอิง
examples/reports/      CSV/JSON และคำอธิบาย
README.md              จุดเริ่มต้น
.gitignore             ป้องกันข้อมูลทดลองและ secrets ถูกเพิ่มโดยเผลอ
```

Repository นี้แยกจาก source code และประวัติ Git ของ CVAT ตัวอย่าง schema, SQL และ pseudocode เป็นข้อเสนอสำหรับพัฒนา ต้องตรวจ API และ permissions กับ instance จริงก่อนใช้งาน

## ค่าที่ต้องปรับเมื่อนำไปใช้

- `/path/to/...` เป็น placeholder ให้แทนด้วย path ของเครื่องตนเอง
- `<YOUR_TEST_PASSWORD>` ให้ตั้งเอง ไม่มีรหัสผ่านบัญชีที่ใช้งานจริงใน repository
- `ptt-demo`, `ptt2`, user names และ resource IDs เป็นตัวอย่างจากการทดลอง ไม่ได้สร้างบัญชีหรือทรัพยากรให้ผู้อ่าน
- URL `localhost:8080` ใช้กับเครื่องทดลอง ให้เปลี่ยนเป็น CVAT URL ของทีม
- คู่มืออ้างผลทดสอบ CVAT 2.75.1 เมื่อ 16–17 กันยายน 2026; schema reference เป็น snapshot จาก `cvat_db` จริง ณ 17 กันยายน 2026

ลิงก์ source CVAT อ้างอิง commit ที่ตรวจในเครื่องทดลองเพื่ออ่าน implementation ได้แม้แยก repository แล้ว

## ข้อควรอ่านก่อน implement

CVAT ใช้จัดการภาพและ annotations ส่วน priority, SLA, assignment history และ business approval ต้องออกแบบเพิ่ม การกด Save ไม่ใช่ส่ง QA และการ Resolve Issue ไม่ใช่ approval ทั้ง Job

SSO ขึ้นกับ edition/deployment, Webhook ต้องตรวจ signature และรองรับการส่งซ้ำ, การเขียน local database กับ CVAT API ไม่ใช่ transaction เดียวกัน และ Keycloak ต้อง map สิทธิ์ CVAT แยกจากการ login รายละเอียดอยู่ใน [Integration guide](docs/CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md) และ [AI Platform Architecture](docs/AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md)

## แหล่งอ้างอิง

- [CVAT](https://github.com/cvat-ai/cvat)
- [CVAT Developer Documentation](https://docs.cvat.ai/docs/api_sdk/)
- [CVAT Webhooks](https://docs.cvat.ai/docs/administration/community/advanced/webhooks/)

เอกสารนี้เป็นคู่มือโครงการ ไม่ใช่เอกสารทางการของ CVAT
