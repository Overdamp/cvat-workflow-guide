# CVAT Database Schema และแนวทาง Monitoring สำหรับ Developer

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

## 1. Database กับ API ใช้คนละวัตถุประสงค์

CVAT มี PostgreSQL database ที่เก็บข้อมูลภายใน เช่น users, projects, tasks, jobs, labels, annotations, issues และ comments สามารถเข้าไปดู schema และ monitor ได้ แต่ database ภายในไม่ควรเป็น integration contract ของระบบธุรกิจ เพราะตารางและชื่อ column อาจเปลี่ยนเมื่อ upgrade

บริบทที่ตรวจเมื่อ 17 กันยายน 2026 คือ CVAT 2.75.1 บน Docker Compose โดย health endpoint ตรวจได้ว่า cache, database และ OPA ทำงานปกติ ณ เวลาตรวจสอบ การมี PostgreSQL ของ CVAT ไม่ได้หมายความว่า Platform ควรใช้ฐานนี้เป็นฐานข้อมูลหลักของตนเอง

แนวทางที่ควรใช้:

| เป้าหมาย | วิธีที่เหมาะสม |
|---|---|
| Platform integration | REST API / Python SDK / Webhook |
| Dashboard สดของงาน | API + Webhook + reconciliation |
| DBA monitoring / incident response | PostgreSQL read-only connection |
| ตรวจ migration และ index | Database read-only |
| แก้ข้อมูลธุรกิจ | CVAT UI หรือ API ที่มีสิทธิ์ ไม่แก้ SQL ตรง |

## 2. Schema ที่ตรวจในเครื่องทดลอง

ตัวอย่าง CVAT ใช้ database `cvat` และ PostgreSQL container `cvat_db` มี schema `public` และตารางประมาณ 71 ตาราง ตารางที่เกี่ยวข้องกับ workflow ได้แก่:

```text
auth_user
organizations_organization
organizations_membership
engine_project
engine_task
engine_segment
engine_job
engine_label
engine_labeledshape
engine_labeledtrack
engine_issue
engine_comment
webhooks_webhook
webhooks_webhookdelivery
django_migrations
```

ชื่อตารางสะท้อน Django app และอาจเปลี่ยนตามรุ่น ห้ามเขียน code ที่ถือว่ารายการนี้คงที่โดยไม่ตรวจ migration/version

## 3. ดู schema ผ่าน Docker

คำสั่งต่อไปนี้เป็น read-only และเหมาะกับ self-hosted Docker Compose:

```bash
docker compose exec -T cvat_db \
  psql -U root -d cvat -c '\\dn' -c '\\dt'
```

ดูโครงสร้าง Job:

```bash
docker compose exec -T cvat_db \
  psql -U root -d cvat -c '\\d+ engine_job'
```

ดูโครงสร้าง Issue และ Comment:

```bash
docker compose exec -T cvat_db \
  psql -U root -d cvat \
  -c '\\d+ engine_issue' \
  -c '\\d+ engine_comment'
```

ดู foreign keys และ index ของทุกตาราง:

```bash
docker compose exec -T cvat_db \
  psql -U root -d cvat -c '\\d+ engine_task' -c '\\d+ engine_project'
```

ดู columns แบบ query ที่นำไปทำ schema inventory ได้:

```bash
docker compose exec -T cvat_db psql -U root -d cvat -c '
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = ''public''
ORDER BY table_name, ordinal_position;'
```

## 4. ดูข้อมูล workflow ปัจจุบัน

Query นี้อ่าน Project → Task → Job → user และ Issues โดยไม่แก้ข้อมูล:

```bash
docker compose exec -T cvat_db psql -U root -d cvat -c '
SELECT
    p.id AS project_id,
    p.name AS project,
    t.id AS task_id,
    t.name AS task,
    j.id AS job_id,
    u.username AS assignee,
    j.stage,
    j.state,
    j.status,
    j.start_frame,
    j.stop_frame,
    j.updated_date,
    COUNT(i.id) FILTER (WHERE i.resolved = false) AS open_issues,
    COUNT(i.id) FILTER (WHERE i.resolved = true) AS resolved_issues
FROM engine_job j
JOIN engine_segment s ON s.id = j.segment_id
JOIN engine_task t ON t.id = s.task_id
LEFT JOIN engine_project p ON p.id = t.project_id
LEFT JOIN auth_user u ON u.id = j.assignee_id
LEFT JOIN engine_issue i ON i.job_id = j.id
GROUP BY p.id, p.name, t.id, t.name, j.id, u.username,
         j.stage, j.state, j.status, j.start_frame,
         j.stop_frame, j.updated_date
ORDER BY j.id;'
```

หมายเหตุ: field `start_frame` และ `stop_frame` อยู่ใน `engine_segment` ในบางรุ่น ไม่ใช่ `engine_job` เสมอไป หาก query ใช้ไม่ได้ ให้เอาสอง column นี้ออกหรือเลือกจาก `s.start_frame, s.stop_frame` ตาม `\\d+ engine_segment` ของรุ่นจริง

