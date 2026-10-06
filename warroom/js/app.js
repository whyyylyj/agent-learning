/* 佣金宝后端面试作战室 - 应用逻辑 */
(function(){
"use strict";
const MODULES = window.GJ_MODULES = window.GJ_MODULES || [];
const $ = (s, el)=> (el||document).querySelector(s);
const $$ = (s, el)=> Array.from((el||document).querySelectorAll(s));

const STORE_KEY = "gjyjb-v1";
let store = { done:{}, mode:"learn", theme:"light" };
try{ const s = JSON.parse(localStorage.getItem(STORE_KEY)); if(s) store = Object.assign(store, s); }catch(e){}
function save(){ try{ localStorage.setItem(STORE_KEY, JSON.stringify(store)); }catch(e){} }

/* ---------- 轻量行内 markdown ---------- */
function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
function inline(s){
  s = esc(s);
  s = s.replace(/==([^=]+)==/g,'<span class="em">$1</span>');
  s = s.replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>');
  s = s.replace(/`([^`]+)`/g,'<code>$1</code>');
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener" style="color:var(--brand2)">$1</a>');
  return s;
}
function block(b){
  switch(b.t){
    case "p": return `<p>${inline(b.md)}</p>`;
    case "h": return `<div class="h">${inline(b.md)}</div>`;
    case "ul": return `<ul style="padding-left:22px;margin:8px 0">${b.items.map(i=>`<li style="margin:4px 0">${inline(i)}</li>`).join("")}</ul>`;
    case "ol": return `<ol style="padding-left:22px;margin:8px 0">${b.items.map(i=>`<li style="margin:4px 0">${inline(i)}</li>`).join("")}</ol>`;
    case "say": return `<div class="say-block"><span class="say-label">🎙 口述话术</span>${b.items? b.items.map(p=>`<p>${inline(p)}</p>`).join("") : `<p>${inline(b.md)}</p>`}</div>`;
    case "code": return `<pre>${esc(b.text)}</pre>`;
    case "flow": return `<pre class="diagram">${esc(b.text)}</pre>`;
    case "tbl": return `<table class="tbl"><thead><tr>${b.head.map(h=>`<th>${inline(h)}</th>`).join("")}</tr></thead><tbody>${b.rows.map(r=>`<tr>${r.map(c=>`<td>${inline(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
    default: return b.html || "";
  }
}

/* ---------- 进度 ---------- */
function cardDone(id){ return !!store.done[id]; }
function setCardDone(id, v){ if(v) store.done[id]=1; else delete store.done[id]; save(); refreshProgress(); }
function moduleProgress(m){
  if(m.type==="page"){ const n = m.pageItems||[]; if(!n.length) return null;
    const d = n.filter(id=>cardDone(id)).length; return {d, n:n.length}; }
  const n = m.cards.length; const d = m.cards.filter(c=>cardDone(c.id)).length;
  return {d, n};
}
function refreshProgress(){
  let td=0, tn=0;
  MODULES.forEach(m=>{ const p = moduleProgress(m); if(p){ td+=p.d; tn+=p.n; } });
  const pct = tn? Math.round(td*100/tn):0;
  $("#overallBar").style.width = pct+"%";
  $("#overallNum").textContent = pct+"% ("+td+"/"+tn+")";
  $$(".nav-item").forEach(el=>{
    const m = MODULES.find(x=>x.id===el.dataset.id); if(!m) return;
    const p = moduleProgress(m); const prog = el.querySelector(".nav-prog");
    if(p){ prog.textContent = p.d+"/"+p.n; prog.className = "nav-prog"+(p.d===p.n?" done":""); }
    else prog.textContent="";
  });
}

/* ---------- 渲染侧边栏 ---------- */
function renderNav(){
  $("#nav").innerHTML = MODULES.map(m=>`
    <button class="nav-item" data-id="${m.id}">
      <span class="nav-meta"><span><span class="nav-icon">${m.icon||"📘"}</span>${esc(m.name)}</span><span class="nav-prog"></span></span>
    </button>`).join("");
  $$(".nav-item").forEach(el=> el.addEventListener("click", ()=>{ location.hash = "#/"+el.dataset.id; $("#sidebar").classList.remove("show"); }));
}

/* ---------- 渲染模块内容 ---------- */
function openCard(cardEl, scroll){
  cardEl.classList.add("open");
  if(scroll) setTimeout(()=> cardEl.scrollIntoView({behavior:"smooth", block:"start"}), 60);
}
function renderCard(m, c){
  const el = document.createElement("div");
  el.className = "card"; el.id = c.id;
  const badges = [
    c.zhen? `<span class="badge zhen">🔴 国金真题</span>`:"",
    c.scene? `<span class="badge scene">场景题</span>`:"",
    ...(c.tags||[]).map(t=>`<span class="badge tag">${esc(t)}</span>`)
  ].join("");
  const scriptHtml = (c.script||[]).map(block).join("");
  const masked = store.mode==="test";
  el.innerHTML = `
    <div class="card-head">
      <div class="card-check" title="标记为已掌握"><input type="checkbox" ${cardDone(c.id)?"checked":""}><span class="check-ui">✓</span></div>
      <div class="card-q">${inline(c.q)}<div class="badges">${badges}</div></div>
      <div class="card-toggle">▶</div>
    </div>
    <div class="card-body">
      ${c.scene? `<div class="sec sec-scene"><div class="sec-title">🎬 场景与考察点</div><div class="scene-box">${inline(c.scene)}</div></div>`:""}
      ${scriptHtml? `<div class="sec sec-script"><div class="sec-title">⭐ 高分回答（${masked?"自测模式：先自己说，再对照":"建议按话术框架口述，不要背诵"}）</div>
        <div class="answer-mask ${masked?"masked":""}"><div class="script-box">${scriptHtml}</div></div>
        ${masked? `<button class="reveal-btn">👁 显示参考话术</button>`:""}</div>`:""}
      ${c.shine&&c.shine.length? `<div class="sec sec-shine"><div class="sec-title">💡 眼前一亮的点</div><ul class="shine-list">${c.shine.map(s=>`<li>${inline(s)}</li>`).join("")}</ul></div>`:""}
      ${c.fu&&c.fu.length? `<div class="sec sec-fu"><div class="sec-title">🔗 追问链（连续追问怎么接）</div><ul class="fu-list">${c.fu.map(f=>`<li><div class="fu-q">${inline(f.q)}</div><div class="fu-a">${inline(f.a)}</div></li>`).join("")}</ul></div>`:""}
      ${c.deep&&c.deep.length? `<div class="sec sec-deep"><div class="sec-title">⛏️ 深挖阶梯 · 连环追问模拟（逐层往下滚）</div><div class="deep-list">${c.deep.map((d,i)=>`
        <div class="deep-item">
          <div class="deep-q"><span class="deep-lv lv${Math.min(i+1,4)}">${d.lv||("L"+(i+1))}</span><span class="deep-qtext">${inline(d.q)}</span></div>
          ${d.a? `<div class="deep-a">${inline(d.a)}</div>`:""}
          ${d.shine? `<div class="deep-shine">💎 ${inline(d.shine)}</div>`:""}
        </div>`).join("")}</div></div>`:""}
      ${c.pit&&c.pit.length? `<div class="sec sec-pit"><div class="sec-title">⚠️ 避坑</div><ul class="pit-list">${c.pit.map(p=>`<li>${inline(p)}</li>`).join("")}</ul></div>`:""}
      ${c.src? `<div class="src-note">📌 ${inline(c.src)}</div>`:""}
    </div>`;
  $(".card-head", el).addEventListener("click", (e)=>{
    if(e.target.closest(".card-check")) return;
    el.classList.toggle("open");
  });
  $(".card-check input", el).addEventListener("change", (e)=>{ setCardDone(c.id, e.target.checked); e.stopPropagation(); });
  const rb = $(".reveal-btn", el);
  if(rb) rb.addEventListener("click", ()=>{ $(".answer-mask", el).classList.remove("masked"); rb.remove(); });
  return el;
}

function renderModulePage(m){
  const wrap = document.createElement("div");
  wrap.innerHTML = m.page();
  return wrap.firstElementChild;
}

function renderModule(id){
  const m = MODULES.find(x=>x.id===id);
  const host = $("#content");
  host.innerHTML = "";
  if(!m){ host.innerHTML = `<div class="search-empty">模块不存在</div>`; return; }
  $$(".nav-item").forEach(el=> el.classList.toggle("active", el.dataset.id===id));
  document.title = m.name + " · 佣金宝后端面试作战室";
  if(m.type==="page"){ host.appendChild(renderModulePage(m)); refreshProgress(); return; }
  const head = document.createElement("div");
  head.className = "module-head";
  const zhenCount = m.cards.filter(c=>c.zhen).length;
  head.innerHTML = `<div class="module-title"><span>${m.icon||"📘"}</span>${esc(m.name)}</div>
    ${m.desc? `<div class="module-desc">${inline(m.desc)}</div>`:""}
    <div class="module-stats">共 <b>${m.cards.length}</b> 题 ${zhenCount? `· <span class="stat-zhen">含 ${zhenCount} 道国金已核验真题</span>`:""}</div>`;
  host.appendChild(head);
  m.cards.forEach(c=> host.appendChild(renderCard(m, c)));
  refreshProgress();
  // hash 定位打开指定卡片
  const parts = location.hash.split("/");
  if(parts.length>2){ const cardEl = document.getElementById(parts[2]); if(cardEl) openCard(cardEl, true); }
}

/* ---------- 搜索 ---------- */
function norm(s){ return (s||"").toLowerCase(); }
function renderSearch(kw){
  const host = $("#content");
  host.innerHTML = "";
  $$(".nav-item").forEach(el=> el.classList.remove("active"));
  document.title = "搜索：" + kw + " · 佣金宝后端面试作战室";
  const k = norm(kw);
  let hits = 0;
  MODULES.forEach(m=>{
    if(m.type==="page") return;
    const cs = m.cards.filter(c=> norm(c.q).includes(k) || norm(c.scene).includes(k) || norm((c.tags||[]).join(" ")).includes(k) || norm((c.shine||[]).join(" ")).includes(k) || norm((c.fu||[]).map(f=>f.q+f.a).join(" ")).includes(k) || norm((c.deep||[]).map(d=>d.q+(d.a||"")+(d.shine||"")).join(" ")).includes(k) || norm((c.script||[]).map(b=>b.md||b.text||(b.items||[]).join(" ")).join(" ")).includes(k));
    if(!cs.length) return;
    hits += cs.length;
    const head = document.createElement("div");
    head.className="module-head";
    head.innerHTML = `<div class="module-title"><span>${m.icon||"📘"}</span>${esc(m.name)}</div>`;
    host.appendChild(head);
    cs.forEach(c=>{
      const el = renderCard(m, c);
      el.classList.add("open");
      host.appendChild(el);
    });
  });
  if(!hits) host.innerHTML = `<div class="search-empty">没有找到与「${esc(kw)}」相关的内容，换个关键词试试（如：幂等 / B+树 / 幻觉 / 行情）</div>`;
  const backBtn = document.createElement("button");
  backBtn.className="reveal-btn"; backBtn.textContent="← 返回当前模块"; backBtn.style.maxWidth="220px";
  backBtn.addEventListener("click", ()=>{ $("#search").value=""; const last = location.hash.replace("#/","")||MODULES[0].id; renderModule(last.split("/")[0]); });
  host.appendChild(backBtn);
}

/* ---------- 页面类模块构造 ---------- */
function progressCards(){
  const grid = MODULES.map(m=>{
    const p = moduleProgress(m); if(!p) return "";
    const pct = Math.round(p.d*100/p.n);
    return `<div class="prog-card"><div class="pc-name"><span>${m.icon||"📘"} ${esc(m.name)}</span><span class="pc-num">${pct}%</span></div><div class="bar"><div class="bar-fill" style="width:${pct}%"></div></div></div>`;
  }).join("");
  return `<div class="progress-grid">${grid}</div>`;
}
window.GJ_progressCards = progressCards;
window.GJ_pageItem = function(key){ return "pg:"+key; };
window.GJ_checkbox = function(key, label){
  return `<label class="check-item"><input type="checkbox" data-pgkey="${esc(key)}" ${cardDone("pg:"+key)?"checked":""}><span>${inline(label)}</span></label>`;
};
document.addEventListener("change", (e)=>{
  const k = e.target.dataset && e.target.dataset.pgkey;
  if(k) setCardDone("pg:"+k, e.target.checked);
});

/* ---------- 主题 / 模式 / 事件 ---------- */
function applyTheme(){ document.documentElement.dataset.theme = store.theme; $("#themeBtn").textContent = store.theme==="dark" ? "☀️ 日间" : "🌙 夜间"; }
$("#themeBtn").addEventListener("click", ()=>{ store.theme = store.theme==="dark"?"light":"dark"; save(); applyTheme(); });
$("#resetBtn").addEventListener("click", ()=>{
  if(confirm("确定清空全部学习进度吗？")){ store.done = {}; save(); refreshProgress(); route(); }
});
function setMode(mode){
  store.mode = mode; save();
  $("#modeLearn").classList.toggle("active", mode==="learn");
  $("#modeTest").classList.toggle("active", mode==="test");
  route();
}
$("#modeLearn").addEventListener("click", ()=>setMode("learn"));
$("#modeTest").addEventListener("click", ()=>setMode("test"));
$("#sidebarToggle").addEventListener("click", ()=> $("#sidebar").classList.toggle("show"));

let searchTimer=null;
$("#search").addEventListener("input", (e)=>{
  clearTimeout(searchTimer);
  const v = e.target.value.trim();
  searchTimer = setTimeout(()=>{
    if(v) renderSearch(v); else route();
  }, 200);
});

function route(){
  const h = location.hash.replace(/^#\//,"");
  if(!h){ renderModule(MODULES[0].id); return; }
  const id = h.split("/")[0];
  if(MODULES.find(m=>m.id===id)) renderModule(id);
  else renderModule(MODULES[0].id);
}
window.addEventListener("hashchange", route);

/* ---------- 启动 ---------- */
applyTheme();
setMode(store.mode||"learn");
renderNav();
route();
})();
