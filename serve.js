const http=require('http'),fs=require('fs'),path=require('path');
const mime={'.html':'text/html','.css':'text/css','.js':'application/javascript','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.ico':'image/x-icon','.json':'application/json'};
const root='C:/Users/Lenovo/osrs-guide-site';
http.createServer((req,res)=>{
  let f=path.join(root,req.url==='/'?'index.html':req.url);
  fs.readFile(f,(e,d)=>{
    if(e){res.writeHead(404);res.end('404');return}
    res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'text/html','Cache-Control':'no-cache'});
    res.end(d);
  });
}).listen(3001,()=>console.log('Server running on http://localhost:3001'));
