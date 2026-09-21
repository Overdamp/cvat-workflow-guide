# ทดลอง Python SDK ด้วย dataset เดิม

ใช้ภาพ train 2 รูปจาก dataset เครื่อง luke และ 26 classes เหมือน REST hands-on แต่สร้าง Project/Task ใหม่ การเรียกใช้เป็น SDK จริงผ่าน make_client, projects.create, tasks.create, upload_data, get_annotations และ job.update; SDK เรียก REST API ภายในให้อีกทอด

## 1. ติดตั้ง (ครั้งแรก)

```bash
cd /home/luke/cvat/cvat-workflow-guide
python3 -m venv .venv
.venv/bin/pip install 'cvat-sdk~=2.75.0'
```

ใช้ SDK สาย 2.75 สำหรับ server สาย 2.75 ต้องปรับเวอร์ชันถ้า upgrade server ไม่ต้อง activate venv เพราะคำสั่งใช้ Python ของ venv โดยตรง

## 2. สร้างงานใหม่

```bash
.venv/bin/python examples/sdk/local_dataset.py create
```

สคริปต์จะถาม CVAT PAT ให้วางแล้ว Enter (ไม่แสดงตัวอักษร) ถ้ามี CVAT_ACCESS_TOKEN ใน environment จะใช้ค่านั้น สร้าง Project, Task, อัปโหลดรูป 2 รูป รอประมวลผล แล้วพิมพ์ URL เปิด Job กับ Run folder

บันทึก path ที่แสดงไว้ เช่น artifacts/sdk-20260922T... เป็นค่าจริงเฉพาะรอบ ไม่ใช้ชื่อสมมตินี้ตรง ๆ

การรัน create อีกครั้งสร้างงานใหม่ ถ้า upload ล้มเหลวให้ตรวจ state.json และ Task เดิมก่อน ไม่ retry create โดยไม่ตรวจ ไม่มีการลบงานเดิมอัตโนมัติ

## 3. วาดและ Save

เปิด URL ที่แสดง Login ใน CVAT วาด rectangle บนภาพแล้วกด Save รอจนบันทึกเสร็จ ขั้นนี้เหมือน REST hands-on ไม่มีการ import labels เดิมของ YOLO

## 4. ดึงผลผ่าน SDK

ให้ Terminal ถาม path เพื่อไม่ต้องแก้คำสั่งข้างใน:

```bash
read -r -p 'วาง Run folder ที่สคริปต์แสดง: ' SDK_RUN
.venv/bin/python examples/sdk/local_dataset.py read --run "$SDK_RUN"
```

ถาม PAT อีกครั้งหากไม่ได้ตั้ง environment แล้วแสดง image_name, label, points และจำนวน shapes/tags/tracks พร้อมเขียน annotations.json, labels.json, media-meta.json และ mapped-shapes.json ใน Run folder

mapped-shapes เป็นตัวอย่างสำหรับ shapes เท่านั้น tags/tracks ยังอยู่ครบใน annotations.json รูปไม่มีกรอบจะแสดงจำนวนศูนย์ได้

## 5. ระบุเสร็จ (optional)

```bash
.venv/bin/python examples/sdk/local_dataset.py complete --run "$SDK_RUN"
```

ยืนยันด้วย yes หลัง Save เพื่อ PATCH ผ่าน SDK เป็น annotation/completed ไม่มีการอนุมัติ QA หรือ export ZIP อัตโนมัติ ผู้ใช้ทำงานระดับเดียวกันตาม PoC เดิม

## เปรียบเทียบกับ REST

| SDK | REST ที่สอดคล้อง |
|---|---|
| client.projects.create | POST /api/projects |
| client.tasks.create | POST /api/tasks |
| task.upload_data | Upload + processing polling |
| task.get_jobs | GET jobs ของ Task |
| job.update | PATCH /api/jobs/{id} |
| job.get_annotations | GET /api/jobs/{id}/annotations |
| task.get_meta / get_labels | Metadata / labels API |

Token ไม่บันทึกลงไฟล์ ผลทดลองเก็บใต้ artifacts ที่ Git ignore แล้ว ยังต้องให้ผู้ใช้รันด้วย PAT และทำ annotation เพื่อยืนยันครบวงจร ไม่ถือว่าตัวอย่างนี้ผ่าน integration test เพียงเพราะ syntax ผ่าน

[สคริปต์](../examples/sdk/local_dataset.py) · [REST hands-on](CVAT-HANDS-ON-LOCAL-DATASET-TH.md) · [สารบัญ](../DOCS-INDEX.md)
