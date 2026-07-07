"use strict";


/* ==========================================
   PAY2LINK V3 APP SCRIPT
========================================== */


/* ==========================================
   MOBILE MENU
========================================== */


const menuBtn = document.querySelector(".menu-btn");

const navMenu = document.querySelector(".nav-menu");


if(menuBtn){

    menuBtn.addEventListener("click",()=>{

        navMenu.classList.toggle("active");


        if(navMenu.classList.contains("active")){

            menuBtn.innerHTML =
            '<i class="fa-solid fa-xmark"></i>';

        }else{

            menuBtn.innerHTML =
            '<i class="fa-solid fa-bars"></i>';

        }


    });

}




/* ==========================================
   NAVBAR SCROLL EFFECT
========================================== */


const navbar = document.querySelector(".navbar");


window.addEventListener("scroll",()=>{


    if(window.scrollY > 50){


        navbar.style.background =
        "rgba(255,255,255,.95)";


        navbar.style.boxShadow =
        "0 15px 40px rgba(0,0,0,.08)";


    }else{


        navbar.style.background =
        "rgba(255,255,255,.75)";


        navbar.style.boxShadow =
        "0 20px 60px rgba(16,24,40,.08)";


    }


});






/* ==========================================
   COUNTER ANIMATION
========================================== */


const counters =
document.querySelectorAll("[data-count]");



counters.forEach(counter=>{


    let target =
    Number(counter.getAttribute("data-count"));


    let current = 0;


    let speed =
    target / 120;



    const update = ()=>{


        current += speed;



        if(current < target){


            counter.innerText =
            Math.floor(current)
            .toLocaleString("id-ID");


            requestAnimationFrame(update);


        }else{


            counter.innerText =
            target.toLocaleString("id-ID");


        }


    };


    update();


});







/* ==========================================
   SCROLL REVEAL
========================================== */


const revealElements =
document.querySelectorAll(
".feature-card,.stat-card,.security-card,.payment-card,.step,.timeline-item"
);



const revealObserver =
new IntersectionObserver((entries)=>{


entries.forEach(entry=>{


    if(entry.isIntersecting){


        entry.target.classList.add("show");


    }


});


},{
threshold:.15
});



revealElements.forEach(el=>{


    el.classList.add("hidden");


    revealObserver.observe(el);


});
/* ==========================================
   PARTICLE STAR EFFECT
========================================== */


const starsContainer =
document.querySelector(".stars");


if(starsContainer){


    for(let i=0;i<80;i++){


        const star =
        document.createElement("span");


        star.className =
        "star";


        star.style.left =
        Math.random()*100+"%";


        star.style.top =
        Math.random()*100+"%";


        star.style.animationDelay =
        Math.random()*5+"s";


        starsContainer.appendChild(star);


    }


}






/* ==========================================
   MOUSE PARALLAX EFFECT
========================================== */


const orbs =
document.querySelectorAll(".orb");



document.addEventListener(
"mousemove",
(e)=>{


    const x =
    e.clientX / window.innerWidth;


    const y =
    e.clientY / window.innerHeight;



    orbs.forEach((orb,index)=>{


        const move =
        (index+1)*20;



        orb.style.transform =
        `
        translate(
        ${x*move}px,
        ${y*move}px
        )
        `;


    });



});







/* ==========================================
   WELCOME TOAST
========================================== */


window.addEventListener(
"load",
()=>{


    setTimeout(()=>{


        createToast(
        "🚀 Selamat datang di Pay2Link"
        );


    },1200);



});







function createToast(message){


    const toast =
    document.createElement("div");


    toast.className =
    "pay-toast";


    toast.innerHTML =
    message;



    document.body.appendChild(toast);



    setTimeout(()=>{


        toast.classList.add("show");


    },100);



    setTimeout(()=>{


        toast.classList.remove("show");



        setTimeout(()=>{

            toast.remove();

        },500);



    },3500);



}







/* ==========================================
   LAZY IMAGE LOAD
========================================== */


const images =
document.querySelectorAll("img");



images.forEach(img=>{


    img.loading =
    "lazy";


});







/* ==========================================
   PAGE READY
========================================== */


document.body.classList.add(
"page-loaded"
);
