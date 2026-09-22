# API Workflow แบบง่าย: สั่ง CVAT ตั้งแต่สร้างงานจนรับผล

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

วันที่ 22 กันยายน 2026 · สำหรับ Backend Developer · อ้างอิง source สาย 2.75 ในเครื่องทดลอง

> **ขอบเขต:** ขั้นตอนนี้เป็น PoC ที่มีทั้ง local upload และ MinIO remote upload เพื่อทดสอบ API ในเครื่อง local สำหรับ production ให้ใช้ MinIO/cloud storage หรือ ingestion service ตามคู่มือ 03 ส่วน local upload และ export ZIP เป็น **Optional Manual Flow** สำหรับ debug, migration หรือ manual release เมื่อจำเป็น

## ขอบเขตของรอบนี้

ทุกคนทำงานระดับเดียวกัน ไม่มีคิวแยก Annotator/Reviewer หรือ approval หลายชั้น ใช้ flow เริ่มทำ → บันทึก → เสร็จ → ดึงผล แบบนี้เป็นการประกาศเสร็จงาน ไม่ใช่หลักฐานว่าผ่าน QA อิสระ

สำหรับ Organization ทดสอบ ให้เจ้าของเตรียมสมาชิกที่ต้องสร้างและจัดการงานเป็น role เดียวกัน เช่น Supervisor แล้วทดสอบ endpoints ด้านล่างด้วยบัญชีของแต่ละคน (Owner ยังเป็นผู้ดูแลองค์กร) ไม่ต้องตั้งทุกคนเป็น global admin ไม่มีการเปลี่ยนสิทธิ์บัญชีจริงจากการเขียนคู่มือนี้

Backend ใช้ PAT ของ service account ที่มีสิทธิ์ในองค์กรนี้ ผู้ใช้ยัง login CVAT ด้วยบัญชีของตนเอง ไม่แชร์ PAT ของ Backend กับ browser

## Flow และรายการ API

```text
ตรวจ auth
→ สร้าง Project + labels (ครั้งแรก)
→ สร้าง Task ใน Project
→ ส่งภาพ local หรือ MinIO URLs
→ รอ async processing
→ อ่าน Jobs และ frame mapping
→ เปิด editor / ทำ annotation / Save
→ เปลี่ยน Job เป็นเสร็จ
→ อ่าน annotations + labels + metadata
→ map กลับ image_id ของ Platform และบันทึก revision
→ export เฉพาะถ้าต้องการไฟล์ COCO/YOLO
```

| ลำดับ | คำสั่ง | สิ่งที่ Backend ต้องเก็บ |
|---|---|---|
| 0 | GET /api/users/self | ตรวจตัวตน token |
| 1 | POST /api/projects | project.id |
| 2 | POST /api/tasks | task.id |
| 3 | POST /api/tasks/{id}/data | rq_id |
| 4 | GET /api/requests/{rq_id} | status / message |
| 5 | GET /api/jobs?task_id={id} | job.id / start_frame / stop_frame |
| 6 | GET /api/tasks/{id}/data/meta | frame mapping และขนาดภาพ |
| 7 | เปิด /tasks/{task_id}/jobs/{job_id} | URL สำหรับ browser |
| 8 | PATCH /api/jobs/{id} | stage / state |
| 9 | GET /api/jobs/{id}/annotations | shapes / tags / tracks |
| 10 | GET /api/labels?task_id={id} | label_id → class name |
| 11 | POST /api/tasks/{id}/dataset/export | optional rq_id สำหรับ export |

## 0. เตรียม Terminal

ใช้ Bash, curl, jq รันทีละส่วนใน Terminal เดียวกัน สคริปต์นี้สร้างข้อมูลจริงเมื่อเรียก POST/PATCH จึงใช้ Project ใหม่สำหรับ PoC ไม่รันทับงานเดิม โดยตัวอย่างยังไม่ได้ execute ครบวงจรบน deployment ของทีม

```bash
set -euo pipefail
export CVAT_BASE_URL='http://localhost:8080'
export CVAT_ORG='ptt-demo'
read -r -s -p 'CVAT PAT: ' CVAT_ACCESS_TOKEN
printf '\n'
export CVAT_ACCESS_TOKEN

api() {
  curl --fail-with-body --silent --show-error \
    --connect-timeout 10 --max-time 180 \
    -H "Authorization: Bearer $CVAT_ACCESS_TOKEN" "$@"
}
api "$CVAT_BASE_URL/api/users/self" | jq '{id,username}'
```

PAT สร้างจาก Access tokens ของบัญชี CVAT ที่ใช้ทดสอบ ต้องเป็น token ที่เขียนได้เมื่อจะ POST/PATCH ถ้าได้ 401 ตรวจ token; 403 ตรวจ membership/role อย่าใส่ Keycloak JWT แทนโดยสมมติว่ารองรับ

