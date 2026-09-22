# สารบัญเอกสารสำหรับ Developer

เอกสารทุกหน้ามีลิงก์กลับมาที่สารบัญเพื่อเปิดไปมาได้สะดวก

อ่านตามลำดับนี้เพื่อเข้าใจระบบจากภาพรวมไปจนถึงการลงมือทดสอบ:

| ลำดับ | เอกสาร | เนื้อหา |
|---:|---|---|
| 01 | [AI Platform + CVAT Architecture](01_AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md) | ภาพรวมระบบและขอบเขตของแต่ละบริการ |
| 02 | [Annotation Tool Selection Matrix](02_ANNOTATION-TOOL-SELECTION-MATRIX-TH.md) | เหตุผลเลือก CVAT และเปรียบเทียบเครื่องมือ |
| 03 | [Backend End-to-End](03_CVAT-MINIO-BACKEND-END-TO-END-TH.md) | MinIO → CVAT → annotation/QA → platform database |
| 04 | [Platform Integration Guideline](04_CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md) | integration contract, retry, consistency และ release |
| 05 | [Developer Workflow Guideline](05_CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md) | queue, assignment, QA และ dataset release |
| 06 | [Operations Guide](06_CVAT-WORKFLOW-OPERATIONS-GUIDE-TH.md) | ขั้นตอนของ annotator, reviewer และ coordinator |
| 07 | [REST API Quickstart](07_CVAT-API-WORKFLOW-QUICKSTART-TH.md) | คำสั่ง curl ตั้งแต่สร้างงานจนรับผล |
| 08 | [Local Dataset Hands-on](08_CVAT-HANDS-ON-LOCAL-DATASET-TH.md) | ทดลองกับภาพจาก dataset ในเครื่อง |
| 09 | [Postman Workflow](09_CVAT-POSTMAN-WORKFLOW-GUIDE-TH.md) | ทดลอง REST API ผ่าน Postman |
| 10 | [Python SDK Hands-on](10_CVAT-SDK-HANDS-ON-TH.md) | ทดลองควบคุม CVAT ด้วย Python SDK |
| 11 | [Job Status API](11_CVAT-JOB-STATUS-API-GUIDE-TH.md) | อ่านสถานะงานและสร้างรายงาน |
| 12 | [Database Monitoring](12_CVAT-DATABASE-SCHEMA-MONITORING-GUIDE-TH.md) | ตรวจ schema และ monitor โดยไม่เขียน DB CVAT โดยตรง |
| 13 | [Database Schema Reference](13_CVAT-DATABASE-SCHEMA-REFERENCE-TH.md) | snapshot schema สำหรับอ้างอิง |
| 14 | [Custom Annotation Frontend Options](14_CUSTOM-ANNOTATION-FRONTEND-OPTIONS-TH.md) | ทางเลือกถ้า backend ทำหน้า annotation เอง |
| 15 | [Label Studio Frontend Integration](15_LABEL-STUDIO-FRONTEND-INTEGRATION-GUIDE-TH.md) | แนวทางใช้ LSF กับ Keycloak, MinIO และ backend DB |
| 16 | [Daily Report](16_DAILY-REPORT-2026-09-22-TH.md) | สรุปงานและคำตอบสำหรับการประชุม |
| 17 | [Historical QA Notes](17_CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md) | ประวัติการทดลอง ไม่ใช่ implementation contract |

เอกสารอ้างอิงที่ย้ายออกจากคู่มือหลักอยู่ใน [archive](archive/)
