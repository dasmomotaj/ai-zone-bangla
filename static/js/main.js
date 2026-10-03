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
(function(){
  try{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}
  paintThemeBtn();
  var menu=document.getElementById('navMenu');
  if(menu){menu.addEventListener('click',function(e){if(e.target.closest('a'))menu.classList.remove('open');});}
  var bar=document.getElementById('navbar');
  if(bar){var onScroll=function(){bar.classList.toggle('scrolled',window.scrollY>8);};window.addEventListener('scroll',onScroll,{passive:true});onScroll();}
  var path=window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(function(a){
    var p=a.getAttribute('data-path');
    if(p==='/blog'&&path.indexOf('/blog')===0)a.classList.add('active');
    else if(p===path)a.classList.add('active');
  });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('visible');io.unobserve(en.target);}});
    },{threshold:.12});
    document.querySelectorAll('.card,.hero,.filter-bar,.stats').forEach(function(el){el.classList.add('reveal');io.observe(el);});
  }
})();
