document.getElementsByName("body")[0].addEventListener("load",()=>{
    setTimeout(document.querySelector(".loader").style="display:block", 3000);      
    document.querySelector(".loader").style = "display:none";
})
console.log('testing')