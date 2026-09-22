# Sanitized REST API output example

ไฟล์ในโฟลเดอร์นี้เป็นตัวอย่างผลลัพธ์จากการทดลอง REST API ด้วยภาพ 2 รูป เพื่อให้ Backend Developer เห็นหน้าตา response ที่ต้อง parse

ข้อมูลถูกทำให้ปลอดภัยสำหรับ repository แล้ว:

- แทน CVAT host ด้วย `https://cvat.example`
- ไม่รวม PAT, secret หรือ presigned URL
- ใช้ username/ID เป็นตัวอย่าง
- เป็น snapshot ไม่ใช่ schema ภายใน PostgreSQL และไม่ใช่ข้อมูลสด

แหล่งผลลัพธ์ดิบในเครื่องอยู่ที่ `artifacts/api-test-RoPMMo/` แต่ไม่ถูก commit เพราะเป็น artifacts จากการทดลอง

ไฟล์สำคัญ:

| ไฟล์ | ความหมาย |
|---|---|
| `annotations.json` | shape และพิกัดจาก `GET /api/jobs/{id}/annotations` |
| `mapped-shapes.json` | ผล map `label_id`/`frame` เป็นชื่อ label/ภาพ |
| `labels.json` | label definitions |
| `media-meta.json` | frame, filename และ image dimensions |
| `ids.json` | project/task/job mapping |
| `project.json`, `task.json`, `jobs.json` | response จาก resource APIs |
| `request.json` | สถานะ asynchronous upload/processing |

Production ควรอ่าน response ผ่าน REST API/SDK แล้ว validate และ upsert ลง Platform Database ไม่ควรเก็บ JSON เหล่านี้ซ้ำทุกครั้ง

