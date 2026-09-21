# ดูแลและเพิ่มคู่มือ

## แหล่งหลัก

แก้เอกสารใน repository นี้เท่านั้น โฟลเดอร์ /home/luke/cvat/docs ของเครื่องทดลองเป็นลิงก์นำทาง สำเนาเก่าที่เก็บสำรองไม่ใช่คู่มือปัจจุบัน

## สารบัญอัตโนมัติ

หลัง clone ให้ตั้งค่าครั้งเดียว (ตรวจ existing hook ก่อนหากเครื่องมี hook อื่น):

```bash
git config core.hooksPath .githooks
```

ก่อน commit hook จะสแกน Markdown ทั้ง repository สร้าง DOCS-INDEX.md และ stage สารบัญให้ ไฟล์ใหม่ที่ไม่รู้หมวดอยู่กลุ่มเอกสารอื่น โดยไม่ต้องแก้สคริปต์ หากต้องการจัดหมวดเฉพาะให้เพิ่มใน KNOWN ของสคริปต์

สร้างสารบัญทันทีหลังเพิ่มไฟล์:

```bash
python3 scripts/update_docs_index.py
```

ตรวจว่าสารบัญตรงกับไฟล์ (GitHub Actions ใช้คำสั่งนี้):

```bash
python3 scripts/update_docs_index.py --check
```

CI ตรวจและแจ้งความคลาดเคลื่อน ไม่ commit แทนผู้เขียน ถ้าเพิ่มไฟล์ผ่าน GitHub UI ต้องสร้างสารบัญจาก checkout และ commit ให้ครบก่อน merge การสร้างสารบัญไม่ได้ตรวจสอบความถูกต้องทางเทคนิคของเนื้อหา

hook อ่าน working tree; stage ไฟล์คู่มือที่ต้องการเผยแพร่พร้อมสารบัญ หลีกเลี่ยงมี Markdown ใหม่ที่ยังไม่ต้องการ commit ค้างอยู่ เพราะลิงก์ในสารบัญจะชี้ไปยังไฟล์นั้นด้วย CI จะตรวจความไม่ตรงกันใน checkout

## กติกาเนื้อหา

- ระบุวันที่/version และแยกผลทดลองออกจากสถานะสด
- คู่มือ Backend End-to-End เป็นแหล่งหลักของ API/SDK/MinIO/Auth/DB
- Architecture อธิบายภาพรวม; Integration Guide อธิบาย consistency; Operations อธิบายขั้นตอนคน
- อ้างลิงก์ไปหัวข้อหลักแทนคัดลอกตัวอย่าง config หลายฉบับ
- ระบุว่าโค้ดเป็นตัวอย่างหรือทดสอบจริงแล้วในขอบเขตใด
- เก็บประวัติใน docs/archive และรักษาลิงก์ย้ายสำหรับ URL เดิม
- Export ไม่ใช่ status sync; SSO ไม่เท่ากับ API token delegation
