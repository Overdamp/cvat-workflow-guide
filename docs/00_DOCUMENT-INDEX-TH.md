# สารบัญเอกสารสำหรับ Developer

เอกสารทุกหน้ามีลิงก์กลับมาที่สารบัญเพื่อเปิดไปมาได้สะดวก

## วิธีแยกเอกสาร Production กับเอกสารทดลอง

**แนวทาง Production ที่ให้ Backend ยึดเป็นหลัก:** เอกสาร 03–05 และแนวคิด API/SDK ในเอกสาร 07, 09, 10 ใช้ REST API หรือ Python SDK เพื่อสร้างงาน อ่านสถานะ และอ่าน annotation แล้วบันทึกลง Platform Database โดยตรง ภาพต้นฉบับอยู่ใน MinIO และไม่ใช้ export ZIP เป็นฐานข้อมูล

**Optional Manual Flow / เอกสารทดลอง:** เอกสาร 08 เป็นการ upload ภาพ local เพื่อพิสูจน์ workflow, เอกสาร 10 ใช้ local dataset และสร้างไฟล์ JSON ชั่วคราว, เอกสาร 11 สร้าง CSV status report และ `examples/reports/` เป็น snapshot จากการทดลอง ใช้ได้เมื่อ backend/MinIO ยังไม่พร้อมหรือใช้ debug/manual release แต่ไม่ใช่ข้อกำหนดให้ production เก็บไฟล์ซ้ำถาวร

**Export ZIP/COCO/YOLO:** ใช้เมื่อสร้าง Dataset Release, ส่งเข้า training หรือส่งมอบให้ consumer เท่านั้น ไม่ใช้ polling สถานะหรือ sync ทุกครั้งที่มีการแก้ annotation

**API reference:** [CVAT API Docs](https://app.cvat.ai/api/docs/) เป็น interactive reference; หากทำงานกับ local CVAT ให้ใช้ host เดิมของ instance เช่น `http://localhost:8080/api/docs/`

**CVAT official documentation:** [https://docs.cvat.ai/docs/](https://docs.cvat.ai/docs/)

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
| 16 | [Backend Developer Handoff](16_BACKEND-DEVELOPER-HANDOFF-TH.md) | เอกสารส่งต่อสำหรับ Backend Developer |
| 17 | [Historical QA Notes](17_CVAT-QA-WORKFLOW-SYSTEM-DESIGN-TH.md) | ประวัติการทดลอง ไม่ใช่ implementation contract |
| 18 | [Annotation Editor Feature Matrix](18_ANNOTATION-EDITOR-FEATURE-MATRIX-TH.md) | เปรียบเทียบฟีเจอร์หน้า annotate โดยใช้ Roboflow เป็น baseline |
| 19 | [CVAT REST API to Backend Explanation](19_CVAT-REST-API-TO-BACKEND-EXPLANATION-TH.md) | ความสัมพันธ์ระหว่าง CVAT DB, REST API และ Platform DB สำหรับ Backend |

เอกสารอ้างอิงที่ย้ายออกจากคู่มือหลักอยู่ใน [archive](archive/)
