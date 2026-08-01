const canvas = document.getElementById('heartCanvas');
const ctx = canvas.getContext('2d');
const W = canvas.width; const H = canvas.height;

function heartX(t, scale){ return 16*Math.pow(Math.sin(t),3)*scale; }
function heartY(t, scale){ return (13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t))*scale; }

let points = [];
for(let scale=10; scale<=16; scale++){
  for(let i=0;i<120;i++){
    const t = i*(Math.PI*2)/120;
    points.push([heartX(t, scale), heartY(t, scale)]);
  }
}

function clear(){ ctx.fillStyle='black'; ctx.fillRect(0,0,W,H); }

let drawIndex=0;
function drawHeartStep(){
  ctx.strokeStyle = '#ffbcd1';
  ctx.lineWidth = 3;
  ctx.beginPath();
  let centerX = W/2; let centerY = H/2 + 30;
  for(let i=0;i<=drawIndex && i<points.length;i++){
    let [x,y]=points[i];
    if(i==0) ctx.moveTo(centerX + x, centerY - y);
    else ctx.lineTo(centerX + x, centerY - y);
  }
  ctx.stroke();
  drawIndex += 3;
  if(drawIndex < points.length) requestAnimationFrame(drawHeartStep);
  else requestAnimationFrame(() => showImageAndText());
}

let uploadedImage=null; let uploadedMessage='';

function showImageAndText(){
  // draw final heart
  clear();
  ctx.strokeStyle = '#ffbcd1'; ctx.lineWidth = 3;
  ctx.beginPath();
  let centerX=W/2, centerY=H/2+30;
  for(let i=0;i<points.length;i++){ let [x,y]=points[i]; if(i==0) ctx.moveTo(centerX+x, centerY-y); else ctx.lineTo(centerX+x, centerY-y); }
  ctx.stroke();

  if(uploadedImage){
    // compute image size to fit inside heart (about 260x260)
    let iw = uploadedImage.width, ih = uploadedImage.height;
    let max = Math.min(260, Math.max(iw, ih));
    let scale = 260/Math.max(iw, ih);
    let dw = iw*scale, dh = ih*scale;
    let ix = centerX - dw/2, iy = centerY - dh/2 - 20; // slightly up center
    ctx.drawImage(uploadedImage, ix, iy, dw, dh);
    // text below image
    ctx.fillStyle='white'; ctx.font='20px Arial'; ctx.textAlign='center';
    ctx.fillText(uploadedMessage, centerX, iy + dh + 30);
  }
}

// form handling
const form = document.getElementById('uploadForm');
form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const msg = document.getElementById('message').value || 'I LOVE YOU JAANU💋';
  const imgInput = document.getElementById('image');
  const fd = new FormData();
  fd.append('message', msg);
  if(imgInput.files[0]) fd.append('image', imgInput.files[0]);
  const res = await fetch('/upload',{method:'POST', body:fd});
  const json = await res.json();
  uploadedMessage = json.message;
  if(json.image){
    const imageUrl = json.image;
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = ()=>{ uploadedImage = img; showImageAndText(); };
    img.src = imageUrl;
  } else{
    uploadedImage = null; showImageAndText();
  }
});

// start
clear();
requestAnimationFrame(drawHeartStep);
