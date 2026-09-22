# ทดลองสั่ง CVAT ผ่าน Postman

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

คู่มือนี้ใช้ REST API ผ่าน Postman ตั้งแต่ตรวจ Token → สร้าง Project → สร้าง Task → ส่งภาพ → รอ processing → อ่าน Job/annotation โดยใช้ผู้ใช้งานระดับเดียวกันใน Organization สำหรับ PoC

นำเข้า Collection จาก [`examples/postman/CVAT-API-Workflow.postman_collection.json`](../examples/postman/CVAT-API-Workflow.postman_collection.json) แล้วทำตามลำดับที่แสดงใน Collection

## 1. เตรียม Environment

สร้าง Postman Environment ชื่อ `CVAT Local` แล้วเพิ่ม variables:

| Variable | Initial value | Current value |
|---|---|---|
| `cvat_base_url` | `http://localhost:8080` | เหมือนกัน |
| `cvat_org` | `ptt-demo` | เหมือนกัน |
| `cvat_pat` | เว้นว่าง | วาง PAT เต็มที่นี่ |
| `project_id` | เว้นว่าง | Collection จะใส่ให้ |
| `task_id` | เว้นว่าง | Collection จะใส่ให้ |
| `request_id` | เว้นว่าง | Collection จะใส่ให้ |
| `job_id` | เว้นว่าง | Collection จะใส่ให้ |

วาง PAT ใน **Current value** เท่านั้น ไม่ใส่ใน Initial value และห้าม export/share Environment ที่มี Token หลังทดสอบเสร็จ ถ้า Token ที่สร้างเป็น Read only จะอ่านได้แต่สร้างหรือเปลี่ยนงานไม่ได้

Collection ใช้ Authorization แบบ Bearer จาก `{{cvat_pat}}` ทุก request ยกเว้น upload ที่ยังใช้ header เดียวกัน

## 2. ลำดับการกด Send

1. `01 - Check current user` ตรวจว่าเป็น user ที่ตั้งใจใช้
2. `02 - Create project` สร้าง Project พร้อม `pump` และ `valve` labels แล้วเก็บ `project_id`
3. `03 - Create task` สร้าง Task ใน Project แล้วเก็บ `task_id`
4. `04 - Upload local images` เลือก Body → form-data แล้วกำหนดไฟล์จริงในช่อง `client_files[0]` และ `client_files[1]`
5. `05 - Get request status` กดซ้ำจน response มี `status: finished` แล้ว collection เก็บ `request_id` จาก upload ไว้ให้
6. `06 - List jobs` อ่าน Jobs และเก็บ annotation `job_id` โดยอัตโนมัติเมื่อมีเพียงหนึ่ง Job
7. `07 - Get media metadata` เก็บข้อมูล frame/filename/ขนาดภาพสำหรับ map กลับ Platform
8. เปิด URL `/tasks/{{task_id}}/jobs/{{job_id}}` ใน browser ด้วยบัญชีที่มีสิทธิ์ วาด rectangle แล้วกด Save
9. `08 - Get annotations` อ่าน JSON annotations ล่าสุดหลัง Save
10. `09 - Complete job` เปลี่ยนเป็น `annotation / completed` เมื่อ Save สำเร็จแล้วเท่านั้น

ถ้า upload ใช้ภาพในเครื่อง Postman ต้องรัน Desktop Agent และเลือกไฟล์จากเครื่องเดียวกับที่เปิด CVAT หากใช้ Postman Web ให้ใช้ `remote_files`/Cloud Storage แทน หรือเปลี่ยนเป็น Desktop Agent

## 3. สิ่งที่ response หมายถึง

