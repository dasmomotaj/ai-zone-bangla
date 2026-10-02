function toggleNav(){document.getElementById('navMenu').classList.toggle('open');}
function toggleTheme(){
  const h=document.documentElement;
  const next=h.getAttribute('data-theme')==='dark'?'light':'dark';
  h.setAttribute('data-theme',next);localStorage.setItem('theme',next);
}
(function(){const t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);})();
