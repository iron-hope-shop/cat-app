import re
import os

with open('quarry.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Title and metadata
content = content.replace(
    '<title>Quarry — a hunting game built for feline eyes</title>',
    '<title>cat-app — a hunting game built for feline eyes</title>'
)
content = content.replace(
    '<meta name="apple-mobile-web-app-title" content="Quarry">',
    '<meta name="apple-mobile-web-app-title" content="cat-app">'
)
content = content.replace(
    '<h1 class="wordmark">Quarry</h1>',
    '<h1 class="wordmark">cat-app</h1>'
)
content = content.replace(
    'download("quarry-"+stamp()+".csv"',
    'download("cat-app-"+stamp()+".csv"'
)
content = content.replace(
    'download("quarry-"+stamp()+".json"',
    'download("cat-app-"+stamp()+".json"'
)

# 2. CSS adjustments for iPad responsive grid
old_css_block = """/* ---------- home ---------- */
#home{padding:clamp(28px,6vw,64px) clamp(22px,6vw,48px) 72px;max-width:660px;margin:0 auto}
.wordmark{
  font-family:var(--display);
  font-size:clamp(44px,13vw,76px);
  font-weight:600;
  line-height:.92;
  letter-spacing:-.02em;
  color:var(--wheat);
}
.standfirst{
  font-family:var(--display);
  font-size:clamp(18px,4.6vw,23px);
  font-weight:400;
  line-height:1.35;
  color:var(--bone);
  max-width:24ch;
  margin-top:14px;
}
.deck{color:var(--muted);font-size:15px;max-width:52ch;margin-top:16px}

/* hero: live specimen window */
.window{
  margin-top:30px;
  border-radius:14px;
  overflow:hidden;
  background:#0b1015;
  box-shadow:inset 0 0 0 1px var(--line), 0 18px 40px -28px #000;
  position:relative;
}
#preview{display:block;width:100%;height:190px}
.window-note{
  position:absolute;left:14px;bottom:11px;
  font-size:12.5px;color:var(--muted);
  pointer-events:none;
}
.peek{
  position:absolute;right:11px;bottom:9px;
  font-size:12.5px;padding:5px 11px;border-radius:20px;
  background:rgba(10,14,18,.7);color:var(--muted);
  box-shadow:inset 0 0 0 1px var(--line);backdrop-filter:blur(4px);
}
.peek[aria-pressed="true"]{background:var(--wheat);color:#141a10;box-shadow:none}
body.cv #preview, body.cv .chip canvas{filter:url(#catvision)}

/* sections */
.block{margin-top:38px}
.block-h{
  font-family:var(--display);
  font-size:20px;font-weight:600;
  color:var(--bone);margin-bottom:4px;
}
.block-sub{color:var(--muted);font-size:14px;margin-bottom:16px;max-width:50ch}

/* specimen chips */
.specimens{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}
.chip{
  background:var(--slate);
  border-radius:11px;
  padding:11px 6px 10px;
  text-align:center;
  transition:background .14s, box-shadow .14s;
  box-shadow:inset 0 0 0 1px transparent;
}
.chip canvas{display:block;width:100%;height:42px}
.chip span{display:block;font-size:13px;color:var(--muted);margin-top:5px}
.chip[aria-checked="true"]{background:var(--slate-hi);box-shadow:inset 0 0 0 1.5px var(--wheat)}
.chip[aria-checked="true"] span{color:var(--bone)}
.specimen-note{color:var(--muted);font-size:14px;margin-top:13px;min-height:2.6em;max-width:48ch}

/* settings rows */
.row{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:15px 0;border-top:1px solid var(--line)}
.row:last-of-type{border-bottom:1px solid var(--line)}
.row-label{font-size:15px}
.row-label small{display:block;color:var(--muted);font-size:13px;line-height:1.4;margin-top:2px}
.seg{display:flex;background:var(--slate);border-radius:9px;padding:3px;flex:none}
.seg button{padding:7px 13px;border-radius:7px;font-size:14px;color:var(--muted);white-space:nowrap}
.seg button[aria-pressed="true"]{background:var(--slate-hi);color:var(--wheat);font-weight:500}

/* cta */
.cta{
  display:block;width:100%;margin-top:30px;
  background:var(--wheat);color:#141a10;
  font-size:18px;font-weight:600;
  padding:19px;border-radius:12px;
  transition:transform .1s;
}
.cta:active{transform:scale(.985)}

/* prep list */
.prep{margin-top:34px;padding-left:18px;border-left:2px solid var(--line)}
.prep h3{font-family:var(--display);font-size:18px;font-weight:600;margin-bottom:12px}
.prep p{color:var(--muted);font-size:14.5px;margin-bottom:11px;max-width:54ch}
.prep b{color:var(--bone);font-weight:500}

/* science disclosure */
details{margin-top:34px;border-top:1px solid var(--line);padding-top:18px}"""

new_css_block = """/* ---------- home ---------- */
#home{
  padding: max(28px, env(safe-area-inset-top, 28px)) max(22px, env(safe-area-inset-right, 22px)) max(64px, env(safe-area-inset-bottom, 64px)) max(22px, env(safe-area-inset-left, 22px));
  max-width: 1100px;
  margin: 0 auto;
}
.home-layout{
  display: flex;
  flex-direction: column;
  gap: 32px;
}
.home-primary, .home-secondary{
  min-width: 0;
}
.wordmark{
  font-family:var(--display);
  font-size:clamp(44px,11vw,76px);
  font-weight:600;
  line-height:.92;
  letter-spacing:-.02em;
  color:var(--wheat);
}
.standfirst{
  font-family:var(--display);
  font-size:clamp(18px,3.8vw,23px);
  font-weight:400;
  line-height:1.35;
  color:var(--bone);
  max-width:32ch;
  margin-top:14px;
}
.deck{color:var(--muted);font-size:15px;max-width:54ch;margin-top:16px}

/* hero: live specimen window */
.window{
  margin-top:24px;
  border-radius:14px;
  overflow:hidden;
  background:#0b1015;
  box-shadow:inset 0 0 0 1px var(--line), 0 18px 40px -28px #000;
  position:relative;
}
#preview{display:block;width:100%;height:200px}
.window-note{
  position:absolute;left:14px;bottom:11px;
  font-size:12.5px;color:var(--muted);
  pointer-events:none;
}
.peek{
  position:absolute;right:11px;bottom:9px;
  font-size:12.5px;padding:6px 13px;border-radius:20px;
  background:rgba(10,14,18,.7);color:var(--muted);
  box-shadow:inset 0 0 0 1px var(--line);backdrop-filter:blur(4px);
  touch-action: manipulation;
}
.peek[aria-pressed="true"]{background:var(--wheat);color:#141a10;box-shadow:none}
body.cv #preview, body.cv .chip canvas{filter:url(#catvision)}

/* sections */
.block{margin-top:32px}
.block-first{margin-top:0}
.block-h{
  font-family:var(--display);
  font-size:20px;font-weight:600;
  color:var(--bone);margin-bottom:4px;
}
.block-sub{color:var(--muted);font-size:14px;margin-bottom:16px;max-width:52ch}

/* specimen chips */
.specimens{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.chip{
  background:var(--slate);
  border-radius:12px;
  padding:12px 6px 11px;
  text-align:center;
  transition:background .14s, box-shadow .14s, transform .1s;
  box-shadow:inset 0 0 0 1px transparent;
  touch-action: manipulation;
  min-height: 74px;
}
.chip:active{transform:scale(.97)}
.chip canvas{display:block;width:100%;height:44px}
.chip span{display:block;font-size:13px;color:var(--muted);margin-top:5px;font-weight:500}
.chip[aria-checked="true"]{background:var(--slate-hi);box-shadow:inset 0 0 0 1.5px var(--wheat)}
.chip[aria-checked="true"] span{color:var(--bone)}
.specimen-note{color:var(--muted);font-size:14px;margin-top:13px;min-height:2.6em;max-width:52ch}

/* settings rows */
.row{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px 0;border-top:1px solid var(--line)}
.row:last-of-type{border-bottom:1px solid var(--line)}
.row-label{font-size:15px}
.row-label small{display:block;color:var(--muted);font-size:13px;line-height:1.4;margin-top:2px}
.seg{display:flex;background:var(--slate);border-radius:10px;padding:4px;flex:none}
.seg button{padding:8px 16px;border-radius:8px;font-size:14.5px;color:var(--muted);white-space:nowrap;touch-action:manipulation}
.seg button[aria-pressed="true"]{background:var(--slate-hi);color:var(--wheat);font-weight:600}

/* cta */
.cta{
  display:block;width:100%;margin-top:24px;
  background:var(--wheat);color:#141a10;
  font-size:19px;font-weight:600;
  padding:20px;border-radius:14px;
  box-shadow: 0 4px 20px rgba(240,222,107,.18);
  transition:transform .1s, filter .1s;
  touch-action: manipulation;
}
.cta:active{transform:scale(.985);filter:brightness(.95)}

/* prep list */
.prep{margin-top:28px;padding-left:18px;border-left:2px solid var(--line)}
.prep h3{font-family:var(--display);font-size:18px;font-weight:600;margin-bottom:12px}
.prep p{color:var(--muted);font-size:14.5px;margin-bottom:11px;max-width:54ch}
.prep b{color:var(--bone);font-weight:500}

/* science disclosure */
details{margin-top:28px;border-top:1px solid var(--line);padding-top:18px}

/* iPad & tablet side-by-side grid optimization */
@media (min-width: 820px){
  .home-layout{
    display: grid;
    grid-template-columns: minmax(320px, 1fr) minmax(380px, 1.25fr);
    gap: 44px;
    align-items: start;
  }
  .home-primary{
    position: sticky;
    top: 28px;
  }
  #preview{
    height: 230px;
  }
  .specimens{
    gap: 12px;
  }
  .chip{
    min-height: 80px;
    padding: 14px 8px 12px;
  }
  .chip canvas{
    height: 48px;
  }
}"""

assert old_css_block in content, "old_css_block not found"
content = content.replace(old_css_block, new_css_block)

# 3. Update HTML markup of #home to use .home-layout
old_home_markup = """<!-- ============ HOME ============ -->
<main id="home" class="screen on">
  <h1 class="wordmark">cat-app</h1>
  <p class="standfirst">A hunting game drawn for the way cats actually see.</p>
  <p class="deck">Prey that flees instead of charging, in the two colours a cat's eye can tell apart, moving at the stop-start rhythm that triggers a pounce. Set it on a tablet on the floor and let them work.</p>

  <div class="window">
    <canvas id="preview"></canvas>
    <span class="window-note" id="previewNote">Beetle, moving as it will in play</span>
    <button class="peek" id="peek" aria-pressed="false">Cat vision</button>
  </div>

  <section class="block">
    <h2 class="block-h">What they'll be chasing</h2>
    <p class="block-sub">Each one moves on a different rhythm. Cats who ignore one will often chase another.</p>
    <div class="specimens" id="specimens" role="radiogroup" aria-label="Choose quarry"></div>
    <p class="specimen-note" id="specimenNote"></p>
  </section>

  <section class="block">
    <div class="row">
      <span class="row-label">Session length
        <small>Hunting happens in short bursts. Two short sessions beat one long one.</small>
      </span>
      <div class="seg" id="lenSeg">
        <button data-min="5" aria-pressed="false">5 min</button>
        <button data-min="10" aria-pressed="true">10 min</button>
        <button data-min="15" aria-pressed="false">15 min</button>
      </div>
    </div>
    <div class="row">
      <span class="row-label">Shuffle quarry
        <small>Swaps to a different creature every minute or two, on its own. The best answer to a cat who's seen it all before.</small>
      </span>
      <div class="seg" id="shufSeg">
        <button data-s="0" aria-pressed="true">Off</button>
        <button data-s="1" aria-pressed="false">On</button>
      </div>
    </div>
    <div class="row">
      <span class="row-label">Squeaks
        <small>One short chirp, only at the moment of a catch. Silent the rest of the time.</small>
      </span>
      <div class="seg" id="sndSeg">
        <button data-snd="1" aria-pressed="true">On</button>
        <button data-snd="0" aria-pressed="false">Off</button>
      </div>
    </div>
  </section>

  <button class="cta" id="start">Start the hunt</button>

  <section class="prep">
    <h3>Before you start</h3>
    <p><b>Have a treat or a real toy ready.</b> This is the part most screen games and laser pointers get wrong. A cat's hunting sequence ends in a physical catch, and a hunt that never ends leaves them wound up. When the timer runs out, give them something they can actually pin down.</p>
    <p><b>Put a screen protector on.</b> Claws come out. A tempered glass sheet costs a few pounds and saves the tablet.</p>
    <p><b>Lay the tablet flat and hold it still,</b> or wedge it against something. A sliding screen breaks the illusion instantly.</p>
    <p><b>Some cats won't register.</b> Dry paw pads and fur don't always trigger a capacitive screen, and plenty of cats simply aren't interested in screens — I've seen no reliable figure for how many, so don't trust anyone who gives you one. Two minutes of watching tells you which kind you have.</p>
  </section>

  <details id="recWrap" hidden>
    <summary>Your cat's record</summary>
    <div class="rec" id="rec"></div>
  </details>

  <details>
    <summary>Why it looks like this</summary>"""

new_home_markup = """<!-- ============ HOME ============ -->
<main id="home" class="screen on">
  <div class="home-layout">
    <div class="home-primary">
      <h1 class="wordmark">cat-app</h1>
      <p class="standfirst">A hunting game drawn for the way cats actually see.</p>
      <p class="deck">Prey that flees instead of charging, in the two colours a cat's eye can tell apart, moving at the stop-start rhythm that triggers a pounce. Set it on a tablet on the floor and let them work.</p>

      <div class="window">
        <canvas id="preview"></canvas>
        <span class="window-note" id="previewNote">Beetle, moving as it will in play</span>
        <button class="peek" id="peek" aria-pressed="false">Cat vision</button>
      </div>

      <button class="cta" id="start">Start the hunt</button>

      <section class="prep">
        <h3>Before you start</h3>
        <p><b>Have a treat or a real toy ready.</b> This is the part most screen games and laser pointers get wrong. A cat's hunting sequence ends in a physical catch, and a hunt that never ends leaves them wound up. When the timer runs out, give them something they can actually pin down.</p>
        <p><b>Put a screen protector on.</b> Claws come out. A tempered glass sheet costs a few pounds and saves the tablet.</p>
        <p><b>Lay the tablet flat and hold it still,</b> or wedge it against something. A sliding screen breaks the illusion instantly.</p>
        <p><b>Some cats won't register.</b> Dry paw pads and fur don't always trigger a capacitive screen, and plenty of cats simply aren't interested in screens — I've seen no reliable figure for how many, so don't trust anyone who gives you one. Two minutes of watching tells you which kind you have.</p>
      </section>
    </div>

    <div class="home-secondary">
      <section class="block block-first">
        <h2 class="block-h">What they'll be chasing</h2>
        <p class="block-sub">Each one moves on a different rhythm. Cats who ignore one will often chase another.</p>
        <div class="specimens" id="specimens" role="radiogroup" aria-label="Choose quarry"></div>
        <p class="specimen-note" id="specimenNote"></p>
      </section>

      <section class="block">
        <div class="row">
          <span class="row-label">Session length
            <small>Hunting happens in short bursts. Two short sessions beat one long one.</small>
          </span>
          <div class="seg" id="lenSeg">
            <button data-min="5" aria-pressed="false">5 min</button>
            <button data-min="10" aria-pressed="true">10 min</button>
            <button data-min="15" aria-pressed="false">15 min</button>
          </div>
        </div>
        <div class="row">
          <span class="row-label">Shuffle quarry
            <small>Swaps to a different creature every minute or two, on its own. The best answer to a cat who's seen it all before.</small>
          </span>
          <div class="seg" id="shufSeg">
            <button data-s="0" aria-pressed="true">Off</button>
            <button data-s="1" aria-pressed="false">On</button>
          </div>
        </div>
        <div class="row">
          <span class="row-label">Squeaks
            <small>One short chirp, only at the moment of a catch. Silent the rest of the time.</small>
          </span>
          <div class="seg" id="sndSeg">
            <button data-snd="1" aria-pressed="true">On</button>
            <button data-snd="0" aria-pressed="false">Off</button>
          </div>
        </div>
      </section>

      <details id="recWrap" hidden>
        <summary>Your cat's record</summary>
        <div class="rec" id="rec"></div>
      </details>

      <details>
        <summary>Why it looks like this</summary>"""

assert old_home_markup in content, "old_home_markup not found"
content = content.replace(old_home_markup, new_home_markup)

# Close the .home-secondary and .home-layout divs before the footer
old_home_end = """  </details>

  <p class="foot">Everything runs in this page — nothing is recorded or sent anywhere. Screen play is a supplement to real toys, not a replacement for them.</p>
</main>"""

new_home_end = """  </details>
    </div>
  </div>

  <p class="foot">Everything runs in this page — nothing is recorded or sent anywhere. Screen play is a supplement to real toys, not a replacement for them.</p>
</main>"""

assert old_home_end in content, "old_home_end not found"
content = content.replace(old_home_end, new_home_end)

# 4. Chip rendering helper so on orientation change/resize they redraw crisp
old_chip_init = """ORDER.forEach(k=>{
  const b=document.createElement("button");
  b.className="chip"; b.setAttribute("role","radio"); b.dataset.k=k;
  b.innerHTML='<canvas></canvas><span>'+SPECIES[k].label+'</span>';
  chipsEl.appendChild(b);
  const cv=b.querySelector("canvas");
  requestAnimationFrame(()=>{
    const r=cv.getBoundingClientRect(), dpr=Math.min(2,devicePixelRatio||1);
    cv.width=Math.round(r.width*dpr); cv.height=Math.round(r.height*dpr);
    const x=cv.getContext("2d"); x.setTransform(dpr,0,0,dpr,0,0);
    x.translate(r.width/2,r.height/2);
    const sz=Math.min(30,r.height*.72);
    DRAW[k](x,sz,SPECIES[k].color,.35,false);
  });
  b.addEventListener("click",()=>selectKind(k));
});"""

new_chip_init = """function paintSpecimenChips(){
  [...chipsEl.children].forEach(b=>{
    const k=b.dataset.k, cv=b.querySelector("canvas"), r=cv.getBoundingClientRect();
    if(!r.width) return;
    const dpr=Math.min(2,devicePixelRatio||1);
    cv.width=Math.round(r.width*dpr); cv.height=Math.round(r.height*dpr);
    const x=cv.getContext("2d"); x.setTransform(dpr,0,0,dpr,0,0);
    x.translate(r.width/2,r.height/2);
    const sz=Math.min(32,r.height*.72);
    DRAW[k](x,sz,SPECIES[k].color,.35,false);
  });
}

ORDER.forEach(k=>{
  const b=document.createElement("button");
  b.className="chip"; b.setAttribute("role","radio"); b.dataset.k=k;
  b.innerHTML='<canvas></canvas><span>'+SPECIES[k].label+'</span>';
  chipsEl.appendChild(b);
  b.addEventListener("click",()=>selectKind(k));
});
requestAnimationFrame(paintSpecimenChips);"""

assert old_chip_init in content, "old_chip_init not found"
content = content.replace(old_chip_init, new_chip_init)

# Update resize handler to repaint chips
content = content.replace(
    'addEventListener("resize",()=>{ sizePreview(); if(document.getElementById("play").classList.contains("on")) sizeField(); });',
    'addEventListener("resize",()=>{ sizePreview(); paintSpecimenChips(); if(document.getElementById("play").classList.contains("on")) sizeField(); });'
)

with open('quarry.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('Quarry/www/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("quarry.html and Quarry/www/index.html successfully updated for iPad layout and cat-app branding.")
