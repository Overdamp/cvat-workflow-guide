# ทดลองสั่ง CVAT ผ่าน Postman

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

คู่มือนี้ใช้ REST API ผ่าน Postman ตั้งแต่ตรวจ Token → สร้าง Project → สร้าง Task → ส่งภาพ → รอ processing → อ่าน Job/annotation โดยใช้ผู้ใช้งานระดับเดียวกันใน Organization สำหรับ PoC

เปิดเอกสาร API แบบ interactive ได้ที่ [https://app.cvat.ai/api/docs/](https://app.cvat.ai/api/docs/) หากทดสอบ CVAT local ให้ใช้ `http://localhost:8080/api/docs/` เพื่อดู endpoint/schema ของ instance ที่กำลังรันอยู่

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

## 1.1 ค่าที่ใช้ทดสอบรอบนี้แบบ copy ตามได้

ใช้รูป 2 รูปนี้จากเครื่อง local:

```text
/home/luke/ai_training/codex_ptt_inspection/datasets/overall-ptt-object-detection.v11i.yolov11/train/images/008835_jpg.rf.f26414cb44a1d9911bbaf6c04840e3f8.jpg
/home/luke/ai_training/codex_ptt_inspection/datasets/overall-ptt-object-detection.v11i.yolov11/train/images/008887_jpg.rf.ec18ceeb39a983ec068c3668c5ba0737.jpg
```

ตรวจไฟล์ก่อนเปิด Postman:

```bash
test -f /home/luke/ai_training/codex_ptt_inspection/datasets/overall-ptt-object-detection.v11i.yolov11/train/images/008835_jpg.rf.f26414cb44a1d9911bbaf6c04840e3f8.jpg && echo image-1-ok
test -f /home/luke/ai_training/codex_ptt_inspection/datasets/overall-ptt-object-detection.v11i.yolov11/train/images/008887_jpg.rf.ec18ceeb39a983ec068c3668c5ba0737.jpg && echo image-2-ok
```

ถ้าเห็น `image-1-ok` และ `image-2-ok` แปลว่าเลือก path ได้ถูกต้อง

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

## 2.1 วิธีทำแบบละเอียดทีละคลิก

### ขั้นที่ 0: เปิด CVAT และ Postman Agent

1. เปิด browser ไปที่ `http://localhost:8080`
2. Login ด้วยบัญชี CVAT ที่มีสิทธิ์สร้าง Project/Task ใน organization `ptt-demo`
3. เปิด Postman Desktop หรือเปิด Postman Web แล้วตรวจว่า Agent เป็น **Desktop Agent**
4. ห้ามใช้ Cloud Agent เพราะ Cloud Agent อ่านไฟล์ใน `/home/luke/...` ไม่ได้

### ขั้นที่ 1: Import Collection

1. กด **Import** ใน Postman
2. เลือกไฟล์:

```text
/home/luke/cvat/cvat-workflow-guide/examples/postman/CVAT-API-Workflow.postman_collection.json
```

3. กด **Import**
4. ควรเห็น collection ชื่อ `CVAT API Workflow - Equal Role PoC`

### ขั้นที่ 2: สร้าง Environment

1. กดเมนู **Environments**
2. กด **Create Environment**
3. ตั้งชื่อ `CVAT Local`
4. เพิ่มตัวแปรดังนี้:

| Variable | Initial value | Current value |
|---|---|---|
| `cvat_base_url` | `http://localhost:8080` | `http://localhost:8080` |
| `cvat_org` | `ptt-demo` | `ptt-demo` |
| `cvat_pat` | เว้นว่าง | วาง CVAT PAT |
| `project_id` | เว้นว่าง | เว้นว่าง |
| `task_id` | เว้นว่าง | เว้นว่าง |
| `request_id` | เว้นว่าง | เว้นว่าง |
| `job_id` | เว้นว่าง | เว้นว่าง |

5. กด **Save**
6. เลือก `CVAT Local` จาก environment selector มุมขวาบน

สร้าง PAT จาก CVAT ที่ **Settings → Access tokens** ใช้ token แบบเขียนได้สำหรับการทดสอบนี้ วางใน Current value เท่านั้น และอย่าใช้ Keycloak token แทนโดยสมมติว่าใช้ได้

### ขั้นที่ 3: ตรวจ token

1. เปิด collection
2. เปิด request `01 - Check current user`
3. กด **Send**
4. ต้องได้ HTTP `200`
5. Response ควรมี `id` และ `username`

ถ้าได้ `401` ให้ตรวจ PAT ถ้าได้ `403` ให้ตรวจ membership ใน `ptt-demo`

### ขั้นที่ 4: สร้าง Project

1. เปิด `02 - Create project`
2. ตรวจว่า Environment เป็น `CVAT Local`
3. กด **Send**
4. ต้องได้ HTTP `201` หรือ `200`
5. เปิด Environment ดูว่า `project_id` ถูกเติมแล้ว

Project นี้มี labels ชื่อ `pump` และ `valve` สำหรับ PoC เท่านั้น

### ขั้นที่ 5: สร้าง Task

1. เปิด `03 - Create task`
2. ตรวจว่า URL แสดง `{{project_id}}` ไม่ใช่ค่าว่าง
3. กด **Send**
4. ต้องได้ HTTP `201` หรือ `200`
5. ตรวจ Environment ว่ามี `task_id`

### ขั้นที่ 6: เลือกไฟล์ local และ upload

1. เปิด `04 - Upload local images`
2. เปิดแท็บ **Body**
3. เลือก **form-data**
4. แถว `image_quality` เป็น Text และค่า `85`
5. แถว `client_files[0]` เปลี่ยนชนิดเป็น **File** แล้วเลือก:

```text
/home/luke/ai_training/codex_ptt_inspection/datasets/overall-ptt-object-detection.v11i.yolov11/train/images/008835_jpg.rf.f26414cb44a1d9911bbaf6c04840e3f8.jpg
```

6. แถว `client_files[1]` เปลี่ยนชนิดเป็น **File** แล้วเลือก:

```text
/home/luke/ai_training/codex_ptt_inspection/datasets/overall-ptt-object-detection.v11i.yolov11/train/images/008887_jpg.rf.ec18ceeb39a983ec068c3668c5ba0737.jpg
```

7. อย่าเพิ่ม `Content-Type` เอง
8. กด **Send**
9. ต้องได้ HTTP `202` และ response มี `rq_id`
10. ตรวจ Environment ว่า `request_id` ถูกเติมแล้ว

### ขั้นที่ 7: รอ processing

1. เปิด `05 - Get request status`
2. กด **Send** ซ้ำทุก 2–5 วินาที
3. หยุดเมื่อ response เป็น:

```json
{"status":"finished"}
```

4. ถ้าเป็น `queued` หรือ `started` ให้รอต่อ
5. ถ้าเป็น `failed` ให้เก็บ response ไว้ตรวจและอย่าสร้าง Task ใหม่ทันที

### ขั้นที่ 8: อ่าน Job และ metadata

1. เปิด `06 - List jobs (one annotation job)`
2. กด **Send**
3. ต้องเห็น annotation job หนึ่งรายการ
4. ตรวจ Environment ว่า `job_id` ถูกเติมแล้ว
5. เปิด `07 - Get media metadata`
6. กด **Send** และเก็บ response ไว้ใช้ map `frame` กับชื่อภาพ

### ขั้นที่ 9: เปิด CVAT เพื่อวาด annotation

แทนค่าจาก Environment ใน URL นี้:

```text
http://localhost:8080/tasks/{{task_id}}/jobs/{{job_id}}
```

ตัวอย่างถ้า `task_id=12` และ `job_id=19`:

```text
http://localhost:8080/tasks/12/jobs/19
```

1. เปิด URL ใน browser
2. Login ด้วย user ที่มีสิทธิ์
3. เลือก label `pump` หรือ `valve`
4. วาด rectangle บนภาพ
5. กด **Save**
6. ตรวจว่าไม่มีข้อความ save error

### ขั้นที่ 10: อ่าน annotation ผ่าน Postman

1. กลับ Postman
2. เปิด `08 - Get annotations after Save`
3. กด **Send**
4. ต้องเห็น `shapes` อย่างน้อยหนึ่งรายการ
5. ตรวจค่า `type`, `label_id`, `frame` และ `points`

### ขั้นที่ 11: Complete Job

1. ตรวจว่า Save ใน CVAT สำเร็จแล้ว
2. เปิด `09 - Complete job`
3. กด **Send**
4. ต้องได้ response:

```json
{
  "stage": "annotation",
  "state": "completed"
}
```

5. นี่คือการจบ PoC annotation เท่านั้น ยังไม่ใช่ approval จาก reviewer

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
