# ตัวอย่างรายงานจาก CVAT Workflow

ไฟล์เหล่านี้เป็น snapshot สำหรับศึกษาโครงสร้างรายงานที่ระบบเสริมสร้างขึ้น ไม่ใช่ export format มาตรฐานที่ CVAT UI มีปุ่มให้ดาวน์โหลดโดยตรง และไม่ใช่ฐานข้อมูล production

ระบบ production ควรอ่านสถานะและ annotation ผ่าน REST API/SDK แล้วเขียนลง Platform Database หรือ reporting store ตาม schema/version ของระบบ ส่วน CSV/JSON เหล่านี้เป็น **Optional Manual Flow** ใช้เป็นตัวอย่าง, validation evidence, debug output หรือ fixture สำหรับทดสอบเท่านั้น

| ไฟล์ | จุดประสงค์ |
|---|---|
| job-status-before-after.csv | เทียบ Assignee/Stage ก่อนและหลังส่ง QA |
| job-status-final.csv | สถานะหลังตรวจรับพร้อมจำนวนภาพ กรอบ และ Issues |
| export-validation.json | ผลเปรียบเทียบ export กับข้อมูล Job ณ เวลาทดสอบ |

## CSV fields

| Field | ความหมาย |
|---|---|
| snapshot | ชื่อช่วงที่เก็บข้อมูล |
| captured_at | เวลาอ่าน snapshot แบบ ISO 8601 มี timezone |
| organization | Organization slug |
| project_id / task_id / job_id | CVAT resource IDs ภายใน instance |
| project / task | ชื่อที่อ่านได้ ณ เวลานั้น (มีในรายงานก่อน/หลัง) |
| start_frame / stop_frame | ช่วงเฟรมแบบรวมปลายทั้งสอง (มีในรายงานก่อน/หลัง) |
| frame_count | 20 ภาพใน Job ตัวอย่าง |
| assignee | ผู้รับผิดชอบปัจจุบัน ไม่ใช่ประวัติผู้ทำทั้งหมด |
| stage / state | สถานะ CVAT ณ เวลาอ่าน |
| open_issues / resolved_issues | จำนวน Issues ตามสถานะ |
| annotation_count | 241 กรอบในรายงานสุดท้าย |

สอง CSV มี schema ต่างกันตามจุดที่เก็บข้อมูล ระบบ production ควรกำหนด schema version และ normalize fields ก่อนรวม ไม่ใช่ต่อไฟล์ด้วยข้อความอย่างเดียว

## JSON validation fields

| Field | ความหมาย |
|---|---|
| archive | path ตัวอย่างของ exported artifact |
| sha256 | placeholder; ต้องคำนวณจาก ZIP ของตนเอง |
| images | จำนวนภาพที่ตรวจ |
| classes | จำนวน class definitions ไม่ใช่จำนวน classes ที่พบจริงในภาพ |
| export_annotations / live_shapes | จำนวนกรอบใน export และ Job ณ snapshot |
| mismatches | ความไม่ตรงกันของข้อมูลที่ตรวจ |
| max_coordinate_error_pixels | ค่าคลาดเคลื่อนสูงสุดจากการแปลง/ปัดเศษในรอบตรวจนี้ |
| parser_import_passed | archive อ่านกลับด้วย parser ได้ |
| stage / state | สถานะงานตอนตรวจ |
| issues | Issue ID, frame และสถานะ resolved |

ค่า images/annotations และผล validation มาจากรอบทดลอง แต่ path และ checksum ถูกแทนด้วย placeholder ไม่ได้แนบภาพหรือ ZIP ต้นฉบับ จึงไม่สามารถใช้ไฟล์นี้พิสูจน์ checksum ของ artifact ที่ดาวน์โหลดจากที่อื่นได้

## ตัวอย่างการใช้

1. Developer อ่าน CSV เป็นตาราง dashboard
2. รวมด้วย instance ID + Job ID และแปลง timezone ให้สอดคล้องกัน
3. ใช้ JSON ออกแบบ validation manifest สำหรับ release
4. เพิ่ม schema_version, source revision, approval record และเวลาเหตุการณ์จริงในระบบใหม่

Snapshots เหล่านี้ไม่พอคำนวณชั่วโมงทำงานจริงหรือประวัติการส่งกลับแก้ ต้องเก็บ events เพิ่ม การไม่มี mismatch พิสูจน์เพียงความตรงกันของ export ที่ตรวจ ไม่ใช่คุณภาพเชิงเนื้อหาของ annotations
