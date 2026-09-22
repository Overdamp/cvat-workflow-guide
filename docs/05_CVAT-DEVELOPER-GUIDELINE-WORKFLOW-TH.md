# CVAT Developer Guideline: ระบบจัดคิว Annotation, QA และ Dataset Release

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

เอกสารนี้เป็นแนวทางส่งต่อให้ Developer นำไปออกแบบและพัฒนาระบบ workflow รอบ CVAT สำหรับงานตรวจจับอุปกรณ์โรงงาน ระบบที่อธิบายยังไม่ใช่ implementation สำเร็จรูป แต่เป็นข้อกำหนดเชิงพฤติกรรม, data contract และเกณฑ์ตรวจรับ

## 1. เป้าหมายของระบบ

ระบบต้องช่วยทีมทำงานตามลำดับนี้:

```text
รับข้อมูล → แบ่งงาน → มอบหมาย Annotator → ทำ annotation
→ ส่ง QA → Reviewer ตรวจ → เปิด Issue หากผิด
→ ส่งกลับแก้ → ตรวจซ้ำ → ตรวจรับ
→ สร้าง Dataset Release → Export → Train model
```

CVAT เป็นระบบหลักสำหรับภาพ, annotations, Jobs, Issues และ Comments ส่วนระบบที่พัฒนาขึ้นจะทำหน้าที่จัดคิว, เก็บประวัติ, บังคับกติกา, แจ้งเตือน, ทำรายงาน และควบคุม Dataset Release

ห้ามออกแบบให้ Platform export ZIP ทุกครั้งที่ต้องการดูสถานะ เพราะเป็น snapshot ที่ทำให้ storage และข้อมูลซ้ำเพิ่มขึ้น ให้ใช้ Job/Issue API และ Webhook สำหรับสถานะ แล้ว export เฉพาะตอนสร้าง Dataset Release หรือส่งเข้า training

