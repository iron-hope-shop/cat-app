import os

with open('quarry.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace head tags
old_head = """<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<title>Quarry — a hunting game built for feline eyes</title>"""

new_head = """<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Quarry">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#10161c">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<title>Quarry — a hunting game built for feline eyes</title>"""

# Replace body/html CSS
old_css = """*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{
  background:var(--field);
  color:var(--bone);
  font-family:var(--body);
  font-size:16px;
  line-height:1.55;
  overscroll-behavior:none;
  -webkit-font-smoothing:antialiased;
}"""

new_css = """*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;-webkit-touch-callout:none}
html,body{
  height:100%;
  -webkit-touch-callout:none;
  -webkit-user-select:none;
  user-select:none;
  touch-action:none;
  -webkit-text-size-adjust:none;
}
body{
  background:var(--field);
  color:var(--bone);
  font-family:var(--body);
  font-size:16px;
  line-height:1.55;
  overscroll-behavior:none;
  -webkit-font-smoothing:antialiased;
}"""

# Add touch hardening and service worker in script
old_script_end = """requestAnimationFrame(()=>{
  sizePreview();
  selectKind("beetle");
  renderRecord();
  requestAnimationFrame(pvLoop);
});
})();"""

new_script_end = """// Cat-proof iOS multi-touch and accidental zoom/magnifier gestures
['gesturestart', 'gesturechange', 'gestureend'].forEach(function(evt){
  document.addEventListener(evt, function(e){ e.preventDefault(); }, { passive: false });
});
document.addEventListener('dblclick', function(e){ e.preventDefault(); }, { passive: false });

// Register offline Service Worker if hosted over HTTP/HTTPS
if ('serviceWorker' in navigator && (location.protocol === 'http:' || location.protocol === 'https:')) {
  navigator.serviceWorker.register('sw.js').catch(function(){});
}

requestAnimationFrame(()=>{
  sizePreview();
  selectKind("beetle");
  renderRecord();
  requestAnimationFrame(pvLoop);
});
})();"""

assert old_head in content, "old_head not found in quarry.html"
assert old_css in content, "old_css not found in quarry.html"
assert old_script_end in content, "old_script_end not found in quarry.html"

updated_content = content.replace(old_head, new_head).replace(old_css, new_css).replace(old_script_end, new_script_end)

with open('quarry.html', 'w', encoding='utf-8') as f:
    f.write(updated_content)

os.makedirs('Quarry/www', exist_ok=True)
with open('Quarry/www/index.html', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Updated quarry.html and Quarry/www/index.html successfully.")
