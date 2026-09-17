# Platform ทดลองเชื่อม CVAT จริง

## เปิดใช้งาน

ต้องมี Node.js 22 และ CVAT ที่ localhost:8080 จาก root repository รัน:

```bash
node prototype/server.cjs
```

เปิด **http://localhost:5175/platform/** แทนหน้า static เดิมที่พอร์ต 5173 ไม่ต้องติดตั้ง npm packages

## วิธีเชื่อมต่อ

```text
Browser → localhost:5175/platform/ → Platform UI
        → localhost:5175/tasks/... → proxy → CVAT localhost:8080
        → localhost:5175/api/...   → proxy → CVAT API
```

CVAT เดิมส่ง X-Frame-Options: deny ทำให้ iframe ใช้ไม่ได้ Proxy ให้ Platform และ CVAT อยู่ origin เดียวกัน ปรับ response ผ่าน proxy เป็น SAMEORIGIN และ CSP frame-ancestors 'self' โดยไม่แก้/restart CVAT containers

Proxy ส่ง session cookie และ CSRF token ให้ CVAT ตรวจตามปกติ แปลง Origin/Referer ของหน้า local ที่ตรวจแล้วให้ตรงกับ upstream ไม่ได้ทำ SSO หรือเพิ่มสิทธิ์บัญชี Bind เฉพาะ loopback และใช้ upstream คงที่สำหรับเครื่องทดสอบ

## ทดลอง workflow

1. เปิด URL ข้างต้น Login ใน CVAT ที่แสดงใน iframe หากยังไม่มี session
2. ใส่ Job ID เช่น 2 แล้วกด **เปิด Job** Dashboard แสดงบัญชีจริง ผู้รับงาน Stage/State และจำนวน Issues จาก API
3. ทำ annotation และ Save ใน CVAT ปุ่มอัปเดตสถานะอ่านข้อมูลใหม่โดยไม่ reload editor
4. Coordinator ที่มีสิทธิ์จัดการ Job ระบุ reviewer01 แล้วกด **ส่งตรวจ QA** ระบบค้น user ID และ PATCH เป็น validation / in progress พร้อม assignee
5. Reviewer เปิด/ตอบ Issue ใน CVAT หากต้องแก้ Coordinator ระบุ annotator เดิมแล้วกด **ส่งกลับแก้** (annotation / in progress)
6. Reviewer ตรวจซ้ำและ Resolve Issue ใน CVAT กดอัปเดตสถานะ
7. กด **ตรวจรับ** หลังตรวจครบ ระบบตรวจ open Issues แล้ว PATCH เป็น acceptance / completed โดยไม่เปลี่ยน assignee

ทุกปุ่มเปลี่ยน workflow มี confirmation เพราะเปลี่ยน Job จริง การเปลี่ยนบัญชีต้อง logout/login ใน CVAT ไม่มี dropdown ปลอมตัวเป็นผู้ใช้อื่น CVAT อาจตอบ 403 หากบัญชีไม่มีสิทธิ์จัดการงานนั้น

Job #2 ตรวจรับแล้วในการทดลองก่อนหน้า ใช้ Job ใหม่หากต้องการคงสถานะเดิม ปุ่ม workflow ไม่สร้าง ZIP/release หรือเริ่ม training ใช้ Export ใน CVAT เมื่อจำเป็น

## API ที่ใช้

| API | วัตถุประสงค์ |
|---|---|
| GET /api/users/self | บัญชีจริง |
| GET /api/jobs/{id} | Job และสถานะ |
| GET /api/issues?job_id={id} | Issues พร้อม pagination |
| GET /api/users?search={username} | ค้นผู้รับตามสิทธิ์ |
| PATCH /api/jobs/{id} | เปลี่ยน stage, state และ assignee |

ไม่มีรหัสผ่านใน source หรือ simulated localStorage state ตัว editor บันทึก annotations ผ่าน CVAT API

## ผลตรวจและขอบเขต

- ตรวจ syntax JavaScript/server ผ่าน
- หน้า Platform และ CVAT ผ่าน proxy ตอบ HTTP 200 และอนุญาต same-origin frame
- ทดสอบ login reviewer และ GET user, Job #2, Issues สำเร็จ พร้อม session/CSRF cookies
- ไม่เปลี่ยนสถานะ Job #2 เพื่อทดสอบ ยังไม่ได้ยืนยันการวาด/Save ผ่าน browser อัตโนมัติ
- ตรวจ updated_date ก่อน PATCH แต่ไม่ใช่ atomic lock; production ต้องเพิ่ม concurrency control
- ยังไม่มี Keycloak SSO, webhook, business audit database หรือ release service
- ไม่มี WebSocket forwarding สำหรับฟีเจอร์ที่ต้องใช้ WebSocket

หาก iframe ว่าง ตรวจว่าเปิด /platform/ พอร์ต 5175 และ server รันอยู่ 401 ให้ login; 403 ตรวจ membership/assignment; 502 ตรวจ CVAT localhost:8080
