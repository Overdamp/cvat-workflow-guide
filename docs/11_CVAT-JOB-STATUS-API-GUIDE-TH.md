# เรียก CVAT API เพื่อดูสถานะงานและคิว QA

← [สารบัญเอกสาร](00_DOCUMENT-INDEX-TH.md)

เอกสารนี้เป็นตัวอย่าง read-only สำหรับ Developer ใช้สร้าง Dashboard หรือรายงานจาก CVAT ตรวจรูปแบบ authentication และ filters จาก source ของรุ่นที่ใช้ในการทดลองแล้ว แต่ต้องตรวจ OpenAPI ของ deployment จริงอีกครั้งหากเปลี่ยนรุ่น

> **ขอบเขต:** CSV ที่สร้างในคู่มือนี้เป็นรายงานสถานะจาก API ไม่ใช่ dataset annotation และไม่ใช่แหล่งข้อมูลหลักของ production ควรเก็บ status/event ใน Platform Database หรือ reporting store ตาม retention policy

## 1. ข้อมูลที่อ่านได้และข้อจำกัด

| ความต้องการ | ข้อมูล |
|---|---|
| ใครรับผิดชอบ Job | assignee.username |
| ทำ annotation หรือ QA | stage |
| สถานะปัจจุบัน | state |
| Job อยู่ใน Task ใด | task_id |
| ปัญหาที่ยังค้าง | Issues API, resolved=false |
| ผู้ใช้กำลังออนไลน์ | Jobs API ไม่ได้บอก |
| ทำไปแล้วกี่ภาพ/กี่เปอร์เซ็นต์ | ต้องกำหนดและเก็บ progress เพิ่ม |
| เวลาที่ใช้ทำจริง | ต้องเก็บ events และแยก active time จาก elapsed time |

Assignee เป็นเจ้าของงานปัจจุบัน ไม่ใช่หลักฐานว่ากำลังเปิดหน้าเว็บทำงานอยู่ จำนวนกรอบไม่ใช่เปอร์เซ็นต์ความคืบหน้า และไม่มี open issues ไม่ได้ยืนยันว่าตรวจครบแล้ว

## 2. เรียกครั้งเดียวด้วย Basic authentication

ตัวอย่างสำหรับ CVAT ในเครื่องทดลอง ใช้บัญชีที่มีสิทธิ์เห็นงานของทีม:

```bash
curl --fail-with-body -sS \
  --user admin2 \
  'http://localhost:8080/api/jobs?org=ptt-demo&page_size=100'
```

curl จะถามรหัสผ่าน ไม่ต้องเขียนรหัสลงในคำสั่ง สำหรับ remote server ให้ใช้ HTTPS หาก instance ปิด Basic authentication ให้ใช้ PAT ตามหัวข้อถัดไป

ผลลัพธ์ย่อเพื่ออธิบายโครงสร้าง ไม่ใช่สถานะสด:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "task_id": 2,
      "assignee": {"username": "reviewer01"},
      "stage": "acceptance",
      "state": "completed"
    }
  ]
}
```

ถ้า assignee เป็น null หมายถึงยังไม่มีผู้รับผิดชอบ

## 3. แสดงเป็นตารางใน Terminal

ต้องมี curl, jq และ column คำสั่งนี้แสดงเฉพาะหน้าที่ขอมา ดูตัวอย่าง pagination ด้านล่างสำหรับรายงานครบทุกหน้า

```bash
curl --fail-with-body -sS \
  --user admin2 \
  'http://localhost:8080/api/jobs?org=ptt-demo&page_size=100' \
