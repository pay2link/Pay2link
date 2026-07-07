/* ==========================================
   PAY2LINK
   APP.JS
========================================== */

"use strict";

/* ==========================================
   INITIALIZE
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initNavbar();

    initCounter();

    initScrollTop();

    initScrollReveal();

    initButtons();

    initTyping();

});

/* ==========================================
   NAVBAR
========================================== */

function initNavbar(){

    const navbar=document.querySelector(".navbar");

    if(!navbar) return;

    window.addEventListener("scroll",()=>{

        if(window.scrollY>70){

            navbar.style.background="rgba(255,255,255,.96)";

            navbar.style.boxShadow="0 15px 35px rgba(0,0,0,.08)";

            navbar.style.height="75px";

        }else{

            navbar.style.background="rgba(255,255,255,.82)";

            navbar.style.boxShadow="0 10px 25px rgba(0,0,0,.05)";

            navbar.style.height="80px";

        }

    });

}

/* ==========================================
   HERO BUTTON
========================================== */

function initButtons(){

    document.querySelectorAll(".start-btn,.login-btn,.login2-btn,.register-btn")

    .forEach(button=>{

        button.addEventListener("mouseenter",()=>{

            button.style.transform="translateY(-4px) scale(1.02)";

        });

        button.addEventListener("mouseleave",()=>{

            button.style.transform="translateY(0) scale(1)";

        });

    });

}

/* ==========================================
   COUNTER
========================================== */

function initCounter(){

const counters=document.querySelectorAll(".counter");

const speed=120;

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

const counter=entry.target;

const target=+counter.dataset.target;

let count=0;

const update=()=>{

const increment=Math.ceil(target/speed);

count+=increment;

if(count<target){

counter.innerText=count.toLocaleString();

requestAnimationFrame(update);

}else{

counter.innerText=target.toLocaleString();

}

};

update();

observer.unobserve(counter);

}

});

});

counters.forEach(counter=>observer.observe(counter));

}

/* ==========================================
   SCROLL TO TOP BUTTON
========================================== */

function initScrollTop(){

const topButton=document.createElement("button");

topButton.innerHTML='<i class="fa-solid fa-arrow-up"></i>';

topButton.id="scrollTop";

document.body.appendChild(topButton);

topButton.style.position="fixed";

topButton.style.right="25px";

topButton.style.bottom="25px";

topButton.style.width="52px";

topButton.style.height="52px";

topButton.style.borderRadius="50%";

topButton.style.border="none";

topButton.style.cursor="pointer";

topButton.style.background="#1677ff";

topButton.style.color="#fff";

topButton.style.fontSize="18px";

topButton.style.display="none";

topButton.style.boxShadow="0 15px 35px rgba(22,119,255,.35)";

topButton.style.zIndex="999";

window.addEventListener("scroll",()=>{

if(window.scrollY>400){

topButton.style.display="block";

}else{

topButton.style.display="none";

}

});

topButton.onclick=()=>{

window.scrollTo({

top:0,

behavior:"smooth"

});

};

}
/* ==========================================
   TYPING EFFECT
========================================== */

function initTyping(){

const title=document.querySelector(".hero-left h1");

if(!title) return;

title.style.opacity="0";

title.style.transform="translateY(25px)";

setTimeout(()=>{

title.style.transition=".8s";

title.style.opacity="1";

title.style.transform="translateY(0)";

},300);

}

/* ==========================================
   SCROLL REVEAL
========================================== */

function initScrollReveal(){

const elements=document.querySelectorAll(

".stat-card,.feature-card,.payment-card,.security-card,.faq-item,.timeline-item"

);

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.style.opacity="1";

entry.target.style.transform="translateY(0)";

observer.unobserve(entry.target);

}

});

},{

threshold:.15

});

elements.forEach(item=>{

item.style.opacity="0";

item.style.transform="translateY(35px)";

item.style.transition=".7s ease";

observer.observe(item);

});

}

/* ==========================================
   RIPPLE BUTTON EFFECT
========================================== */

document.addEventListener("click",e=>{

const button=e.target.closest(

".start-btn,.login-btn,.login2-btn,.register-btn"

);

if(!button) return;

const ripple=document.createElement("span");

const rect=button.getBoundingClientRect();

const size=Math.max(rect.width,rect.height);

ripple.style.width=size+"px";

ripple.style.height=size+"px";

ripple.style.position="absolute";

ripple.style.borderRadius="50%";

ripple.style.background="rgba(255,255,255,.4)";

ripple.style.left=(e.clientX-rect.left-size/2)+"px";

ripple.style.top=(e.clientY-rect.top-size/2)+"px";

ripple.style.pointerEvents="none";

ripple.style.transform="scale(0)";

ripple.style.transition=".6s";

button.style.position="relative";

button.style.overflow="hidden";

button.appendChild(ripple);

requestAnimationFrame(()=>{

ripple.style.transform="scale(3)";

ripple.style.opacity="0";

});

setTimeout(()=>{

ripple.remove();

},650);

});

