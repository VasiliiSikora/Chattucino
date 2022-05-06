// Password Checker:
email = document.getElementById('signup_email')
errorMessage = document.getElementById('error')
signupButton = document.getElementById('signup_disabler')
signupButton.disabled=true
console.log(signupButton)
// Utilised: https://stackoverflow.com/questions/68156642/can-i-use-an-event-listener-to-validate-an-email-address-after-its-entered-with
email.addEventListener("input", (e) => {
    const emailInputValue = e.currentTarget.value;
    if(emailInputValue=='') {
        errorMessage.innerText = ''
        signupButton.disabled=true
    }
    else if( /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(emailInputValue) != true) {
        errorMessage.innerText = 'Email address is an invalid format'
        signupButton.disabled=true
         
    } else {
        errorMessage.innerText = ''
        signupButton.disabled=false
    }
   })

