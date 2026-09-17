# PTT AI Platform Prototype

หน้าเว็บตัวอย่างสำหรับทดลอง workflow ที่เชื่อมกับ CVAT โดยใช้ข้อมูลการทดลองจริง:

- Organization: `ptt-demo`
- Project: `ptt2` (#3)
- Task: `train` (#2)
- Job: #2 (20 ภาพ)
- CVAT URL เริ่มต้น: `http://localhost:8080`

## เริ่มใช้งาน

จาก root ของ repository:

```bash
cd prototype
python3 -m http.server 5173
```

เปิด `http://localhost:5173` ใน browser และเปิด CVAT ที่ `http://localhost:8080` ไว้ด้วย จากนั้นลอง:

1. กด **เปิด Job ใน CVAT** เพื่อทำงานใน CVAT จริง
2. กด **ส่ง QA** เพื่อจำลอง Coordinator ส่งงานให้ reviewer
3. กด **ส่งกลับแก้** เพื่อจำลองการส่ง Issue กลับ annotator
4. กด **Resolve issue** เพื่อปิด Issue
5. กด **ตรวจรับและสร้าง release** เพื่อสร้าง release ในโหมดทดลอง

## สิ่งที่ prototype นี้ทำและยังไม่ทำ

หน้าเว็บนี้เก็บสถานะ demo ใน `localStorage` จึงกดทดสอบ workflow ได้ทันทีโดยไม่ต้องมี backend เพิ่ม ปุ่ม workflow เป็น simulation และยังไม่ได้เปลี่ยนข้อมูล CVAT จริง ส่วน CVAT Job ถูกโหลดไว้ใน iframe บนหน้าเดียวกันโดยตรง

เมื่อนำไปต่อ production ให้เปลี่ยน `app.js` เป็น Platform API ที่เรียก CVAT REST API, ใช้ Keycloak OIDC SSO, เก็บ mapping ใน Platform PostgreSQL และรับ Webhook เพื่อ sync สถานะตามเอกสาร architecture ใน `docs/AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md`

## หมายเหตุ iframe

ช่อง workspace โหลด CVAT ใน iframe โดยตรง แต่ browser/CVAT อาจบล็อกด้วย `X-Frame-Options` หรือ CSP ในกรณีนั้นให้ใช้ปุ่มเปิดแท็บใหม่ หรือปรับ reverse proxy/CSP ของ CVAT ให้อนุญาต origin ของ Platform ก่อนใช้งาน production