/* ==========================================
   FLOATING ANIMATION
========================================== */

setInterval(()=>{

document.querySelectorAll(

".feature-card,.payment-card,.security-card"

).forEach((card,index)=>{

card.style.transform=

"translateY("+

Math.sin(Date.now()/800+index)*3+

"px)";

});

},60);

/* ==========================================
   NAVBAR ACTIVE LINK
========================================== */

const sections=document.querySelectorAll("section");

const navLinks=document.querySelectorAll("nav a");

window.addEventListener("scroll",()=>{

let current="";

sections.forEach(section=>{

const top=section.offsetTop-120;

if(scrollY>=top){

current=section.getAttribute("id");

}

});

navLinks.forEach(link=>{

link.classList.remove("active");

if(link.getAttribute("href")==="#"+current){

link.classList.add("active");

}

});

});
/* ==========================================
   MOBILE MENU
========================================== */

function initMobileMenu(){

const navbar=document.querySelector(".navbar");

const nav=document.querySelector("nav");

if(!navbar || !nav) return;

const menu=document.createElement("button");

menu.className="mobile-menu";

menu.innerHTML='<i class="fa-solid fa-bars"></i>';

navbar.appendChild(menu);

menu.addEventListener("click",()=>{

nav.classList.toggle("show");

menu.classList.toggle("open");

if(menu.classList.contains("open")){

menu.innerHTML='<i class="fa-solid fa-xmark"></i>';

}else{

menu.innerHTML='<i class="fa-solid fa-bars"></i>';

}

});

document.querySelectorAll("nav a").forEach(link=>{

link.addEventListener("click",()=>{

nav.classList.remove("show");

menu.classList.remove("open");

menu.innerHTML='<i class="fa-solid fa-bars"></i>';

});

});

}

/* ==========================================
   FAQ ACCORDION
========================================== */

function initFAQ(){

const items=document.querySelectorAll(".faq-item");

items.forEach(item=>{

const answer=item.querySelector("p");

if(!answer) return;

answer.style.maxHeight="0";

answer.style.overflow="hidden";

answer.style.transition=".4s ease";

item.addEventListener("click",()=>{

const opened=item.classList.contains("open");

items.forEach(i=>{

i.classList.remove("open");

const p=i.querySelector("p");

if(p) p.style.maxHeight="0";

});

if(!opened){

item.classList.add("open");

answer.style.maxHeight=answer.scrollHeight+"px";

}

});

});

}

/* ==========================================
   TOAST NOTIFICATION
========================================== */

function showToast(message){

const toast=document.createElement("div");

toast.className="toast";

toast.innerHTML=`<i class="fa-solid fa-circle-check"></i> ${message}`;

document.body.appendChild(toast);

Object.assign(toast.style,{

position:"fixed",

top:"25px",

right:"25px",

padding:"15px 22px",

background:"#1677ff",

color:"#fff",

borderRadius:"14px",

fontWeight:"600",

boxShadow:"0 15px 40px rgba(22,119,255,.35)",

zIndex:"9999",

opacity:"0",

transform:"translateX(80px)",

transition:".35s"

});

setTimeout(()=>{

toast.style.opacity="1";

toast.style.transform="translateX(0)";

},50);

setTimeout(()=>{

toast.style.opacity="0";

toast.style.transform="translateX(80px)";

setTimeout(()=>toast.remove(),400);

},3000);

}

/* ==========================================
   LOADING SCREEN
========================================== */

window.addEventListener("load",()=>{

const loader=document.createElement("div");

loader.id="pageLoader";

loader.innerHTML='<div class="loader-circle"></div>';

Object.assign(loader.style,{

position:"fixed",

top:"0",

left:"0",

width:"100%",

height:"100%",

background:"#ffffff",

display:"flex",

alignItems:"center",

justifyContent:"center",

zIndex:"99999",

transition:".5s"

});

document.body.appendChild(loader);

const circle=loader.querySelector(".loader-circle");

Object.assign(circle.style,{

width:"70px",

height:"70px",

border:"6px solid #dbeafe",

borderTop:"6px solid #1677ff",

borderRadius:"50%",

animation:"spinLoader 1s linear infinite"

});

setTimeout(()=>{

loader.style.opacity="0";

setTimeout(()=>loader.remove(),500);

},700);

});

/* ==========================================
   START
========================================== */

document.addEventListener("DOMContentLoaded",()=>{

initMobileMenu();

initFAQ();

showToast("Selamat datang di Pay2Link 🚀");

});

/* ==========================================
   LOADER ANIMATION
========================================== */

const loaderStyle=document.createElement("style");

loaderStyle.innerHTML=`

@keyframes spinLoader{

0%{transform:rotate(0deg);}

100%{transform:rotate(360deg);}

}

`;

document.head.appendChild(loaderStyle);