หาก edition/deployment รองรับ SSO และตั้งค่าสำเร็จ ให้เชื่อม CVAT ผ่าน OIDC SSO เพื่อให้ผู้ใช้ไม่ต้อง login ซ้ำ แต่ยังต้อง provision Organization membership, Project/Job permission และ mapping ของกลุ่มผู้ใช้แยกจากการยืนยันตัวตน ดูรายละเอียดใน [AI Platform + CVAT Architecture](01_AI-PLATFORM-CVAT-INTEGRATION-ARCHITECTURE-TH.md#31-ใช้-keycloak-ทำ-sso-ร่วมกับ-platform)

## 2. ขอบเขตข้อมูลอ้างอิง

ตัวอย่างระบบทดลองปัจจุบัน:

| รายการ | ค่า |
|---|---|
| CVAT | `http://localhost:8080` |
| Organization | `ptt-demo` |
| Project | `ptt2` (#3) |
| Task | `train` (#2) |
| Job | #2, 20 ภาพ, เฟรม 0–19 |
| Format | Ultralytics YOLO Detection 1.0 |
| Classes | 26 |
| Annotations หลัง QA | 241 |

ไฟล์ตัวอย่างที่ผ่าน import และ export:

```text
/path/to/cvat/cvat-test-20-fixed.zip
/path/to/downloads/ptt-demo.zip
```

รายงานตัวอย่าง:

```text
examples/reports/job-status-final.csv
examples/reports/export-validation.json
```

## 3. หลักการออกแบบ

### 3.1 แยก source of truth

กำหนดให้ CVAT เป็น source of truth สำหรับ:

- Project, Task และ Job
- ภาพ/เฟรม
- Labels และ annotations
- Issues และ Comments
- Assignee, Stage และ State ที่มีอยู่ใน CVAT

กำหนดให้ Workflow Service เป็น source of truth สำหรับ:

- Business status
- Priority และ due date
- Original annotator
- Reviewer ที่กำหนด
- Assignment history
- Review rounds
- Workflow events
- Dataset releases
- Training runs

อย่าแก้ข้อมูลเดียวกันในสองระบบโดยไม่มีนโยบาย sync ที่ชัดเจน

### 3.2 ใช้ CVAT ID เป็น external reference

ระบบเสริมต้องเก็บ `cvat_project_id`, `cvat_task_id` และ `cvat_job_id` เป็น reference ห้ามใช้ชื่อ Project หรือ Task เป็น key เพราะชื่อเปลี่ยนได้และอาจซ้ำกัน

### 3.3 ทุก transition ต้องตรวจสิทธิ์และบันทึกประวัติ

ทุกการเปลี่ยน Assignee, Stage, State, Issue หรือ release ต้องบันทึก actor, เวลา, ค่าเดิม, ค่าใหม่ และเหตุผลที่จำเป็น

## 4. บทบาทระบบ

| บทบาท | สิ่งที่ทำได้ |
|---|---|
| Coordinator | สร้างงาน, แจก Job, โอนงาน, ส่ง QA, ตรวจคิว |
| Annotator | แก้ annotations และตอบ Issues ของงานที่ได้รับ |
| Reviewer | ตรวจ Job, เปิด/Resolve/Reopen Issues |
| Dataset Manager | ตรวจ release และเริ่ม export/training |
| System Admin | จัดการ CVAT, ผู้ใช้, Organization และ config |

ใน CVAT `Reviewer` เป็นหน้าที่ใน workflow ไม่ใช่ Organization role โดยตรง สามารถใช้ Worker ได้ถ้าไม่ต้องแจกงานเอง

## 5. Business State Machine

ระบบเสริมควรใช้สถานะธุรกิจที่ชัดเจนและ map กับ CVAT:

```text
UNASSIGNED
    ↓ assign
ANNOTATING
    ↓ submit_for_qa
READY_FOR_QA
    ↓ reviewer_claims
REVIEWING
    ├── request_changes → CHANGES_REQUESTED
    │                          ↓ return_to_annotator
    │                      ANNOTATING
    └── approve → ACCEPTED
```

Mapping กับ CVAT ที่แนะนำ:

| Business status | CVAT Stage | CVAT State |
|---|---|---|
| `annotating` | `annotation` | `in progress` |
| `reviewing` | `validation` | `in progress` |
| `accepted` | `acceptance` | `completed` |

`Issue.resolved = true` ไม่ควรใช้แทนสถานะ Job ที่ accepted ต้องตรวจทุกภาพและทุก blocking issue ก่อน approve

### 5.1 Transition rules

| Transition | ผู้ทำ | เงื่อนไข |
|---|---|---|
| unassigned → annotating | Coordinator / auto-assign | ผู้ใช้ active และมีสิทธิ์ |
| annotating → ready_for_qa | Annotator / Coordinator | Save สำเร็จและทำครบตาม checklist |
| ready_for_qa → reviewing | Coordinator / Reviewer claim | Reviewer ได้รับมอบหมาย |
| reviewing → changes_requested | Reviewer | มี Issue ที่ต้องแก้ |
| changes_requested → annotating | Coordinator / auto-route | ต้องเก็บ annotator เดิม |
| reviewing → accepted | Reviewer + Coordinator policy | ตรวจครบ ไม่มี blocking issue |
| accepted → reviewing | Coordinator | มีการแก้ข้อมูลหรือ reopen review |

Transition ที่ไม่ผ่านเงื่อนไขต้องคืน HTTP 4xx พร้อมข้อความที่ผู้ใช้เข้าใจได้ และต้องไม่เปลี่ยนข้อมูลบางส่วนค้างไว้

## 6. Data Model ที่เสนอ

### 6.1 Work item

```sql
CREATE TABLE work_items (
    id UUID PRIMARY KEY,
    cvat_project_id BIGINT NOT NULL,
    cvat_task_id BIGINT NOT NULL,
    cvat_job_id BIGINT NOT NULL UNIQUE,
    organization_slug TEXT NOT NULL,
    original_annotator_id TEXT,
    current_assignee_id TEXT,
    reviewer_id TEXT,
    business_status TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 100,
    due_at TIMESTAMPTZ,
    review_round INTEGER NOT NULL DEFAULT 0,
    guideline_version TEXT,
    row_version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
```

ข้อกำหนด:

- `cvat_job_id` ต้อง unique
- `original_annotator_id` ห้ามถูกเขียนทับเมื่อเปลี่ยนไป reviewer
- `row_version` ใช้ optimistic locking
- `business_status` ต้องเป็น enum ที่ตรวจได้ ไม่รับ string ใด ๆ

### 6.2 Assignment history

```sql
CREATE TABLE assignment_history (
    id UUID PRIMARY KEY,
    work_item_id UUID NOT NULL REFERENCES work_items(id),
    from_user_id TEXT,
    to_user_id TEXT NOT NULL,
    changed_by TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL
);
```

### 6.3 Workflow events

```sql
CREATE TABLE workflow_events (
    id UUID PRIMARY KEY,
    event_key TEXT NOT NULL UNIQUE,
    work_item_id UUID NOT NULL REFERENCES work_items(id),
    actor_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    before_status TEXT,
    after_status TEXT,
    payload JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL
);
```

`event_key` ต้องใช้ทำ idempotency เพื่อให้ retry ไม่สร้าง event หรือ assignment ซ้ำ

### 6.4 Dataset release

```sql
CREATE TABLE dataset_releases (
    id UUID PRIMARY KEY,
    release_name TEXT NOT NULL UNIQUE,
    cvat_project_id BIGINT NOT NULL,
    source_job_ids BIGINT[] NOT NULL,
    guideline_version TEXT NOT NULL,
    image_count INTEGER NOT NULL,
    annotation_count INTEGER NOT NULL,
    class_count INTEGER NOT NULL,
    split_manifest JSONB NOT NULL,
    artifact_path TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    validation_result JSONB NOT NULL,
    approved_by TEXT NOT NULL,
    approved_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
```

ห้ามสร้าง release ถ้า validation result มี mismatch, parser failure, open blocking issue หรือ source Job ยังไม่ accepted

## 7. CVAT API Integration

ดูตัวอย่างคำสั่งที่นำไปใช้ได้ใน [คู่มือเรียก Job Status API](11_CVAT-JOB-STATUS-API-GUIDE-TH.md): ดูงานรายคน, คิว QA, Issues/Comments, PAT authentication และ Python สำหรับอ่านทุกหน้าแล้วสร้าง CSV พร้อมข้อจำกัดเรื่อง online status และเปอร์เซ็นต์ความคืบหน้า

### 7.1 Client requirements

สร้าง CVAT client กลางเพียงตัวเดียวและให้ทุก service ใช้ร่วมกัน ต้องรองรับ:

- base URL จาก environment variable
- authentication token/session ที่ไม่ hardcode
- timeout และ retry แบบ exponential backoff
- pagination
- HTTP 401/403/404/409/429/5xx
- request ID ใน log
- idempotency key ในคำสั่งเปลี่ยนสถานะ

ตัวอย่าง config:

```text
CVAT_BASE_URL=http://localhost:8080
CVAT_ORGANIZATION=ptt-demo
CVAT_TOKEN_SECRET=<secret-manager-reference>
CVAT_REQUEST_TIMEOUT_SECONDS=30
```

ห้ามใส่ token หรือ password ใน source code, CSV, application log หรือ error message ที่ส่งให้ผู้ใช้

### 7.2 Read APIs ที่ต้องใช้

ระบบควรอ่านอย่างน้อย:

```text
GET /api/projects
GET /api/projects/{id}
GET /api/tasks
GET /api/tasks/{id}
GET /api/jobs
GET /api/jobs/{id}
GET /api/jobs/{id}/annotations
GET /api/issues?job_id={id}
GET /api/requests
```

ตรวจ path และ query parameters ตาม OpenAPI ของ CVAT รุ่นที่ติดตั้งจริงก่อน implement เพราะรายละเอียดอาจเปลี่ยนระหว่างรุ่น

### 7.3 Write APIs ที่ต้องใช้

ระบบอาจต้องเรียกเพื่อ:

- เปลี่ยน Job assignee
- เปลี่ยน Stage และ State
- สร้างหรือ update Issue ตามสิทธิ์
- เริ่ม Import/Export

ทุก write ต้องทำ read-after-write หรือรับ event ยืนยันก่อนเปลี่ยน business state เป็นสำเร็จ

### 7.4 Sync strategy

เริ่มจาก polling ที่ปลอดภัยก่อน:

```text
ทุก N วินาที → อ่าน Jobs/Requests ที่เปลี่ยนหลัง cursor
              → compare กับ workflow DB
              → สร้าง event หรือ sync error
```

หากใช้ webhook ให้ตรวจว่า CVAT รุ่นที่ติดตั้งรองรับ event ที่ต้องใช้จริง และตรวจ signature/authentication ของ webhook

## 8. Queue และ Assignment

### 8.1 Auto-assignment algorithm

ขั้นตอนที่แนะนำ:

1. เลือก WorkItems ที่ status เป็น `unassigned`
2. กรองสมาชิกที่ active และมีทักษะตรงกับ label/task
3. ตัดคนที่มี conflict หรือถึง concurrency limit
4. เรียง priority สูงก่อน, due date ใกล้ก่อน, เวลารอนานก่อน
5. claim ด้วย transaction/row lock
6. เรียก CVAT เพื่อเปลี่ยน Assignee
7. ยืนยันผล แล้วบันทึก assignment history

### 8.2 ป้องกันแจกซ้ำ

การ claim ต้อง atomic ตัวอย่างเงื่อนไข:

```sql
UPDATE work_items
SET current_assignee_id = :user,
    business_status = 'claim_pending',
    row_version = row_version + 1
WHERE id = :id
  AND business_status = 'unassigned'
  AND row_version = :expected_version;
```

ถ้า affected rows เป็นศูนย์ ให้ตอบว่างานถูก claim ไปแล้ว ห้ามเรียก CVAT ซ้ำโดยคิดว่าสำเร็จ

หลัง claim ให้เก็บ command/outbox ใน transaction เดียวกัน แล้ว worker เรียก CVAT API และอ่านยืนยัน จึงเปลี่ยนเป็น `annotating` หากล้มเหลวให้คงสถานะ pending/retry หรือ sync_failed และบันทึกเหตุผล ไม่ประกาศว่ามอบหมายสำเร็จก่อน CVAT ยืนยัน ต้องเพิ่มสถานะเหล่านี้ใน state machine/validation ของ implementation ด้วย SQL นี้จองเฉพาะ local record ไม่ใช่ distributed transaction

### 8.3 Review routing

ค่าเริ่มต้น:

- Reviewer ต้องไม่ใช่ annotator เดิมถ้านโยบายแยกคนทำกับ QA
- งานแก้ส่งคืน `original_annotator_id`
- ถ้า annotator เดิม inactive ให้ Coordinator เลือกคนใหม่และบันทึกเหตุผล
- หลังแก้เสร็จ review round เพิ่มหนึ่งครั้ง

## 9. Quality Gate และ Annotation Validation

ก่อนสร้าง release ให้ตรวจอย่างน้อย:

- จำนวนภาพตรงกับ source Job
- มีภาพและ label file คู่กัน
- class IDs อยู่ในช่วงของ `data.yaml`
- bounding box อยู่ในช่วง normalize ที่ถูกต้อง
- width/height มากกว่าศูนย์
- ไม่มี annotation ที่อ้าง frame ไม่มีอยู่
- parser อ่าน archive กลับได้
- จำนวน annotations export ตรงกับ live annotations ภายใน tolerance ที่กำหนด
- ไม่มี mismatch
- ไม่มี open blocking issue
- Job อยู่ Acceptance / Completed

ตัวอย่าง JSON validation contract:

```json
{
  "parser_import_passed": true,
  "images": 20,
  "classes": 26,
  "export_annotations": 241,
  "live_shapes": 241,
  "mismatches": [],
  "issues": [{"id": 1, "frame": 1, "resolved": true}],
  "passed": true
}
```

ถ้า field ที่เป็นตัวเลขไม่ตรงหรือ `mismatches` ไม่ว่าง ให้ผลเป็น `passed = false` และหยุด release

## 10. Issue และ Review Contract

ระบบรายงานควรดึง Issue พร้อม:

```text
issue_id
cvat_job_id
frame
position
owner
comments
resolved
created_at
updated_at
```

ถ้าต้องการ severity/category ให้เก็บในระบบเสริม เช่น:

```text
wrong_class
missing_object
bad_geometry
duplicate_box
uncertain_class
```

Comment ควรกำหนด template ให้ระบุ:

```text
Frame: <number>
Problem: <what is wrong>
Action: <what to change>
Reason: <optional>
```

อย่าใช้การมี Comment เพียงอย่างเดียวเป็นหลักฐานว่าแก้แล้ว ต้องตรวจ annotation หลังแก้และเก็บ reviewer decision

## 11. Reporting API และไฟล์รายงาน

### 11.1 Job status CSV

ขั้นต่ำควรมี:

```csv
snapshot,captured_at,organization,project_id,task_id,job_id,frame_count,assignee,stage,state,open_issues,resolved_issues,annotation_count
```

`captured_at` ต้องเป็น timezone-aware ISO 8601 และทุกแถวต้องบอกว่าเป็น snapshot ช่วงใด

### 11.2 Release validation JSON

ควรมี:

```json
{
  "release_id": "ptt-equipment-v1",
  "archive": "ptt-demo.zip",
  "sha256": "...",
  "images": 20,
  "classes": 26,
  "export_annotations": 241,
  "mismatches": [],
  "parser_import_passed": true,
  "stage": "acceptance",
  "state": "completed",
  "approved_by": "reviewer01",
  "passed": true
}
```

### 11.3 Dashboard metrics

ต้องแสดงอย่างน้อย:

- จำนวน Jobs ต่อ business status
- จำนวนงานต่อ Assignee
- จำนวนงานรอ QA และอายุการรอ
- Open Issues แยกตาม Project/Task/Job
- First-pass acceptance rate
- Rework rounds
- งานเลย due date
- Release ล่าสุดและ validation result

ตัวเลข throughput ต้องใช้ event timestamps ไม่ควรคำนวณจาก snapshot สองแถวอย่างเดียว

## 12. Dataset Release และ Training Integration

Flow ที่ต้อง implement:

```text
Job accepted
  → freeze/snapshot source
  → CVAT export
  → validate archive
  → compute SHA256
  → create DatasetRelease
  → start TrainingRun
```

ห้าม train หาก:

- release ไม่ผ่าน quality gate
- class mapping เปลี่ยนโดยไม่มี version ใหม่
- มี open blocking issues
- checksum ของ artifact เปลี่ยนหลัง approval
- train/validation/test split ไม่มี manifest

Training Run ต้องอ้าง `release_id` เสมอและบันทึก model, code revision, hyperparameters, metrics และ artifact path

## 13. Security และ Reliability

- ใช้บัญชีส่วนตัวและ least privilege
- แยก CVAT token ต่อ service และเก็บใน secret manager
- ห้าม log password, token หรือข้อมูลภาพที่เป็นความลับ
- ตรวจสิทธิ์ Organization ทุกครั้งก่อนอ่าน/เขียน Job
- จำกัดชนิดไฟล์และขนาด upload
- สแกน archive ก่อนแตกไฟล์ หากระบบต้องรับไฟล์จากภายนอก
- ป้องกัน path traversal ใน ZIP
- ตั้ง timeout และจำกัด retry เพื่อไม่สร้างงานซ้ำ
- เก็บ request ID และ correlation ID ในทุก service
- ทำ backup ของ workflow DB และ artifacts
- ทำ reconciliation job ตรวจ CVAT กับ workflow DB เป็นระยะ

## 14. Acceptance Criteria

### Workflow

- [ ] Coordinator แจก Job ให้ผู้ใช้ที่ active ได้
- [ ] Worker เห็นเฉพาะงานตามสิทธิ์และ Assignee
- [ ] ส่งงานเข้า QA แล้วเปลี่ยน Assignee/Stage อย่างถูกต้อง
- [ ] ส่งกลับแก้แล้วกลับ annotator เดิม
- [ ] Reviewer เปิด Issue และ Resolve/Reopen ได้ตามสิทธิ์
- [ ] Job accepted ไม่ได้ถ้ามี blocking Issue เปิดอยู่
- [ ] การแก้หลัง accepted เปิด review ใหม่หรือ invalidate approval

### Queue

- [ ] สอง worker claim Job เดียวกันพร้อมกันแล้วสำเร็จเพียงคนเดียว
- [ ] retry ไม่สร้าง assignment ซ้ำ
- [ ] งานที่ user inactive ไม่ถูกแจก
- [ ] priority และ due date มีผลต่อการเรียงคิว
- [ ] assignment history ตรวจสอบย้อนหลังได้

### Export / Release

- [ ] Export สำเร็จมี manifest และ checksum
- [ ] Parser อ่าน ZIP กลับได้
- [ ] จำนวนภาพและ annotations ตรงกับ source
- [ ] mismatch ทำให้ release ถูก block
- [ ] release อ้างอิง Job IDs และ reviewer approval
- [ ] Training Run อ้าง release ที่ผ่านแล้วเท่านั้น

### Reliability

- [ ] CVAT 401/403/404/409/429/5xx ถูกจัดการชัดเจน
- [ ] timeout มีสถานะ sync failed ให้ผู้ดูแลเห็น
- [ ] worker restart ไม่ทำ event ซ้ำ
- [ ] reconciliation ตรวจพบข้อมูล CVAT กับ local DB ไม่ตรง
- [ ] audit log มี actor, action, before/after และ timestamp

## 15. แผนพัฒนาเป็นระยะ

### Phase 1: Read-only reporting

ดึง Jobs, Issues และ Requests มาทำ Dashboard และ CSV ก่อน ยังไม่ทำ auto-assignment เพื่อลดความเสี่ยงข้อมูลผิด

### Phase 2: Controlled workflow

เพิ่ม state machine, assignment history, ปุ่ม Submit for QA, Return for correction และ Approve พร้อมตรวจสิทธิ์

### Phase 3: Quality gate และ release

เพิ่ม export validator, checksum, release manifest และ approval snapshot

### Phase 4: Automation

เพิ่ม auto-assignment, QA routing, notifications และ reconciliation

### Phase 5: Training loop

เชื่อม Dataset Release กับ training, validation, model registry และ active learning

## 16. สิ่งที่ต้องทดสอบซ้ำเมื่ออัปเกรด CVAT

- OpenAPI path และ query parameters
- รูปแบบ response ของ Jobs, annotations และ Issues
- Organization permission
- Import/export format และ YAML compatibility
- Stage/State transition
- Review workspace และ Comment behavior
- Requests และ worker failure handling

ให้ใช้ชุด 20 ภาพเป็น smoke test ก่อนนำการเปลี่ยนแปลงไปใช้กับ dataset ใหญ่

## 17. สรุป implementation contract

Developer ควรส่งมอบระบบที่ทำให้ลำดับนี้ตรวจสอบได้:

```text
CVAT Job
  ↕
WorkItem + AssignmentHistory + WorkflowEvents
  ↕
Queue / QA / Dashboard
  ↕
DatasetRelease + ValidationManifest
  ↕
TrainingRun + ModelArtifact
```

ข้อกำหนดที่สำคัญที่สุดคือไม่อนุมัติ dataset จากค่า `Completed` เพียงอย่างเดียว ต้องตรวจ annotations, Issues, export artifact, checksum และประวัติ reviewer ให้ครบก่อนสร้าง release ทุกครั้ง
