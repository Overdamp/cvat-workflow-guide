# คู่มือปฏิบัติการ CVAT: Workflow Annotation และ QA

คู่มือนี้สรุป workflow ที่ทดลองจริงกับ CVAT สำหรับทีมตรวจจับอุปกรณ์โรงงาน ตั้งแต่เตรียมผู้ใช้จนถึง export dataset และรายงานสถานะ

## 1. ขอบเขตและตัวอย่างที่ใช้

ระบบทดลองเปิดที่ `http://localhost:8080` และใช้ข้อมูลดังนี้:

| รายการ | ค่า |
|---|---|
| Organization | `ptt-demo` |
| Project | `ptt2` (#3) |
| Task | `train` (#2) |
| Job | #2, เฟรม 0–19, รวม 20 ภาพ |
| Format | Ultralytics YOLO Detection 1.0 |
| Labels | 26 classes |

บัญชีตัวอย่าง:

| Username | หน้าที่ | Organization role |
|---|---|---|
| `admin2` | Owner / Coordinator | Owner |
| `annotator01` | ทำและแก้ annotation | Worker |
| `annotator02` | รับงาน annotation เพิ่ม | Worker |
| `reviewer01` | QA, Issue และตรวจรับ | Worker |

รหัสผ่าน `<YOUR_TEST_PASSWORD>` ใช้เฉพาะเครื่องทดลอง ควรใช้รหัสส่วนตัวในระบบจริง

## 2. โครงสร้างข้อมูล

```text
Project → Task → Job → ภาพ/เฟรม → Annotation
                                  └→ Issue → Comment
```

Project รวมงานที่ใช้ labels และ guideline เดียวกัน Task คือชุดภาพหนึ่งชุด Job คือส่วนที่มอบหมายให้คนทำหรือคนตรวจ และ Job หนึ่งมีหลายภาพได้ ดังนั้นข้อความ `1 total` บนหน้า Project อาจหมายถึง 1 Job ไม่ใช่ 1 ภาพ

## 3. หน้าที่ของแต่ละคน

### Owner / Coordinator (`admin2`)

สร้าง Organization, Project, Task และ Job, เชิญสมาชิก, ย้าย Project เข้า Organization, กำหนด Assignee/Stage/State, ส่งงานระหว่าง annotator กับ reviewer, ตรวจสถานะ และเริ่ม export

### Annotator (`annotator01`, `annotator02`)

เปิด Job ที่ได้รับมอบหมาย ตรวจหรือสร้างกรอบ, เปลี่ยน label, ลบกรอบที่ผิด, Save และตอบ Issue หลังแก้ไข

### Reviewer / QA (`reviewer01`)

ตรวจทุกภาพใน Review workspace, เปิด Issue บนจุดผิด, เขียน Comment, ตรวจซ้ำ และกด Resolve หรือ Reopen

Reviewer เป็นหน้าที่ของ workflow ไม่ใช่ Organization role ที่ชื่อ Reviewer โดยตรง Worker ใช้ทำ QA ได้ถ้าไม่ต้องแจกงาน

## 4. การตั้งค่าทีมครั้งแรก

1. Login ด้วย `admin2`
2. คลิกชื่อผู้ใช้มุมขวาบน → **Organization → + Create**
3. ตั้งชื่อ เช่น `ptt-demo` แล้ว Submit
4. เข้า Organization → **Invite members**
5. เพิ่ม annotator และ reviewer เป็น Worker
6. ให้สมาชิก login เปิด **Invitations** และรับคำเชิญ
7. ทุกคนเลือก Organization `ptt-demo` จากเมนูผู้ใช้
8. ย้าย Project เข้า Organization ผ่าน Project → **Actions → Move**
9. ตรวจ Task และ Job หลังย้าย เพราะการย้าย workspace อาจต้องมอบหมายงานใหม่

ถ้าไม่เลือก Organization ผู้ใช้จะอยู่ Personal workspace และอาจไม่เห็น Project ของทีม

## 5. นำเข้า YOLO dataset

ใช้ **Project → Actions → Import dataset** เมื่อ ZIP มีภาพ, labels และ `data.yaml` ส่วน Create task ใช้เมื่อมี source ภาพหรือวิดีโอที่ยังไม่มี annotations

โครงสร้างที่แนะนำ:

```text
dataset.zip
├── data.yaml
└── train/
    ├── images/image001.jpg
    └── labels/image001.txt
```

ชื่อ stem ต้องตรงกัน (`image001.jpg` กับ `image001.txt`) และ `data.yaml` ต้องมี `names` ครบตาม class IDs `labels.cache` เป็น cache ชั่วคราว ไม่จำเป็นต่อ CVAT และควรไม่นำเข้าใน ZIP

ชุดทดสอบที่ผ่านการตรวจ parser แล้วอยู่ที่:

```text
/path/to/cvat/cvat-test-20-fixed.zip
```

มี 20 ภาพ, 20 labels และ 26 classes การทดสอบชุดเล็กควรทำก่อน import ZIP ขนาดใหญ่เสมอ

## 6. สถานะที่ทีมใช้

| ความหมาย | Stage | State |
|---|---|---|
| Annotator กำลังทำ | Annotation | In progress |
| QA กำลังตรวจ | Validation | In progress |
| ผ่านการตรวจรับ | Acceptance | Completed |

Issue มีสถานะของตัวเอง `Open → แก้ไข → ตรวจซ้ำ → Resolve` ถ้ายังผิดให้ `Reopen` การ Resolve ปิดเฉพาะ Issue ไม่ได้ทำให้ Job ผ่านโดยอัตโนมัติ

## 7. Workflow หลัก

```text
Coordinator แจก Job
        ↓
Annotator ตรวจ/แก้ annotations และ Save
        ↓
Coordinator ส่งให้ Reviewer (Validation)
        ↓
Reviewer ตรวจทุกภาพ
   ├─ พบปัญหา: Issue + Comment → ส่งกลับ Annotator
   │                              ↓
   │                    แก้ + Save + ตอบ Comment
   │                              ↓
   │                    Reviewer ตรวจซ้ำ
   │                    ├─ ยังผิด: Reopen
   │                    └─ ถูก: Resolve
   └─ ผ่านครบ → Acceptance / Completed
                         ↓
                    Export release
```

### 7.1 Coordinator แจกงาน

ในหน้า Jobs เลือก Job แล้วตั้ง `Assignee = annotator01`, `Stage = Annotation`, `State = In progress` จากนั้นบันทึก ถ้ามีหลายคนให้แบ่งเป็นหลาย Jobs และเก็บคนทำเดิมไว้ในตาราง workflow เสริม

### 7.2 Annotator ทำงาน

1. Login ด้วยบัญชีของตนเองและเลือก `ptt-demo`
2. เปิดเมนู Jobs หรือ URL `/tasks/<task_id>/jobs/<job_id>`
3. ตรวจทุกเฟรมว่ามีวัตถุครบ, class ถูก และกรอบพอดี
4. ปรับกรอบด้วยจุดมุมหรือลากย้าย
5. เปลี่ยน label เมื่อ class ผิด
6. ใช้ Rectangle สร้างกรอบใหม่เมื่อวัตถุตกหล่น
7. ลบกรอบซ้ำหรือกรอบที่ไม่มีวัตถุ
8. กด **Save** เป็นระยะและก่อนส่งตรวจ
9. แจ้ง Coordinator ว่าพร้อม QA

ถ้าไม่แน่ใจให้จดเลขเฟรมและถามผ่าน Issue แทนการเดา โดยเฉพาะคลาสวาล์วที่คล้ายกัน

### 7.3 Coordinator ส่ง QA

หลัง annotator Save แล้ว ให้เปลี่ยน `Assignee = reviewer01`, `Stage = Validation`, `State = In progress` การส่งงานไม่เกิดขึ้นอัตโนมัติเมื่อ annotator กด Save

### 7.4 Reviewer ตรวจ

1. Login `reviewer01` และเลือก `ptt-demo`
2. เปิด Job ที่ได้รับมอบหมาย
3. เลือก Review workspace
4. ตรวจทุกภาพ ไม่ใช่เฉพาะ thumbnail
5. ตรวจ completeness, class, geometry และ consistency
6. หากพบปัญหาเลือก **Open an issue** แล้วคลิก/ลากบริเวณนั้น
7. เขียน Comment ที่ระบุ `เฟรม + สิ่งผิด + วิธีแก้`

ตัวอย่าง:

```text
Frame 7: เกจด้านขวาเป็นหน้าปัดเข็ม
กรุณาเปลี่ยน digital-gauge เป็น analog-gauge
และปรับกรอบให้ชิดขอบหน้าปัด
```

### 7.5 ส่งกลับแก้

Coordinator เปลี่ยน Assignee กลับเป็น annotator เดิมและ Stage เป็น Annotation โดยไม่ลบ Issue Annotator เปิด Issue อ่าน Comment แก้ annotation, Save และตอบว่าแก้แล้ว จากนั้น Coordinator ส่งกลับ reviewer และเปลี่ยนเป็น Validation

Annotator ไม่ควรกด Resolve เอง เพราะ reviewer ต้องตรวจซ้ำก่อนปิด Issue

### 7.6 ตรวจรับ

Reviewer ตรวจจุดเดิมและภาพที่เหลือ เมื่อถูกต้องกด **Resolve** ทุก Issue ที่แก้เสร็จ แล้วแจ้ง Coordinator จากนั้น Coordinator ตรวจว่าไม่มี blocking Issue และตั้ง `Stage = Acceptance`, `State = Completed`

## 8. ตัวอย่างรอบที่ทำจริง

```text
เริ่ม: Job #2 → annotator01 / Annotation / In progress
QA: reviewer01 / Validation / In progress
พบ: Issue #1 ที่ frame 1
แก้: annotator01 แก้และตอบ Comment
ตรวจซ้ำ: reviewer01 Resolve Issue #1
จบ: Job #2 → Acceptance / Completed
```

ผลหลังรอบนี้คือ Job มี 20 ภาพ, 241 annotations และ Issue 1 จุดที่ `resolved = true`

## 9. การจัดคิวหลายคน

CVAT จัดคิว import/export ให้ worker อัตโนมัติ แต่คิวงานคนต้องกำหนดเองผ่าน UI หรือพัฒนาระบบผ่าน API

ตัวอย่างตารางคิว:

| Job | คนทำเดิม | ผู้รับผิดชอบปัจจุบัน | ขั้นตอน | Priority |
|---|---|---|---|---|
| #101 | annotator01 | annotator01 | กำลังทำ | สูง |
| #102 | annotator02 | reviewer01 | รอ QA | ปกติ |
| #103 | annotator01 | annotator01 | ส่งกลับแก้ | สูง |

เมื่อระบบใหญ่ขึ้นควรเก็บ `original_annotator`, reviewer, priority, due date, review round และ assignment history ในระบบเสริม กติกาคิวที่ควรมีคือแจกตามทักษะและงานค้าง, ส่งงานแก้คืนเจ้าของเดิม, ป้องกันสองคน claim Job เดียวกัน และบันทึกทุก transition

## 10. Export dataset ผ่าน UI

เมื่อ QA ผ่านและ Job เป็น Acceptance / Completed:

1. Login ผู้มีสิทธิ์ เช่น `admin2`
2. เปิด Project `ptt2` ใน Organization `ptt-demo`
3. เลือก **Actions → Export dataset**
4. เลือก **Ultralytics YOLO Detection 1.0**
5. เปิด **Save images** หากต้องการภาพใน ZIP
6. กดยืนยัน
7. ไปหน้า **Requests** และรอจนสำเร็จ
8. ดาวน์โหลด ZIP

CVAT ไม่ได้ export ตาราง workflow เป็น CSV แบบรวมโดยอัตโนมัติ หน้า Jobs/Requests ใช้ดูสถานะได้ ส่วนรายงานที่รวม Assignee, Stage, State และ Issues ต้องดึง API หรือสร้าง service เพิ่ม

ไฟล์ที่ export และตรวจแล้ว:

```text
/path/to/downloads/ptt-demo.zip
```

ผลตรวจ: 20 images, 20 label files, 26 classes, 241 annotations, parser import ผ่าน และตรงกับ live annotations ทั้งหมด

## 11. Export รายงานสถานะ

รายงานเป็น snapshot สร้างใหม่เมื่อสถานะเปลี่ยน ไม่อัปเดตเอง:

- [CSV สถานะก่อน/หลังส่ง QA](../examples/reports/job-status-before-after.csv)
- [CSV สถานะหลังตรวจรับ](../examples/reports/job-status-final.csv)
- [JSON ผลตรวจ ZIP](../examples/reports/export-validation.json)

ตัวอย่างข้อมูล:

```csv
job_id,assignee,stage,state,open_issues,resolved_issues
2,reviewer01,acceptance,completed,0,1
```

Comment, assignment history และประวัติ QA ไม่ติดไปกับไฟล์ YOLO ต้องเก็บรายงานแยก

## 12. Checklist การทำงาน

### ก่อนเริ่ม

- [ ] ผู้ใช้ทุกคนมีบัญชีแยกและเลือก Organization ถูกต้อง
- [ ] Project อยู่ใน Organization
- [ ] labels และ guideline เป็นรุ่นเดียวกัน
- [ ] Task/Job มีภาพครบและมี Assignee

### ก่อนส่ง QA

- [ ] Annotator ตรวจครบทุกเฟรม
- [ ] กด Save สำเร็จ
- [ ] Coordinator เปลี่ยนเป็น reviewer / Validation

### ก่อนตรวจรับ

- [ ] Reviewer ตรวจทุกภาพ
- [ ] Issue มีคำอธิบายชัด
- [ ] Issue ที่แก้ถูกตรวจซ้ำและ Resolve
- [ ] ไม่มี blocking Issue เปิดอยู่

### ก่อน release

- [ ] Job เป็น Acceptance / Completed
- [ ] ตรวจจำนวนภาพ, labels และ class mapping
- [ ] ดาวน์โหลด ZIP และทดสอบอ่านกลับ
- [ ] เก็บ CSV/JSON คู่กับ ZIP
- [ ] บันทึก release ID, guideline version และ checksum

## 13. กรณีปัญหาที่พบบ่อย

`A task must contain at least one file` หมายถึงหน้า Create task ยังไม่มีไฟล์ที่ browser รับไว้ ให้ตรวจว่าชื่อไฟล์แสดงก่อน Submit

`The file is required` ทั้งที่เลือกไฟล์แล้วอาจเกิด Ubuntu file portal timeout ตรวจด้วย:

```bash
journalctl --user --since '30 minutes ago' --no-pager \
  -u xdg-desktop-portal -u xdg-document-portal
```

ถ้าพบ `Failed to register ... Timeout was reached` ปิด dialog แล้วใช้:

```bash
systemctl --user restart xdg-document-portal.service xdg-desktop-portal.service
```

`'int' object is not iterable` ระหว่าง import ให้ดู:

```bash
docker compose logs --tail 200 cvat_worker_import
```

ตรวจ YAML และโครงสร้าง archive ใช้ชุดเล็กทดสอบก่อนชุดใหญ่เสมอ

## 14. แนวทางระบบต่อยอด

แยกความรับผิดชอบให้ชัด: CVAT เป็นแหล่งหลักของภาพ, annotations, Jobs และ Issues ส่วน workflow service เก็บ priority, due date, คนทำเดิม, routing, assignment history และ business status

สถานะธุรกิจที่แนะนำคือ `Unassigned → Annotating → ReadyForQA → Reviewing → ChangesRequested → Accepted` ระบบเสริมควร claim งานแบบ atomic, retry API แบบไม่สร้างงานซ้ำ, บันทึก event และแจ้ง sync failure

เมื่อสร้าง Dataset Release ให้เก็บ Job IDs, จำนวนภาพ/annotations, class mapping, guideline version, train/val/test split, checksum, reviewer approval และ Training Run ที่ใช้ release นั้น

## 15. ลำดับใช้งานครั้งต่อไป

```text
admin2 ตรวจงานและแจก Job
→ annotator ตรวจ/แก้และ Save
→ admin2 ส่ง reviewer / Validation
→ reviewer ตรวจและเปิด Issue ถ้าจำเป็น
→ annotator แก้/ตอบ
→ reviewer ตรวจซ้ำและ Resolve
→ admin2 ตั้ง Acceptance / Completed
→ admin2 Export dataset ผ่าน UI
→ ตรวจ ZIP และสร้างรายงาน CSV/JSON
→ สร้าง release ก่อนนำไป train model
```

เมื่ออัปเกรด CVAT หรือเปลี่ยน dataset ให้ทำรอบทดสอบ 20 ภาพซ้ำ โดยตรวจสิทธิ์, import, Issue, state transition และ export ก่อนใช้กับข้อมูลจำนวนมาก