API reference แบบ interactive: [CVAT API Docs](https://app.cvat.ai/api/docs/) สำหรับ instance ที่ใช้งานจริงให้เปลี่ยน host เป็น `http://localhost:8080/api/docs/` หรือ `https://<cvat-host>/api/docs/` ส่วน schema ของ instance คือ `/api/schema/?scheme=json` และควรยึด schema ของ instance เป็นหลัก

## 1. สร้าง Project พร้อม Labels

```bash
PROJECT_JSON=$(api -X POST \
  "$CVAT_BASE_URL/api/projects?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' \
  --data '{"name":"API-PoC-2026-09-22","labels":[{"name":"pump","type":"rectangle"},{"name":"valve","type":"rectangle"}]}')
PROJECT_ID=$(jq -er '.id' <<< "$PROJECT_JSON")
printf 'PROJECT_ID=%s\n' "$PROJECT_ID"
```

ได้ 201 และ JSON ที่มี id เก็บ ID ลง Platform DB ทันที ถ้ามี Project ที่ labels ตรงอยู่แล้วให้ใช้ ID นั้นและข้าม POST ห้ามสร้าง Project ซ้ำทุกครั้งที่ refresh Dashboard

## 2. สร้าง Task

```bash
TASK_JSON=$(api -X POST \
  "$CVAT_BASE_URL/api/tasks?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' \
  --data "$(jq -n --argjson project "$PROJECT_ID" \
    '{name:"batch-001",project_id:$project,segment_size:20}')")
TASK_ID=$(jq -er '.id' <<< "$TASK_JSON")
printf 'TASK_ID=%s\n' "$TASK_ID"
```

Task ใน Project ใช้ labels ของ Project ไม่ส่ง labels ซ้ำใน Task บันทึก task_id ก่อนเริ่ม upload หาก request timeout ให้ตรวจผลก่อนสร้างใหม่

## 3. ส่งภาพเข้า Task — เลือกวิธีเดียว

### A. Optional Manual: ไฟล์ local (ทดสอบเร็ว)

เปลี่ยน paths ให้เป็นไฟล์จริง ไม่ใช้ร่วมกับ B ใน Task เดียวกัน:

```bash
UPLOAD_JSON=$(api -X POST \
  "$CVAT_BASE_URL/api/tasks/$TASK_ID/data?org=$CVAT_ORG" \
  -F 'image_quality=85' \
  -F 'client_files[0]=@/path/to/img-101.jpg' \
  -F 'client_files[1]=@/path/to/img-102.jpg')
RQ_ID=$(jq -er '.rq_id' <<< "$UPLOAD_JSON")
```

### B. MinIO presigned URLs

เตรียมไฟล์ private ชื่อ remote-data.json จาก Backend โดยมี URL ที่ sign จริง:

```json
{
  "image_quality": 85,
  "sorting_method": "lexicographical",
  "remote_files": [
    "https://minio.example/inspection/img-101.jpg?<real-signed-query>",
    "https://minio.example/inspection/img-102.jpg?<real-signed-query>"
  ]
}
```

```bash
UPLOAD_JSON=$(api -X POST \
  "$CVAT_BASE_URL/api/tasks/$TASK_ID/data?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' --data-binary @remote-data.json)
RQ_ID=$(jq -er '.rq_id' <<< "$UPLOAD_JSON")
```

CVAT worker ต้องเข้าถึง MinIO URL ได้ตลอดช่วงนำเข้า `remote_files` มีการดาวน์โหลดเข้า CVAT ไม่ใช่ streaming แบบไม่มีสำเนา URL หมดอายุต้อง retry อย่างมีการตรวจ Task เดิมก่อน และไม่ commit URL ที่ sign แล้วลง Git

## 4. รอ processing สำเร็จ

POST data รับงานแล้วไม่ได้แปลว่า images พร้อมทันที ใช้ rq_id ที่ได้ ไม่เดาจาก Task ID:

```bash
wait_request() {
  local request_id="$1" encoded response state attempt
  encoded=$(jq -rn --arg id "$request_id" '$id|@uri')
  for attempt in $(seq 1 120); do
    response=$(api "$CVAT_BASE_URL/api/requests/$encoded?org=$CVAT_ORG") || return 1
    state=$(jq -r '.status' <<< "$response")
    case "$state" in
      finished) printf '%s\n' "$response"; return 0 ;;
      failed) printf '%s\n' "$response" >&2; return 1 ;;
      queued|started) sleep 2 ;;
      *) printf 'Unexpected request state: %s\n' "$state" >&2; return 1 ;;
    esac
  done
  printf 'Timeout: keep rq_id and resume polling later; do not recreate task\n' >&2
  return 1
}
wait_request "$RQ_ID" | jq '{id,status,message}'
```

ตัวอย่างรอประมาณ 4 นาทีบวกเวลา HTTP ถ้าชุดใหญ่ใช้ worker ติดตามต่อในพื้นหลังและมี retry/backoff

## 5. อ่าน Jobs และ Metadata

ฟังก์ชัน list_all รวบรวมทุกหน้า โดยเรียก host ที่กำหนดเองเพื่อไม่ส่ง token ตาม next URL ไป host อื่น:

```bash
list_all() {
  local endpoint="$1" page=1 payload
  while true; do
    payload=$(api "$CVAT_BASE_URL/api/$endpoint&org=$CVAT_ORG&page_size=100&page=$page") || return 1
    jq -c '.results[]' <<< "$payload"
    if jq -e '.next == null' <<< "$payload" >/dev/null; then break; fi
    page=$((page+1))
  done
}
JOBS_JSON=$(list_all "jobs?task_id=$TASK_ID" | jq -s '.')
printf '%s\n' "$JOBS_JSON" | jq '.[]|{id,task_id,start_frame,stop_frame,type,stage,state}'
JOB_ID=$(jq -er '[.[]|select(.type=="annotation")][0].id' <<< "$JOBS_JSON")
api "$CVAT_BASE_URL/api/tasks/$TASK_ID/data/meta?org=$CVAT_ORG" > media-meta.json
```

JOB_ID เลือกงานแรกเพื่อสาธิต ถ้ามีหลาย Jobs ต้องทำครบตามขอบเขตที่จะนำผลไปใช้ ตรวจ frame metadata หลัง processing แล้วสร้าง mapping (instance,task_id,frame) → image_id ของ Platform อย่าถือว่า Task name คือชื่อภาพ หรือ index ที่ส่งเข้าเท่ากับ frame เสมอ

## 6. เปิดงานและทำ Annotation

```bash
printf '%s/tasks/%s/jobs/%s\n' "$CVAT_BASE_URL" "$TASK_ID" "$JOB_ID"
api -X PATCH "$CVAT_BASE_URL/api/jobs/$JOB_ID?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' \
  --data '{"stage":"annotation","state":"in progress"}' | jq '{id,stage,state}'
```

เปิด URL ใน browser Login ด้วยบัญชีของผู้ใช้ เลือกกล่อง pump/valve วาดและกด Save PAT ที่ Backend ถืออยู่ไม่ได้ login browser ให้โดยอัตโนมัติ หากใช้เว็บฝังของเราเปิด http://localhost:5175/platform/ แล้วกรอก Job ID

รอบนี้ไม่บังคับ assignee หรือแยกผู้ตรวจ ทุกคนที่มีสิทธิ์เท่ากันใช้ปุ่มทำงานเหมือนกัน เพื่อหลีกเลี่ยงการเขียนชนกันให้ตกลงคนทำหนึ่งคนต่อ Job ในแต่ละช่วง

## 7. ประกาศเสร็จงาน

ต้อง Save ใน editor สำเร็จก่อน เพราะ PATCH state ไม่ได้บันทึกกรอบที่ค้างใน browser

```bash
api -X PATCH "$CVAT_BASE_URL/api/jobs/$JOB_ID?org=$CVAT_ORG" \
  -H 'Content-Type: application/json' \
  --data '{"stage":"annotation","state":"completed"}' | jq '{id,stage,state}'
```

PoC นี้ใช้ annotation/completed เป็นจุดให้ Backend ดึงผล ไม่อ้างว่าผ่าน Validation/Acceptance ถ้าจะเพิ่ม QA ภายหลังจึงเพิ่ม policy อีกชั้น

กลับมาแก้: PATCH state กลับ in progress แล้ว Save ใหม่ สร้าง revision ใหม่หลังเสร็จรอบนั้น ไม่แก้ release เก่าทับ

## 8. ดึงผลเป็น JSON โดยไม่ Export ZIP

```bash
api "$CVAT_BASE_URL/api/jobs/$JOB_ID/annotations?org=$CVAT_ORG" > annotations.json
list_all "labels?task_id=$TASK_ID" | jq -s '.' > labels.json
jq '{version,shapes:(.shapes|length),tags:(.tags|length),tracks:(.tracks|length)}' annotations.json
```

ตัวอย่าง shape แบบย่อ (IDs สมมติ):

```json
{"id":501,"frame":0,"label_id":7,"type":"rectangle","points":[100,150,300,400],"rotation":0,"attributes":[]}
```

rectangle rotation=0 ใช้ xmin,ymin,xmax,ymax หน่วย pixel Backend join label_id กับ labels.json และ frame กับ manifest ของภาพ แล้วบันทึกลง DB หรือ artifact ของ revision เช่น:

```json
{"image_id":"img-101","source":{"instance":"cvat-local","task_id":55,"job_id":81,"shape_id":501},"class":"pump","geometry":{"type":"rectangle","xyxy":[100,150,300,400]},"revision_id":"revision-001"}
```

ตัวอย่างหลังแปลงเป็น contract ของ Platform ไม่ใช่ response CVAT ตรวจ shapes/tags/tracks ไม่รองรับชนิดใดให้ reject ชัดเจน ภาพไม่มีวัตถุต้องมี manifest ว่าทำแล้ว จำนวนศูนย์ไม่เท่ากับไม่เคยทำ

เมื่อดึงซ้ำให้ใช้ digest/revision ป้องกัน duplicate และสะท้อน shape ที่ลบไปด้วย ไม่ INSERT เพิ่มทุกครั้ง หากอ่านทั้ง Task ใช้ GET /api/tasks/{id}/annotations หลังตรวจว่า Jobs ในขอบเขตเสร็จครบและไม่มีการแก้ระหว่าง capture

## 9. Optional Manual: Export สำหรับ training tool

ข้ามขั้นนี้ได้หาก training อ่าน MinIO originals และ annotation revision ได้อยู่แล้ว ตรวจชื่อ format จาก GET /api/server/annotation/formats ของ instance ก่อน ตัวอย่าง COCO:

```bash
EXPORT_JSON=$(api -X POST \
  "$CVAT_BASE_URL/api/tasks/$TASK_ID/dataset/export?org=$CVAT_ORG&format=COCO%201.0&save_images=false")
EXPORT_RQ_ID=$(jq -er '.rq_id' <<< "$EXPORT_JSON")
wait_request "$EXPORT_RQ_ID" > export-request.json
jq '{status,result_url}' export-request.json
```

เมื่อ finished ดาวน์โหลดจาก result_url ที่ API คืน ไม่เดา URL เอง ถ้า relative ให้ resolve กับ CVAT_BASE_URL ถ้า absolute ตรวจ scheme/host/port ให้ตรง CVAT ก่อนแนบ PAT ถ้าเป็น storage URL ภายนอกอย่าส่ง CVAT PAT ไปด้วย

```bash
# ตั้งค่าจาก result_url หลังตรวจปลายทางแล้ว
# ตัวอย่างนี้ใช้เฉพาะ URL ที่อยู่ CVAT origin เดียวกัน
read -r -p 'Verified CVAT download URL: ' EXPORT_URL
case "$EXPORT_URL" in
  "$CVAT_BASE_URL"/*) api "$EXPORT_URL" --output annotations-export.zip ;;
  *) printf 'Download URL must match CVAT origin\n' >&2; exit 1 ;;
esac
```

save_images=false ขอ annotations package; true รวมภาพและใช้พื้นที่มากขึ้น ไม่ใช้ export เพื่อดูสถานะ ไม่ลบ Task หลัง export อัตโนมัติ

## Backend ต้องรับผิดชอบอะไรบ้าง

- persist project_id/task_id/rq_id/job_ids และ image/frame mapping
- รอ async, paginate, timeout/retry โดยไม่สร้างงานซ้ำ
- ตรวจ state ก่อน capture ผล และกั้นการแก้ระหว่าง publish revision
- polling เมื่อผู้ใช้กดเสร็จหรืออ่านเป็นระยะเพียงพอสำหรับ PoC นี้ ไม่ต้องมี Webhook ตั้งแต่วันแรก
- ถ้าเพิ่ม Webhook ภายหลังให้เป็น trigger ดึง API ไม่สมมติว่า payload มีพิกัดครบ
- 400 ตรวจ payload; 401 token; 403 role/org; 404 ID/context; 409 ตรวจ conflict; 429/5xx retry แบบจำกัด

## ขอบเขตหลักฐาน

ตรวจ endpoints/signatures กับ source workspace และแนวทาง [CVAT Server API](https://docs.cvat.ai/docs/api_sdk/api/) ตัวอย่าง curl เป็นคู่มือให้ Dev execute กับ dataset ทดสอบ ยังไม่ได้รันสร้าง Project/Task หรือเปลี่ยน roles บนระบบจริงในการจัดทำเอกสารนี้

รายละเอียด production ดู [คู่มือ Backend End-to-End](03_CVAT-MINIO-BACKEND-END-TO-END-TH.md) และ [สารบัญ](00_DOCUMENT-INDEX-TH.md)