| Response | ความหมาย |
|---|---|
| `200` | อ่านหรือแก้สำเร็จ |
| `201` | สร้าง Project/Task สำเร็จ |
| `202` | รับงาน async แล้ว ต้องใช้ `request_id` poll ต่อ |
| `400` | body/parameter ไม่ถูกต้อง |
| `401` | Token ผิด หมดอายุ หรือไม่ได้ส่ง |
| `403` | ไม่มีสิทธิ์ใน Organization/Project/Job |
| `404` | ID หรือ query context ไม่ถูกต้อง |
| `409` | ข้อมูลเปลี่ยนชนกัน ต้องอ่านปัจจุบันก่อน retry |
| `429`, `5xx` | retry แบบจำกัดและไม่ POST สร้างซ้ำโดยไม่ตรวจผลเดิม |

`annotation / completed` แปลว่าจบ PoC นี้ ไม่ใช่ approval จาก Reviewer การอ่าน annotations ผ่าน API ไม่ต้อง export ZIP และไม่ควรทำ export ทุกครั้งที่ดูสถานะ

## 4. Upload files ใน Postman

เปิด request `04 - Upload local images` แล้วตั้ง Body เป็น `form-data`:

| Key | Type | Value |
|---|---|---|
| `image_quality` | Text | `85` |
| `client_files[0]` | File | ภาพ train รูปแรก |
| `client_files[1]` | File | ภาพ train รูปที่สอง |

ห้ามใส่ `Content-Type` เอง เพราะ Postman ต้องเติม multipart boundary ให้เอง Authorization ให้ใช้ Bearer จาก Collection

## 5. ใช้ MinIO แทนไฟล์ local

ใน request data ให้เปลี่ยนเป็น raw JSON และใช้ presigned URLs ที่ CVAT worker เข้าถึงได้:

```json
{
  "image_quality": 85,
  "remote_files": [
    "https://minio.example/inspection/img-101.jpg?<signed-query>",
    "https://minio.example/inspection/img-102.jpg?<signed-query>"
  ]
}
```

URL ต้องไม่หมดอายุก่อน CVAT processing เสร็จ การใช้ `remote_files` อาจทำให้ CVAT ดาวน์โหลด/cache ไฟล์ จึงไม่ควรถือว่าเป็น zero-copy โดยอัตโนมัติ

## 6. ตัวอย่าง annotation response

```json
{
  "version": 0,
  "tags": [],
  "shapes": [
    {
      "id": 246,
      "frame": 0,
      "label_id": 35,
      "type": "rectangle",
      "points": [980.0, 426.25, 1167.5, 622.5],
      "rotation": 0.0,
      "attributes": []
    }
  ],
  "tracks": []
}
```

`label_id` ต้อง map กับ labels API และ `frame` ต้อง map กับ media metadata ก่อนเชื่อมกลับ `image_id` ของ Platform ส่วน `points` ของ rectangle ที่ rotation เป็นศูนย์คือ `[xmin, ymin, xmax, ymax]` หน่วย pixel

## 7. ข้อควรระวัง

- Collection นี้มี scripts เพื่อเก็บ IDs จึงควรรันตามลำดับและใช้ Environment ที่ถูกต้อง
- `05 - Get request status` ต้องกดซ้ำจน `finished`; ไม่สร้าง Task ใหม่เมื่อยังรออยู่
- ถ้ามีหลาย annotation Jobs ให้แก้ script `06 - List jobs` และตรวจทุก Job ไม่เลือกตัวแรกเงียบ ๆ
- อย่าเก็บ Token, presigned URL หรือข้อมูลภาพจริงใน collection ที่ commit ขึ้น Git
- เก็บ annotation revision ใน Platform ด้วย `revision_id`/digest เพื่อให้กด Send ซ้ำแล้วไม่เกิดข้อมูลซ้ำ
- Postman ใช้ทดสอบและสำรวจ API; production Backend ควรมี retry, pagination, inbox/outbox และ audit ตามคู่มือ End-to-End

ดู flow แบบ shell ที่ให้ผลเดียวกันใน [REST hands-on](08_CVAT-HANDS-ON-LOCAL-DATASET-TH.md) และดูขอบเขต API/SDK ใน [Backend guide](03_CVAT-MINIO-BACKEND-END-TO-END-TH.md)