Query ที่ปรับตาม schema ที่ตรวจในเครื่องนี้:

```bash
docker compose exec -T cvat_db psql -U root -d cvat -c '
SELECT
    p.id AS project_id, p.name AS project,
    t.id AS task_id, t.name AS task,
    j.id AS job_id, u.username AS assignee,
    j.stage, j.state, j.status,
    s.start_frame, s.stop_frame,
    j.updated_date,
    COUNT(i.id) FILTER (WHERE i.resolved = false) AS open_issues,
    COUNT(i.id) FILTER (WHERE i.resolved = true) AS resolved_issues
FROM engine_job j
JOIN engine_segment s ON s.id = j.segment_id
JOIN engine_task t ON t.id = s.task_id
LEFT JOIN engine_project p ON p.id = t.project_id
LEFT JOIN auth_user u ON u.id = j.assignee_id
LEFT JOIN engine_issue i ON i.job_id = j.id
GROUP BY p.id, p.name, t.id, t.name, j.id, u.username,
         j.stage, j.state, j.status,
         s.start_frame, s.stop_frame, j.updated_date
ORDER BY j.id;'
```

## 5. ตรวจจำนวน annotations

CVAT แยก annotations ตามชนิด shape/track/tag ตารางจึงต้องนับแยก:

```bash
docker compose exec -T cvat_db psql -U root -d cvat -c '
SELECT
    j.id AS job_id,
    COUNT(DISTINCT ls.id) AS labeled_shapes,
    COUNT(DISTINCT lt.id) AS labeled_tracks
FROM engine_job j
LEFT JOIN engine_labeledshape ls ON ls.job_id = j.id
LEFT JOIN engine_labeledtrack lt ON lt.job_id = j.id
GROUP BY j.id
ORDER BY j.id;'
```

สำหรับรายงานที่เชื่อถือได้ควรอ่าน annotations ผ่าน `GET /api/jobs/{id}/annotations` แล้วนับตาม response ด้วย เพราะ API อาจรวม logic ของ shape, track, interpolation และ permission ให้เหมาะกับรุ่นนั้น

## 6. ตรวจสมาชิก Organization

```bash
docker compose exec -T cvat_db psql -U root -d cvat -c '
SELECT
    o.slug AS organization,
    u.username,
    m.role,
    m.is_active,
    m.joined_date
FROM organizations_membership m
JOIN organizations_organization o ON o.id = m.organization_id
JOIN auth_user u ON u.id = m.user_id
ORDER BY o.slug, u.username;'
```

ข้อมูลนี้ใช้ monitor สมาชิกได้ แต่การเปลี่ยน role ควรทำผ่าน CVAT UI/API เพื่อให้ permission logic และ audit ที่ CVAT จัดการทำงานครบ

## 7. Query สำหรับ monitoring

### งานที่ไม่มีผู้รับผิดชอบ

```sql
SELECT j.id, t.name AS task, j.stage, j.state
FROM engine_job j
JOIN engine_segment s ON s.id = j.segment_id
JOIN engine_task t ON t.id = s.task_id
WHERE j.assignee_id IS NULL;
```

### งานที่รอ QA

```sql
SELECT j.id, u.username AS assignee, j.updated_date
FROM engine_job j
LEFT JOIN auth_user u ON u.id = j.assignee_id
WHERE j.stage = 'validation'
  AND j.state = 'in progress'
ORDER BY j.updated_date;
```

### งานที่มี Issue เปิด

```sql
SELECT j.id, COUNT(i.id) AS open_issues
FROM engine_job j
JOIN engine_issue i ON i.job_id = j.id
WHERE i.resolved = false
GROUP BY j.id
ORDER BY open_issues DESC;
```

### งานที่ไม่ได้อัปเดตนาน

```sql
SELECT j.id, j.updated_date
FROM engine_job j
WHERE j.state = 'in progress'
  AND j.updated_date < NOW() - INTERVAL '24 hours'
ORDER BY j.updated_date;
```

การไม่ได้อัปเดต Job ไม่ได้แปลว่าผู้ใช้หยุดทำงานเสมอไป ผู้ใช้อาจแก้ใน browser แล้วยังไม่ Save หรือทำงานโดยไม่มีการเปลี่ยน field ของ Job จึงใช้เป็นสัญญาณเตือน ไม่ใช่หลักฐานการทำงาน

## 8. Export schema และข้อมูลเพื่อสำรวจ

Export schema อย่างเดียว:

```bash
docker compose exec -T cvat_db \
  pg_dump -U root -d cvat --schema-only \
  > cvat-schema-$(date +%Y%m%d).sql
```

Export ข้อมูลเฉพาะตารางสำหรับ debug ต้องระวังข้อมูลส่วนบุคคลและ annotations:

```bash
docker compose exec -T cvat_db \
  pg_dump -U root -d cvat --data-only \
  -t engine_project -t engine_task -t engine_job \
  > cvat-workflow-data.sql
```

อย่า commit dump ที่มี password hash, access tokens, email, ภาพ หรือข้อมูล annotation จริงลง GitHub

## 9. Read-only database account สำหรับ Developer

