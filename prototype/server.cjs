const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const port = Number(process.env.PORT || 5175);
const upstream = new URL('http://localhost:8080');
const files = {'/platform/':'index.html','/platform/app.js':'app.js','/platform/styles.css':'styles.css','/platform/embed.css':'embed.css'};
const mime = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8'};
const server = http.createServer((req,res)=>{
  const origin = `http://localhost:${port}`;
  if (![`localhost:${port}`,`127.0.0.1:${port}`].includes(req.headers.host)) {res.writeHead(403);res.end('Invalid host');return;}
  if (req.headers.origin && ![origin,`http://127.0.0.1:${port}`].includes(req.headers.origin)) {res.writeHead(403);res.end('Invalid origin');return;}
  const pathname = new URL(req.url,origin).pathname;
  if (pathname==='/platform') {res.writeHead(302,{location:'/platform/'});res.end();return;}
  if(files[pathname]) {
    res.writeHead(200,{'content-type':mime[path.extname(files[pathname])],'cache-control':'no-store','x-frame-options':'SAMEORIGIN'});
    fs.createReadStream(path.join(__dirname,files[pathname])).pipe(res);return;
  }
  const headers={...req.headers,host:upstream.host};
  // Translate our trusted local origin for Django CSRF validation. Cookies and CSRF tokens remain required.
  if(headers.origin) headers.origin=upstream.origin;
  if(headers.referer) headers.referer=upstream.origin+new URL(headers.referer).pathname;
  delete headers['forwarded']; delete headers['x-forwarded-host']; delete headers['x-forwarded-proto'];
  const out=http.request({hostname:'127.0.0.1',port:8080,path:req.url,method:req.method,headers},response=>{
    const h={...response.headers,'x-frame-options':'SAMEORIGIN'};
    // Allow only this local origin to frame CVAT; preserve other CSP directives.
    h['content-security-policy']=(String(h['content-security-policy']||'').replace(/frame-ancestors[^;]*(;|$)/gi,'')+"; frame-ancestors 'self'").replace(/^; /,'');
    if(h.location?.startsWith(upstream.origin)) h.location=h.location.slice(upstream.origin.length)||'/';
    res.writeHead(response.statusCode,h);response.pipe(res);
  });
  out.setTimeout(120000,()=>out.destroy(new Error('Upstream timeout')));
  out.on('error',()=>{if(!res.headersSent)res.writeHead(502,{'content-type':'text/plain'});res.end('Cannot reach CVAT at localhost:8080');});
  req.pipe(out);
});
server.listen(port,'127.0.0.1',()=>console.log(`Open http://localhost:${port}/platform/`));
