var lim
var i
var creditIndex
var slide_len
const load = document.querySelector("#loading")


window.onload=menu_update;
document.addEventListener('contextmenu', event => event.preventDefault());

let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    creditIndex = n
    let slides = document.getElementsByClassName("mySlides") 
      // Call python's random_python function 
      eel.Check()(function(number){   
        lim =number +1                  
      }) 


    if (n > lim) {
      slideIndex = 1
    }

    if (n < 1) {
      slideIndex = lim
    }
    slide_len=lim
    
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slides[slideIndex-1].style.display = "block"; 
}

function call_back(){
  slideIndex = 1
}

function new_wall(){
  load.style.display = "block";
  eel.check_internet()
}


function remove_load(){
  load.style.display = "none";
}


//reload fn
eel.expose(new_wall2)
function new_wall2(){
  call_back()
  window.location.reload()
}

function show_credit(){
  //document.querySelector("#fram").style.display = "block";
  const frames = document.querySelectorAll("#fram")[creditIndex-1];
  frames.style.display = "block";
  document.querySelector('#credit').style.display = "none";
  document.querySelector('#closer').style.display = "block";
}

function show_menu(){
  document.querySelector("#menu").style.display = "block";
  document.querySelector("#vis").style.display = "none";
  closeCredit()
}

function hide_menu(){
  document.querySelector("#menu").style.display = "none";
  document.querySelector("#vis").style.display = "block";
  closeCredit()
}


document.querySelector("#click-right").addEventListener("mouseover", () => 
  document.querySelector('#background').style.background = "linear-gradient(to left,rgba(0, 0, 0, 0.82), rgba(0, 0, 0, 0.281), rgba(0, 0, 0, 0.767))");

document.querySelector("#click-left").addEventListener("mouseover", () => 
  document.querySelector('#background').style.background = "linear-gradient(to left,rgba(0, 0, 0, 0.767), rgba(0, 0, 0, 0.281), rgba(0, 0, 0, 0.82))");


document.querySelector("#click-right").addEventListener("mouseout", () => 
  document.querySelector('#background').style.background = "linear-gradient(to left,rgba(0, 0, 0, 0.767), rgba(0, 0, 0, 0.281), rgba(0, 0, 0, 0.767))");

document.querySelector("#click-left").addEventListener("mouseout", () => 
  document.querySelector('#background').style.background = "linear-gradient(to left,rgba(0, 0, 0, 0.767), rgba(0, 0, 0, 0.281), rgba(0, 0, 0, 0.767))");



function closeCredit(){
  document.querySelectorAll("#fram")[creditIndex-1].style.display = "none";
  document.querySelector('#closer').style.display = "none";
  document.querySelector('#credit').style.display = "block";
}



function resolution(quality){
  eel.resolution(quality)
  menu_update();
}

function source(preferred){
  if (preferred==0){
    eel.sources("featured")
  }
  if (preferred==1){
    let input = document.querySelector("#custom");
    let value = input.value;
    eel.sources(value)
  }
  menu_update();
}

function con_filter(quality){
  eel.con_filter(quality);
  menu_update();
}

function start_wall(val){
  eel.con_startup(val);
  eel.get_startup(0,val)
  menu_update();
}


function menu_update(){
  eel.res_get()(function(menures){
    document.querySelector("#resText").textContent = menures;
  })
  eel.query_get()(function(menuquery){
    document.querySelector("#queryText").textContent = menuquery;
  })
  eel.con_fil_get()(function(menucon){
    document.querySelector("#conText").textContent = menucon;
  })
  eel.interval_get()(function(menuinterval){
    document.querySelector("#intervalText").textContent = menuinterval;
  })
  eel.con_startup_get()(function(menuinterval){
    document.querySelector("#startText").textContent = menuinterval;
  })
  eel.interval_Secget()(function(timing){
    autoTime(timing)
  })
}

function set(){
  setas = creditIndex-1;
  eel.set_wallpaper(setas,2)
}

function auto(interval){
  eel.interval(interval);
  menu_update();
  new_wall2()
}

