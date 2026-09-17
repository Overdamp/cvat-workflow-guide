const $ = id => document.getElementById(id);
let job = null;
let busy = false;
function notice(message) { $('notice').textContent = message; }
function jobId() { const id=Number($('jobId').value); if(!Number.isSafeInteger(id)||id<1) throw Error('Job ID ไม่ถูกต้อง'); return id; }
async function api(url, method='GET', body) {
  const csrf=document.cookie.split('; ').find(x=>x.startsWith('csrftoken='))?.slice(10);
  const response=await fetch(url,{method,credentials:'same-origin',headers:{'Content-Type':'application/json',...(csrf?{'X-CSRFToken':decodeURIComponent(csrf)}:{})},...(body?{body:JSON.stringify(body)}:{})});
  if(!response.ok) throw Error(`${response.status}: ${response.status===401?'กรุณา login ใน CVAT':response.status===403?'บัญชีนี้ไม่มีสิทธิ์ หรือ session หมดอายุ':(await response.text()).slice(0,250)}`);
  return response.status===204?null:response.json();
}
async function list(url) {
  const results=[];
  while(url) { const target=new URL(url,location.origin); if(![location.origin,'http://localhost:8080'].includes(target.origin)) throw Error('Unexpected pagination origin'); const page=await api(target.pathname+target.search); results.push(...page.results); url=page.next; }
  return results;
}
async function refresh() {
  job=null;
  $('jobInfo').textContent='กำลังอ่านข้อมูล…'; $('issueInfo').textContent='';
  try {
    const me=await api('/api/users/self'); $('connection').textContent=`CVAT: ${me.username}`;
    const id=jobId();
    const current=await api(`/api/jobs/${id}`);
    const issues=await list(`/api/issues?job_id=${id}&page_size=100`);
    job=current;
    $('jobInfo').textContent=`Job #${job.id} · Task #${job.task_id} · ${job.stage} / ${job.state} · ผู้รับผิดชอบ: ${job.assignee?.username||'ยังไม่มอบหมาย'}`;
    $('issueInfo').textContent=`Issues เปิด ${issues.filter(x=>!x.resolved).length} / ทั้งหมด ${issues.length} · อ่านล่าสุด ${new Date().toLocaleTimeString()}`;
    notice('อัปเดตข้อมูลจาก CVAT แล้ว');
  } catch(error) { $('jobInfo').textContent='ไม่สามารถอ่านสถานะปัจจุบัน'; notice(error.message); }
}
async function loadJob() { await refresh(); if(job) $('cvatFrame').src=`/tasks/${job.task_id}/jobs/${job.id}`; }
$('refresh').onclick=refresh;
$('load').onclick=loadJob;
$('login').onclick=()=>{ $('cvatFrame').src='/auth/login'; notice('Login ใน CVAT ด้านล่าง แล้วกดเปิด Job; หากเปลี่ยนบัญชี ให้ logout จากเมนู CVAT ก่อน'); };
$('openCvat').onclick=()=>window.open(job?`/tasks/${job.task_id}/jobs/${job.id}`:'/auth/login','_blank','noopener');
$('fullscreen').onclick=()=> $('cvatFrame').requestFullscreen().catch(error=>notice(error.message));
for(const button of document.querySelectorAll('[data-stage]')) button.onclick=async()=>{
  if(busy) return;
  busy=true;
  document.querySelectorAll('[data-stage]').forEach(x=>x.disabled=true);
  try {
    if(!job||job.id!==jobId()) throw Error('กดเปิด Job และตรวจสถานะก่อน');
    const id=job.id, stage=button.dataset.stage;
    if(!confirm(`ยืนยันว่า Save annotation แล้ว และต้องการเปลี่ยน Job #${id} เป็น ${stage} จริง?`)) return;
    const current=await api(`/api/jobs/${id}`);
    if(current.updated_date!==job.updated_date) throw Error('Job มีการเปลี่ยนแปลง กรุณาอัปเดตสถานะก่อน');
    const body={stage,state:stage==='acceptance'?'completed':'in progress'};
    if(stage==='acceptance') {
      const issues=await list(`/api/issues?job_id=${id}&page_size=100`);
      if(issues.some(x=>!x.resolved)) throw Error('ยังมี Issue เปิดอยู่ ให้ reviewer ตรวจและ Resolve ใน CVAT ก่อน');
    } else {
      const name=$('assignee').value.trim();
      const users=await list(`/api/users?search=${encodeURIComponent(name)}&page_size=100`);
      const target=users.find(x=>x.username===name);
      if(!target) throw Error('ไม่พบผู้รับงาน หรือบัญชีนี้ไม่มีสิทธิ์ดูรายชื่อ');
      body.assignee=target.id;
    }
    await api(`/api/jobs/${id}`,'PATCH',body);
    await refresh(); notice(`CVAT บันทึก ${stage} แล้ว; หากต้องทำงานต่อให้กดเปิด Job หลังแน่ใจว่า Save แล้ว`);
  } catch(error) {notice(error.message);} finally {busy=false;document.querySelectorAll('[data-stage]').forEach(x=>x.disabled=false);}
};
$('cvatFrame').src='/auth/login';
loadJob();
