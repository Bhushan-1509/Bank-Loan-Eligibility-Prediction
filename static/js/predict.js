document.getElementById("applicant-income").addEventListener("change",()=>{
    document.getElementById("applicant-income-label").innerText = "₹" +document.getElementById("applicant-income").value;    
})



document.getElementById("coapplicant-income").addEventListener("change",()=>{
    document.getElementById("coapplicant-income-label").innerHTML = "₹" + document.getElementById("coapplicant-income").value;
})


document.getElementById("loan-amount").addEventListener("change",()=>{
    document.getElementById("loan-amount-label").innerHTML = "₹" + document.getElementById("loan-amount").value;
})