function autoTime(sectime){
  if(sectime != "never"){
// Set the date we're counting down to
    time  =Number(sectime)
    const countDownDate = (new Date().getTime()/1000)+time;

    // Update the count down every 1 second
    var x = setInterval(function() {

      // Get today's date and time
      var now = (new Date().getTime()/1000);
        
      // Find the distance between now and the count down date
      var distance = countDownDate - now;
        
      // If the count down is over, write some text 
      if (distance < 0) {
        new_wall();
        clearInterval(x);
      }
    }, 1000);
  }
}

eel.expose(notify_internet)
function notify_internet(){

  remove_load()

  document.querySelector("#test").innerHTML = "NO INTERNET!"
  setTimeout(function(){
    document.querySelector("#test").innerHTML = "WELCOME"
  }, 2000);

}

function web(n){
  auth_page = creditIndex-1
  eel.web_open(n,auth_page,slide_len)
}


function confirm(n){
  document.querySelector('#confirmation').style.display = "block";
  if(n==0){
    document.querySelector('#info').innerHTML = "THIS ACTION WILL DELETE ALL YOUR PREVIOUS WALLPAPERS!"
    document.querySelector('#yes').style.display = "block"
    document.querySelector('#no').style.display = "block"
    document.querySelector('#full').style.display = "none"
    document.querySelector('#raw').style.display = "none"
  }
  if(n==1){
    document.querySelector('#info').innerHTML = "THIS ACTION WILL GET ALL LOW RESOLUTION WALLPAPERS IN HIGH RESOLUTION (WILL REQUIRE A CONSIDERABLE AMOUNT OF INTERNET)!"
    document.querySelector('#yes').style.display = "none"
    document.querySelector('#no').style.display = "none"
    document.querySelector('#full').style.display = "block"
    document.querySelector('#raw').style.display = "block"
  }
}

function confirm_hide(n){

  document.querySelector('#confirmation').style.display = "none";
    if(n==1){
      eel.revoke_()
      new_wall2()
    }

}

function confirm_res_hide(n){
  load.style.display = "block"
  if(n==0){
    eel.get_high_res(1)//1 == Raw
    set()
    new_wall2()
  }
  if(n==1){
    eel.get_high_res(2)// 2 == Full
    set()
    new_wall2()
  }
}


async function sleep(ms) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function next(n){
  if(n==0){
    for(let i=10;i>-10;i=i-1){
      t = ((i/2)**2 + 1*i)
      NewValue = (((10 - (-10)) * (0.1 - 0.01)) / (10 - (i))) + 0.001
      document.querySelector('.license').style.opacity = NewValue;
      await sleep(t)
      console.log(NewValue)
    }
  }
  var button=document.querySelector('#next2')
  var key=document.querySelector('#key')
  document.querySelector('.license').style.display = "none";
  document.querySelector('#next1').style.display = "none";
  button.style.display = "block";
  key.style.display = "block";
  document.querySelector('#link_api').style.display = "block";
}

function get_api(){
  key.style.borderColor = "#5c5b5b92"
  var text = "";
  text=key.value
  console.log(text)
  if(text==""){
    key.style.borderColor = "red";
  }
  else{
    load.style.display = "block"
    eel.saveEnv(text)
  }
}

eel.expose(invalid_key)
function invalid_key(n){
  key.value="";
  if(n==0){
    remove_load();
    key.style.borderColor = "red";
    key.placeholder ="INVALID KEY! PLEASE TRY AGAIN";
  }

  if(n==1){
    remove_load();
    key.style.borderColor = "red";
    key.placeholder ="NO INTERNET CONNECTION!";
  }
}

eel.expose(status_ok)
function status_ok(n){
  var startwindow=document.querySelector('.startWindow');
  if(n==0){
    remove_load();
    startwindow.style.display="block";
  }
  if(n==1){
    remove_load();
    startwindow.style.display="none";
  }
}


eel.expose(destroyer)
function destroyer(){
  window.close();
}



eel.expose(resetDialog)
function resetDialog(){
  remove_load()
  document.querySelector('#confirmationReset').style.display = "block";

}