| jq -r '
    ["JOB", "TASK", "ASSIGNEE", "STAGE", "STATE"],
    (.results[] | [
      .id,
      .task_id,
      (.assignee.username // "unassigned"),
      .stage,
      .state
    ])
  | @tsv' \
| column -t -s $'\t'
```

## 4. ตัวอย่าง filters ที่ใช้บ่อย

งานของ annotator01:

```bash
curl --fail-with-body -sS --user admin2 \
  'http://localhost:8080/api/jobs?org=ptt-demo&assignee=annotator01&page_size=100'
```

งานในขั้น Validation:

```bash
curl --fail-with-body -sS --user admin2 \
  'http://localhost:8080/api/jobs?org=ptt-demo&stage=validation&page_size=100'
```

รายละเอียด Job เดียว:

```bash
curl --fail-with-body -sS --user admin2 \
  'http://localhost:8080/api/jobs/2?org=ptt-demo'
```

Issues ที่ยังเปิดของ Job:

```bash
curl --fail-with-body -sS --user admin2 \
  'http://localhost:8080/api/issues?org=ptt-demo&job_id=2&resolved=false&page_size=100'
```

Issues ทั้งหมดของ Job:

```bash
curl --fail-with-body -sS --user admin2 \
  'http://localhost:8080/api/issues?org=ptt-demo&job_id=2&page_size=100'
```

Comments ของ Issue:

```bash
curl --fail-with-body -sS --user admin2 \
  'http://localhost:8080/api/comments?org=ptt-demo&issue_id=1&page_size=100'
```

ผลลัพธ์ถูกกรองด้วยสิทธิ์ของบัญชี/Token ด้วย Worker อาจเห็นเพียงงานของตนเอง หากต้องการรายงานภาพรวมให้ใช้ identity ที่มีสิทธิ์เหมาะสม ไม่เพิ่มสิทธิ์ admin ให้ทุกคน

## 5. Personal Access Token สำหรับสคริปต์

สร้าง PAT ใน UI ของ CVAT ส่วนการตั้งค่าผู้ใช้/Access Tokens เลือก Read-only และกำหนดวันหมดอายุ Token ยังคงถูกจำกัดด้วยสิทธิ์ของเจ้าของบัญชี

```bash
read -rsp 'CVAT access token: ' CVAT_ACCESS_TOKEN
printf '\n'

curl --fail-with-body -sS \
  -H "Authorization: Bearer $CVAT_ACCESS_TOKEN" \
  'http://localhost:8080/api/jobs?org=ptt-demo&page_size=100'

unset CVAT_ACCESS_TOKEN
```

PAT ใช้ Bearer ส่วน legacy token ใช้ authentication scheme ต่างกัน อย่าสลับรูปแบบโดยเดา ไม่บันทึกค่าจริงลง Git หรือ log

## 6. Pagination ที่ต้องทำ

Jobs, Issues และ Comments ส่ง list แบบแบ่งหน้า ต้องวนจน next เป็น null ไม่ถือว่า page_size=100 จะได้ทั้งหมดเสมอ

เพื่อหลีกเลี่ยงส่ง token ไป URL ปลายทางที่ไม่คาดคิด ตัวอย่าง Python ใช้ next เป็นสัญญาณว่ามีหน้าต่อไป แล้วเรียก page หมายเลขถัดไปบน base URL ที่กำหนดเอง

ติดตั้ง requests ใน Python environment ของโครงการก่อน ตัวอย่างนี้พิมพ์ CSV ออก stdout โดยไม่แก้ข้อมูลใน CVAT:

```python
import csv
import getpass
import os
import sys

import requests

base_url = os.environ.get("CVAT_BASE_URL", "http://localhost:8080").rstrip("/")
organization = os.environ.get("CVAT_ORG", "ptt-demo")
token = os.environ.get("CVAT_ACCESS_TOKEN") or getpass.getpass("CVAT PAT: ")

session = requests.Session()
session.headers["Authorization"] = f"Bearer {token}"


def list_all(endpoint, **filters):
    page = 1
    while True:
        response = session.get(
            f"{base_url}/api/{endpoint}",
            params={
                "org": organization,
                "page": page,
                "page_size": 100,
                **filters,
            },
            timeout=30,
            allow_redirects=False,
        )
        if response.status_code != 200:
            # ไม่พิมพ์ token หรือ response body ที่อาจมีข้อมูลภายใน
            raise RuntimeError(f"{endpoint}: HTTP {response.status_code}")
        payload = response.json()
        yield from payload["results"]
        if not payload.get("next"):
            return
        page += 1


writer = csv.writer(sys.stdout)
writer.writerow([
    "job_id", "task_id", "assignee", "stage", "state",
    "open_issues", "resolved_issues",
])

for job in list_all("jobs", sort="id"):
    issues = list(list_all("issues", job_id=job["id"], sort="id"))
    resolved = sum(bool(issue["resolved"]) for issue in issues)
    writer.writerow([
        job["id"],
        job["task_id"],
        (job.get("assignee") or {}).get("username", ""),
        job["stage"],
        job["state"],
        len(issues) - resolved,
        resolved,
    ])
```

บันทึกตัวอย่างเป็น export_job_status.py แล้วรัน:

```bash
python export_job_status.py > job-status.csv
```

ตัวอย่างนี้เป็นจุดเริ่มต้น มีหนึ่งชุด request สำหรับ Issues ต่อ Job จึงอาจช้าเมื่อมีงานจำนวนมาก รายงาน production ควร batch/cache ในขอบเขตสิทธิ์ที่เหมาะสม และเพิ่ม retry, captured_at, schema_version, instance ID และการตรวจความครบถ้วน

ข้อมูลอาจเปลี่ยนระหว่างอ่านหลายหน้า ผลลัพธ์จึงเป็นรายงานช่วงเวลาหนึ่ง ไม่ใช่ transaction snapshot ทั้งระบบ หากต้องการ release approval ต้องใช้ snapshot/revision strategy เพิ่ม

## 7. Mapping สู่ Dashboard

| Dashboard column | แหล่ง |
|---|---|
| Job | job.id |
| Task | job.task_id |
| ผู้รับผิดชอบ | job.assignee.username |
| ขั้นตอน | job.stage |
| สถานะ | job.state |
| Issues ค้าง | นับ resolved=false |
| Issues ปิดแล้ว | นับ resolved=true |
| เวลาอ่านล่าสุด | captured_at ที่ service สร้าง |

รายชื่อคนที่ไม่มีงานจะไม่ปรากฏจาก Jobs อย่างเดียว ต้องอ่านสมาชิก/ผู้ใช้ตามสิทธิ์แล้วทำ left join กับรายการ Jobs ไม่สรุปว่าคนหายจากตารางคือถูกลบบัญชี

## 8. การอัปเดตข้อมูล

เริ่มจากปุ่ม Refresh หรือ polling เช่นทุก 30–60 วินาทีตามจำนวนผู้ใช้และโหลดจริง แสดงเวลาอ่านล่าสุดและสถานะ sync error

เมื่อขยายระบบให้ใช้ Webhook กระตุ้นการอ่าน resource ล่าสุด ร่วมกับ periodic reconciliation อย่าให้ webhook payload เป็นข้อมูลล่าสุดโดยอัตโนมัติ เพราะ event อาจซ้ำหรือมาช้า

## 9. การแปลข้อผิดพลาด

| HTTP / อาการ | สิ่งที่ควรตรวจ |
|---|---|
| 401 | Token หมดอายุ/ไม่ถูกต้อง หรือ authentication ไม่ผ่าน |
| 403 | สิทธิ์บัญชี, Organization และ Job assignment |
| 404 | Resource ID และ route/version |
| 429 | ลดความถี่และ retry ตาม server guidance |
| 502 | Reverse proxy ติดต่อ backend ไม่สำเร็จ |
| Timeout | Network, server load และ timeout policy |
| count มากกว่า results | ต้องอ่าน pagination ต่อ |
| results ว่าง | Filter/สิทธิ์/Organization อาจไม่ตรง ไม่ใช่หลักฐานว่าระบบไม่มีงาน |

คำสั่งทั้งหมดในเอกสารนี้เป็น GET/read-only ไม่มีการมอบหมาย Job หรือเปลี่ยน Stage/State

## 10. เอกสารประกอบ

- [Developer Workflow Guideline](05_CVAT-DEVELOPER-GUIDELINE-WORKFLOW-TH.md)
- [Platform Integration Guideline](04_CVAT-PLATFORM-INTEGRATION-GUIDELINE-TH.md)
- [ตัวอย่างรายงานและความหมาย field](../examples/reports/README.md)
- [CVAT API และ SDK](https://docs.cvat.ai/docs/api_sdk/)
- [Personal Access Tokens](https://docs.cvat.ai/docs/api_sdk/access_tokens/)
