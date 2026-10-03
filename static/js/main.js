function toggleNav(){document.getElementById('navMenu').classList.toggle('open');}
function currentTheme(){return document.documentElement.getAttribute('data-theme')==='dark'?'dark':'light';}
function paintThemeBtn(){var b=document.getElementById('themeBtn');if(b)b.textContent=currentTheme()==='dark'?'☀️':'🌙';}
function toggleTheme(){
  var h=document.documentElement;
  var next=h.getAttribute('data-theme')==='dark'?'light':'dark';
  h.setAttribute('data-theme',next);
  try{localStorage.setItem('theme',next);}catch(e){}
  paintThemeBtn();
}
function scrollToTop(){window.scrollTo({top:0,behavior:'smooth'});}
function bnDigits(n){try{return Number(n).toLocaleString('bn-BD');}catch(e){return String(n);}}
function animateCount(el){
  var target=parseFloat(el.getAttribute('data-count'));if(isNaN(target))return;
  var suffix=el.getAttribute('data-suffix')||'';
  var dur=1300,t0=null;
  function step(ts){
    if(!t0)t0=ts;var p=Math.min((ts-t0)/dur,1);
    var eased=1-Math.pow(1-p,3);
    el.textContent=bnDigits(Math.round(target*eased))+suffix;
    if(p<1)requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
function startTyping(el){
  var phrases=JSON.parse(el.getAttribute('data-phrases')||'[]');
  if(!phrases.length)return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){el.textContent=phrases[0];return;}
  var pi=0,ci=0,deleting=false;
  var caret=document.createElement('span');caret.className='caret';
  function tick(){
    var cur=phrases[pi];
    el.textContent=cur.slice(0,ci);el.appendChild(caret);
    var delay=deleting?32:65;
    if(!deleting&&ci===cur.length){delay=1600;deleting=true;}
    else if(deleting&&ci===0){deleting=false;pi=(pi+1)%phrases.length;delay=350;}
    ci+=deleting?-1:1;
    setTimeout(tick,delay);
  }
  tick();
}
(function(){
  try{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}
  paintThemeBtn();
  var menu=document.getElementById('navMenu');
  if(menu){menu.addEventListener('click',function(e){if(e.target.closest('a'))menu.classList.remove('open');});}
  var bar=document.getElementById('navbar');
  var prog=document.getElementById('scrollbar');
  var toTop=document.getElementById('toTop');
  var onScroll=function(){
    var y=window.scrollY||0;
    if(bar)bar.classList.toggle('scrolled',y>8);
    if(toTop)toTop.classList.toggle('show',y>420);
    if(prog){var h=document.documentElement.scrollHeight-window.innerHeight;
      prog.style.width=(h>0?(y/h*100):0)+'%';}
  };
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  if(toTop)toTop.addEventListener('click',scrollToTop);
  var path=window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(function(a){
    var p=a.getAttribute('data-path');
    if(p==='/blog'&&path.indexOf('/blog')===0)a.classList.add('active');
    else if(p===path)a.classList.add('active');
  });
  var counted=false;
  function watchCounts(){
    document.querySelectorAll('[data-count]').forEach(function(el){
      if(el.getAttribute('data-done'))return;
      var r=el.getBoundingClientRect();
      if(r.top<window.innerHeight&&r.bottom>0){el.setAttribute('data-done','1');animateCount(el);}
    });
  }
  window.addEventListener('scroll',watchCounts,{passive:true});watchCounts();
  document.querySelectorAll('.typing-line').forEach(startTyping);
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('visible');io.unobserve(en.target);}});
    },{threshold:.12});
    document.querySelectorAll('.card,.hero,.filter-bar,.stats,.marquee').forEach(function(el){el.classList.add('reveal');io.observe(el);});
  }
  if(window.matchMedia('(pointer:fine)').matches&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    document.querySelectorAll('.card').forEach(function(card){
      card.classList.add('tilt');
      card.addEventListener('mousemove',function(e){
        var r=card.getBoundingClientRect();
        var x=(e.clientX-r.left)/r.width-.5, y=(e.clientY-r.top)/r.height-.5;
        card.style.transform='translateY(-6px) perspective(700px) rotateX('+(-y*7)+'deg) rotateY('+(x*7)+'deg)';
      });
      card.addEventListener('mouseleave',function(){card.style.transform='';});
    });
  }
})();
