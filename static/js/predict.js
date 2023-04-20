
// event listeners to applicant income section 
document.getElementById("applicant-income").addEventListener("change",()=>{
    document.getElementById("app-income").value = "₹" +document.getElementById("applicant-income").value;    
})

document.getElementById("app-income").addEventListener("change",()=>{
    let appIncome = document.getElementById("app-income").value;
    let addOn = "₹";
    document.getElementById("applicant-income").value = appIncome;
    if(appIncome.includes("₹")){
        addOn = "";
    }
    document.getElementById("app-income").value = addOn + appIncome;
});

// event listeners co-applicant income section 
document.getElementById("coapplicant-income").addEventListener("change",()=>{
    document.getElementById("coapp-income").value = "₹" + document.getElementById("coapplicant-income").value;
    
})
document.getElementById("coapp-income").addEventListener("change",()=>{
    let coAppIncome = document.getElementById("coapp-income").value
    let addOn = "₹"
    document.getElementById("coapplicant-income").value = coAppIncome;
    if(coAppIncome.includes("₹")){
        addOn = "";
    }
    document.getElementById("coapp-income").value = addOn + coAppIncome;
});



// event listeners in loan amount section

document.getElementById("loan-amount").addEventListener("change",()=>{
    document.getElementById("loan-amt").value = "₹" + document.getElementById("loan-amount").value;
})


document.getElementById("loan-amt").addEventListener("change",()=>{
    let loanAmount = document.getElementById("loan-amt").value;
    let addOn = "₹";
    document.getElementById("loan-amount").value = loanAmount;
    if(loanAmount.includes("₹")){
        addOn = "";
    }
    document.getElementById("loan-amt").value = addOn + loanAmount;
});




