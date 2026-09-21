# ตารางตัดสินใจเลือก Annotation Tool

เอกสารนี้ใช้เป็นเอกสารประกอบการประชุมเพื่อเปรียบเทียบเครื่องมือทำ annotation และอธิบายเหตุผลที่โครงการ PTT AI Platform เลือก CVAT ในระยะ PoC/เริ่มต้น การให้คะแนนเป็นการประเมินเบื้องต้นตามบริบทของโครงการ ไม่ใช่ผล benchmark และควรตรวจสอบราคาและความสามารถของ edition ที่จะใช้งานจริงอีกครั้งก่อนจัดซื้อ

## ข้อสรุปสำหรับโครงการปัจจุบัน

แนะนำ **CVAT Community แบบ self-hosted** เป็น annotation engine ของแพลตฟอร์มในระยะนี้ เพราะทีมติดตั้งและทดสอบ workflow จริงแล้ว ตั้งแต่ Project → Task → Job → annotation → review/issue → complete และมี Docker, REST API, Python SDK, webhook, งานหลายผู้ใช้ และการนำเข้า/ส่งออก dataset ที่สอดคล้องกับแผน MinIO + backend database ของเรา ตัว core ของ CVAT Community เป็น MIT License และมี API/SDK สำหรับ integration ([CVAT repository](https://github.com/cvat-ai/cvat), [CVAT Developer Documentation](https://docs.cvat.ai/docs/api_sdk/))

การเลือกนี้ไม่ได้หมายความว่า CVAT เหมาะกับทุกงาน หากโจทย์เปลี่ยนเป็นบริการ SaaS ที่ต้องการลดภาระดูแลระบบ, งาน NLP/multimodal เป็นหลัก, หรือแพลตฟอร์มที่ต้องการ active learning และ model lifecycle แบบสำเร็จรูป อาจต้องประเมินเครื่องมืออื่นใหม่

## ขอบเขตการคัดเลือกแบบ Open Source

การประชุมครั้งนี้ให้ความสำคัญกับซอร์สโค้ดที่ตรวจสอบได้, self-host ได้, ควบคุมข้อมูลใน network ขององค์กร และเชื่อมกับ backend ของเราได้ จึงแบ่งเครื่องมือเป็น 3 กลุ่ม:

1. **ตัวเลือกหลักแบบ open source/self-host**: CVAT, Label Studio, doccano, LabelMe และ FiftyOne
2. **ตัวเลือกที่มี open-source component แต่ต้องตรวจ edition/license ของ platform**: Supervisely
3. **เครื่องมือ managed/commercial ที่ใช้เป็น benchmark ได้ แต่ไม่ใช่ตัวเลือกหลักตามเกณฑ์นี้**: V7 Darwin, Labelbox และ Roboflow

คำว่า open source ไม่ได้แปลว่าฟีเจอร์ทุกอย่างของทุก edition ใช้ได้ฟรีหรือมี license เดียวกันทั้งหมด ต้องตรวจ repository, license, รุ่นที่ติดตั้ง และเงื่อนไขของ dependency ก่อนนำไปผลิตจริง

## เครื่องมือที่นำมาเปรียบเทียบ

| เครื่องมือ | ลักษณะเด่น | เหมาะกับงานแบบใด |
| --- | --- | --- |
| **CVAT Community** | Open source, self-hosted, เน้น computer vision และ workflow แบบ Project/Task/Job | ทีมที่ต้องควบคุมข้อมูลและโครงสร้างพื้นฐานเอง ต้องการ API/SDK และงานตรวจคุณภาพ |
| **Label Studio** | Labeling interface ที่ปรับแต่งได้มาก รองรับหลายชนิดข้อมูลและ integration ผ่าน API/webhook | งาน image, text, audio หรือ multimodal ที่ต้องออกแบบ labeling UI เอง |
| **Roboflow Annotate** | Managed computer-vision platform เชื่อม dataset versioning และการ train/model workflow | ทีมที่ต้องการเริ่มเร็วและใช้บริการจัดการ dataset/model แบบครบวงจร |
| **Supervisely** | Visual data platform สำหรับ annotation, apps, automation และการจัดการข้อมูลทีม | องค์กรที่ต้องการ platform สำเร็จรูปและยอมรับการพึ่งพา ecosystem/แผนบริการ |
| **V7 Darwin** | Managed visual-data platform ที่เน้น annotation, automation และ dataset/model workflow | องค์กรที่ต้องการบริการพร้อมใช้และ automation ระดับ production |
| **Labelbox** | Managed data-labeling และ AI lifecycle platform พร้อม API/SDK และ workflow สำหรับทีม | ทีมที่ต้องการ SaaS, collaboration และบริการจัดการข้อมูลแบบองค์กร |
| **LabelMe** | Desktop/Python GUI สำหรับวาด polygon, rectangle, circle, line และ point | นักวิจัยหรือผู้ใช้รายเดียวที่ต้องการ annotate แบบ local อย่างรวดเร็ว |
| **doccano** | Web tool แบบ open source สำหรับ text classification, sequence labeling และ text-to-text | งาน NLP และการทำ label ข้อความ ไม่ใช่ตัวเลือกหลักสำหรับภาพอุตสาหกรรม |
| **FiftyOne** | Dataset/model exploration, evaluation และ visualization; เชื่อม annotation backend ได้ | วิเคราะห์ dataset และผลโมเดล ไม่ใช่ตัวเลือกหลักสำหรับ workflow annotation ของเรา |

CVAT มี integration layer เป็น REST API + Swagger, Python SDK และ CLI รวมทั้งระบุว่าควรจับคู่ major/minor version ของ server กับ SDK/CLI ให้ตรงกัน ([CVAT Developer Documentation](https://docs.cvat.ai/docs/api_sdk/)) Label Studio มี API สำหรับ import/export, cloud storage และ ML integration และมี webhook สำหรับแจ้งเหตุการณ์ไปยัง pipeline ([Label Studio API](https://labelstud.io/guide/api), [Label Studio webhooks](https://labelstud.io/guide/webhooks.html))

## ตารางเปรียบเทียบปัจจัยหลัก

คะแนน 1–5: 5 = ตรงกับความต้องการมาก, 1 = ต้องพัฒนาเพิ่มมากหรือมีข้อจำกัดสำคัญ

| ปัจจัยตัดสินใจ | น้ำหนัก | CVAT | Label Studio | Roboflow | Supervisely | FiftyOne | เหตุผลที่มีผลต่อโครงการ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| ควบคุมข้อมูลและติดตั้งในองค์กร | 20% | **5** | 4 | 2 | 4 | 5 | ภาพอุตสาหกรรมและ annotation ไม่ควรต้องออกนอก network โดยไม่จำเป็น |
| REST API / SDK / automation | 20% | **5** | 5 | 4 | 4 | 4 | Backend ต้องสร้างงาน ดึงสถานะ และนำผลกลับ DB โดยไม่พึ่งการกด UI |
| Workflow ทีม: task/job/มอบหมาย/review/issue | 15% | **5** | 4 | 4 | 5 | 2 | ต้องติดตามว่าใครทำอะไร อยู่ขั้นไหน และแก้ comment/issue ได้ |
| MinIO/S3 หรือ external storage | 10% | **4** | 4 | 4 | 4 | 4 | ลดการอัปโหลดภาพซ้ำและให้ object storage เป็นแหล่งไฟล์ต้นฉบับ |
| การฝังเข้ากับ platform และ auth | 10% | **4** | 4 | 4 | 4 | 3 | ต้องเปิดจาก platform เดียวกันและวาง SSO/สิทธิ์โดยไม่ผูกระบบเกินจำเป็น |
| รูปแบบ annotation และ ML/auto-labeling | 10% | **5** | 4 | 5 | 5 | 4 | ต้องใช้ YOLO/COCO และต่อโมเดลตรวจจับภายหลังได้ |
| ต้นทุนและภาระดูแลระบบ | 15% | **4** | 4 | 3 | 2 | 4 | PoC ใช้เครื่องที่มีอยู่ได้ แต่ต้องประเมิน backup, upgrade และ monitoring |

คะแนนเป็นการประเมินเชิงสถาปัตยกรรมสำหรับโครงการนี้ ควรปรับน้ำหนักหากผู้บริหารให้ความสำคัญกับ SaaS, จำนวนผู้ใช้, SLA, หรือความสามารถด้านข้อมูลชนิดอื่นมากกว่าการควบคุมข้อมูล

## ตารางความเข้ากันได้กับ flow ของเรา

คะแนน: 5 = ตรงกับ flow และทำได้โดยตรง, 3 = ทำได้แต่ต้องเขียน adapter/ตั้งค่าเพิ่ม, 1 = ไม่ใช่บทบาทของเครื่องมือ

| เครื่องมือ | Backend DB ของเรา | MinIO/S3 | REST API/SDK | Webhook/event | Keycloak/OIDC | Multi-user review | บทบาทที่แนะนำ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **CVAT Community** | **5** | **4** | **5** | **5** | 3* | **5** | Annotation engine หลัก |
| **Label Studio OSS** | 5 | **4** | **5** | **5** | 3* | 4 | ทางเลือกหลักอันดับสอง โดยเฉพาะงานหลายชนิดข้อมูล |
| **doccano** | 4 | 3 | 4 | 3 | 3* | 4 | Text/NLP annotation service แยกต่างหาก |
| **LabelMe** | 2 | 1 | 1 | 1 | 1 | 1 | Local utility สำหรับผู้ใช้คนเดียว/แปลงไฟล์ |
| **FiftyOne** | 4 | **5** | 4 | 2 | 2 | 2 | Dataset curation, QA และ model evaluation |
| **Supervisely** | 4 | 4 | 4 | 4 | 3* | 5 | พิจารณาเมื่อซื้อ/ใช้ platform edition ที่รองรับองค์กร |

\* Keycloak: คะแนนนี้หมายถึงต้องตรวจวิธี OIDC/SAML ของรุ่นที่ใช้และการแมป role เพิ่มเติม ไม่ควรถือว่า Keycloak JWT จาก platform จะใช้เป็น CVAT API token ได้โดยอัตโนมัติ ใน PoC ให้หน้าเว็บใช้ SSO ตามความสามารถของ deployment และให้ backend ใช้ PAT/service account แยกเก็บใน secret manager

รูปแบบ flow ที่ทุกตัวเลือกต้องรองรับคือ `MinIO → backend สร้าง task → annotator ทำงาน → event/webhook → backend อ่าน annotation ผ่าน API → upsert ลง backend DB → สร้าง dataset release` โดยไม่เขียนตารางภายในของ annotation tool โดยตรง

## ตารางคัดกรองเครื่องมือเพิ่มเติม

ตารางนี้ช่วยป้องกันการนำเครื่องมือคนละประเภทมาเทียบกันโดยตรงกับ CVAT

| เครื่องมือ | ควบคุมระบบเอง | API/automation | Workflow ทีมและ QA | ประเภทข้อมูลเด่น | ข้อจำกัดเมื่อเทียบกับโครงการนี้ |
| --- | ---: | ---: | ---: | --- | --- |
| **V7 Darwin** | 2 | 5 | 5 | Image/video และ visual AI | เป็น managed platform; ต้องตรวจเรื่อง data residency, ราคา และการเชื่อม MinIO ตามแผนบริการ |
| **Labelbox** | 2 | 5 | 5 | Image, video, text และ AI lifecycle | เหมาะกับ SaaS องค์กร แต่มี vendor lock-in และค่าใช้บริการที่ต้องประเมิน |
| **LabelMe** | 5 | 2 | 1 | Image บนเครื่องเดียว | ไม่มี server workflow, assignment, webhook หรือ multi-user review แบบที่ต้องใช้ |
| **doccano** | 4 | 4 | 3 | Text classification, sequence labeling, text-to-text | เหมาะกับ NLP; ไม่ใช่เครื่องมือหลักสำหรับ bounding box/segmentation ภาพอุตสาหกรรม |
| **FiftyOne** | 5 | 4 | 2 | Dataset exploration และ model evaluation | ควรใช้เสริม CVAT เพื่อวิเคราะห์ข้อมูล ไม่ควรใช้แทน annotation engine หลัก |

ข้อมูลประกอบการจัดกลุ่ม: V7 มีเอกสาร API และ Darwin JSON ของตนเอง ([V7 Darwin Documentation](https://docs.v7labs.com/), [Darwin JSON](https://docs.v7labs.com/reference/darwin-json)); Labelbox มี API/SDK และ webhook ([Labelbox platform](https://docs.labelbox.com/docs), [Labelbox annotations](https://docs.labelbox.com/reference/create-and-import-annotations)); LabelMe เป็นแอป GUI ที่เขียนด้วย Python/Qt และรองรับรูปทรงพื้นฐาน ([LabelMe repository](https://github.com/wkentaro/labelme)); doccano มี backend REST API และ client สำหรับงาน text ([doccano developer guide](https://doccano.github.io/doccano/developer_guide/)); FiftyOne ทำหน้าที่ dataset/model analysis และเชื่อม annotation backend มากกว่าจะเป็นระบบจัดงาน annotation หลัก

## เหตุผลที่เลือก CVAT ตอนนี้

1. **ลดความเสี่ยงเริ่มต้น**: CVAT รันอยู่ใน Docker ของเราแล้ว และ workflow จริงผ่านมาแล้ว จึงไม่ต้องย้ายข้อมูลหรือฝึกทีมกับเครื่องมือใหม่ในช่วงทดสอบ
2. **แยกหน้าที่ชัดเจน**: MinIO เก็บภาพต้นฉบับ, CVAT เก็บบริบทการทำ annotation, ส่วน platform database เก็บ mapping, สถานะธุรกิจ, revision และ dataset release
3. **เชื่อม backend ได้หลายระดับ**: ใช้ REST API เมื่อทีมต้องการควบคุม request ชัดเจน, ใช้ Python SDK เมื่อต้องการลด boilerplate, และใช้ webhook เป็นสัญญาณให้ backend ไปอ่านผลผ่าน API
4. **รองรับงานอุตสาหกรรมจริง**: มี Project/Task/Job, การมอบหมาย, review, issue/comment, หลายผู้ใช้ และรูปแบบภาพ/วิดีโอที่ตรงกับ object detection
5. **ไม่บังคับให้ export ทุกครั้ง**: backend สามารถอ่าน annotation จาก API แล้วเขียนลงฐานข้อมูลเดิมได้ ส่วน export ZIP/COCO/YOLO ใช้เฉพาะตอนสร้าง dataset release หรือส่งให้ training pipeline

## แนวทางใช้งานที่เสนอให้ลงมติ

| ระยะ | การตัดสินใจ | วิธีทำ |
| --- | --- | --- |
| PoC ปัจจุบัน | ใช้ CVAT Community, ผู้ใช้ใน organization ใช้สิทธิ์ระดับเดียวกัน | สร้าง Project/Task/Job ผ่าน API หรือ SDK และมอบหมายงานผ่าน CVAT |
| เชื่อมข้อมูล | ให้ MinIO เป็น source ของภาพ และ platform DB เป็น source ของสถานะธุรกิจ | เก็บ `platform_image_id`, `cvat_task_id`, `cvat_job_id`, `annotation_revision` |
| รับผลลัพธ์ | Webhook แจ้ง event แล้ว backend ดึง annotation จริงจาก API | ทำ idempotency ด้วย task/job + revision/hash ก่อน upsert ลง DB |
| ลดข้อมูลซ้ำ | ไม่ export หรือคัดลอกภาพทุกครั้งที่มีการแก้ไข | เก็บ export เฉพาะ release ที่ระบุ version และ retention policy ของ CVAT |
| ความปลอดภัย | Backend ใช้ PAT/service account ที่เก็บใน secret manager | ผู้ใช้หน้าเว็บและ token ของ backend แยกกัน; ห้ามเขียนฐานข้อมูล CVAT โดยตรง |
| ก่อน production | ทดสอบ load, backup/restore, object-storage permission, SSO และ role matrix | ตรวจ edition/license และกำหนด SLA/retention เป็นเอกสารก่อนเปิดผู้ใช้จำนวนมาก |

## คำถามที่ควรถามในที่ประชุม

- ข้อมูลภาพต้องอยู่ภายใน network/ประเทศหรือไม่ และใครมีสิทธิ์อ่าน object ใน MinIO?
- ต้องการ self-hosted 100% หรือยอมใช้ SaaS เพื่อแลกกับการลดภาระดูแลระบบ?
- จำนวนภาพต่อ batch, จำนวนผู้ใช้พร้อมกัน และเวลาที่รับได้ต่อการสร้าง task คือเท่าไร?
- ต้องรองรับ image/video/3D/text หรือในเฟสแรกมีเฉพาะ object detection บนภาพ?
- ต้องการ review แบบกี่ชั้น และ audit trail ต้องเก็บใน platform เองนานเท่าไร?
- ผลลัพธ์จะเข้า training pipeline ในรูปแบบ API/DB หรือสร้าง versioned export เป็นไฟล์?
- ใครเป็นเจ้าของการกำหนด label schema และการเปลี่ยน schema กระทบ dataset รุ่นเก่าอย่างไร?

## เกณฑ์เปลี่ยนเครื่องมือในอนาคต

ควรเปิดการประเมินใหม่เมื่อเกิดอย่างน้อยหนึ่งข้อ: CVAT ต้องใช้ความสามารถ Enterprise ที่ยังไม่ได้จัดหา, ภาระดูแลระบบสูงกว่าคุณค่าที่ได้, มีงาน text/audio/multimodal เป็นสัดส่วนหลัก, ต้องการ managed SaaS พร้อม SLA, หรือ pipeline ต้องการ model training/versioning ที่รวมอยู่ในแพลตฟอร์มเดียว การเปลี่ยนเครื่องมือควรทำเป็น benchmark จาก dataset เดียวกัน โดยวัดเวลาต่อภาพ, ความถูกต้องหลัง review, API latency, ค่าใช้จ่าย และเวลาปฏิบัติการจริง

## แหล่งอ้างอิง

- [CVAT Developer Documentation](https://docs.cvat.ai/docs/api_sdk/)
- [CVAT Webhook recipes](https://docs.cvat.ai/docs/api_sdk/sdk/examples/webhooks/)
- [Label Studio API](https://labelstud.io/guide/api)
- [Label Studio webhooks](https://labelstud.io/guide/webhooks.html)
- [Label Studio external storage](https://labelstud.io/guide/storage.html)
- [Roboflow Documentation](https://docs.roboflow.com/)
- [Supervisely Documentation](https://docs.supervisely.com/)
- [V7 Darwin Documentation](https://docs.v7labs.com/)
- [Labelbox Documentation](https://docs.labelbox.com/docs)
- [LabelMe repository](https://github.com/wkentaro/labelme)
- [doccano Developer Guide](https://doccano.github.io/doccano/developer_guide/)