ใน production ไม่ควรให้ Developer ใช้ PostgreSQL superuser หรือ `root` ของ Compose ควรสร้าง role สำหรับ monitoring โดย DBA:

```sql
CREATE ROLE cvat_monitor LOGIN PASSWORD '<use-secret-manager>';
GRANT CONNECT ON DATABASE cvat TO cvat_monitor;
GRANT USAGE ON SCHEMA public TO cvat_monitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO cvat_monitor;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO cvat_monitor;
```

รหัสผ่านต้องไม่อยู่ใน Git, shell history หรือ application log ควรจำกัด network access, SSL, expiration และ rotate ตามนโยบายองค์กร `ALTER DEFAULT PRIVILEGES` มีผลกับ object ที่ role ผู้สั่งสร้างต่อไป จึงควรตั้งโดย DBA ที่เข้าใจ ownership ของ migrations

## 10. ใช้ API แทน DB ในระบบ Application

ตัวอย่างคำสั่งดูสถานะผ่าน API:

```bash
curl --fail-with-body -sS \
  --user admin2 \
  'http://localhost:8080/api/jobs?org=ptt-demo&page_size=100'
```

สำหรับ production ให้ใช้ PAT ที่มีสิทธิ์อ่าน และใช้ pagination ตาม [Job Status API Guide](11_CVAT-JOB-STATUS-API-GUIDE-TH.md) ใช้ Webhook แจ้งการเปลี่ยน แล้วทำ reconciliation จาก API เป็นระยะ

ข้อดีของ API:

- เคารพ Organization และ permission
- ใช้ representation ที่ CVAT รองรับ
- ลดการผูกกับชื่อ table/migration
- รองรับการเปลี่ยน implementation ภายใน

## 11. ข้อควรระวังในการ monitor

- Query หนักบน production อาจกระทบ CVAT; ใช้ read replica หรือ replica/export สำหรับ analytics เมื่อปริมาณมาก
- เพิ่ม index เองต้องผ่าน migration และ benchmark ไม่เพิ่มใน production แบบชั่วคราว
- อย่าใช้ `SELECT *` ใน dashboard ถ้า table มีข้อมูล annotation ขนาดใหญ่
- ใช้ pagination/aggregation และจำกัดช่วงเวลา
- แยกข้อมูล monitoring จากข้อมูลภาพและ labels ที่เป็นความลับ
- เก็บ query latency, connection count, locks, disk usage และ replication lag ในระบบ monitoring ของ PostgreSQL
- ตรวจ timezone ให้ชัดเจน ใช้ UTC ใน storage และแปลงบน UI
- ตรวจ schema หลัง upgrade ทุกครั้ง

## 12. DB monitoring ที่ควรมี

```sql
-- active connections
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;

-- long-running queries
SELECT pid, now() - query_start AS duration, state, query
FROM pg_stat_activity
WHERE query_start IS NOT NULL
ORDER BY duration DESC;

-- largest tables
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 20;
```

คำสั่งเหล่านี้เป็น PostgreSQL monitoring ไม่ใช่ CVAT workflow report โดยตรง ควรเรียกด้วย monitoring role และปกปิด query ที่อาจมีข้อมูลภายในในระบบ log

## 13. Acceptance criteria สำหรับ DB/API integration

- [ ] Application ไม่อ่านหรือเขียน CVAT PostgreSQL โดยตรง
- [ ] Developer มี read-only role แยกจาก admin
- [ ] รายงาน API ใช้ Organization context และ pagination
- [ ] Dashboard แยก snapshot จาก event history
- [ ] Webhook ตรวจ signature และรองรับ event ซ้ำ/มาช้า
- [ ] มี reconciliation หลัง CVAT restart หรือ webhook delivery fail
- [ ] Schema inventory ทำหลัง upgrade
- [ ] Query monitor ไม่ดึงภาพหรือ annotations ทั้งหมดโดยไม่จำเป็น
- [ ] ไม่มี secrets หรือข้อมูลส่วนตัวใน repository
- [ ] Dataset release อ้าง CVAT IDs, revision และ artifact checksum

## 14. สรุปสำหรับ Developer

ใช้ database เพื่อดูแลระบบ, ตรวจ schema, debug และสร้าง monitoring แบบ read-only ใช้ REST API/SDK/Webhook สำหรับ application integration ระบบที่ดีจะแยก CVAT ออกจาก workflow database, เก็บ CVAT IDs เป็น reference, รับ event อย่างปลอดภัย และใช้ API reconciliation เพื่อรับมือข้อมูลที่เปลี่ยนระหว่างการอ่าน

อ้างอิงเพิ่มเติม:

- [CVAT REST API และ SDK](https://docs.cvat.ai/docs/api_sdk/)
- [Personal Access Tokens](https://docs.cvat.ai/docs/api_sdk/access_tokens/)
- [CVAT Webhooks](https://docs.cvat.ai/docs/administration/community/advanced/webhooks/)
- [คู่มือ Job Status API](11_CVAT-JOB-STATUS-API-GUIDE-TH.md)
