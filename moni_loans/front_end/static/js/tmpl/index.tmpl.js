async function postLoan(loanInfo) {
  let response = await fetch('http://127.0.0.1:8000/api/loan/', {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: loanInfo
  }).then(function(response){
    return response.json();
  });
  return response;
};

window.addEventListener("load", function () {
  // Loan request form
  document.getElementById('loan-form').addEventListener('submit', (e) => {
    e.preventDefault()
    let FormName = document.getElementById('loan-form')

    let params = {};
    for (var i = 0; i < FormName.elements.length - 1; i++) {
      params[FormName.elements[i].name] = FormName.elements[i].value;

    }

    let loanRequestData = JSON.stringify({
      "amount": params.amount,
      "requester_info": {
        "dni": params.dni,
        "name": params.name,
        "lastname": params.lastname,
        "email": params.email,
        "gender": params.gender
      }
    })    
    postLoan(loanRequestData).then(function (response){  
      console.log("response", response);
      if (response.loan.state == 'OK') {
        alert("Su solicitud de prestamo por " + response.loan.amount + " fue aprobada.")
      } else {
        alert("Su solicitud de prestamo por " + response.loan.amount + " fue rechazada.")
      }
    });    

  });

  // Login form
  document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault()
    let FormName = document.getElementById('login-form')

    let params = {};
    for (var i = 0; i < FormName.elements.length; i++) {
      if (FormName.elements[i].name === "user" || FormName.elements[i].name === "password") {
        params[FormName.elements[i].name] = FormName.elements[i].value;
      }
    }
    let paramsToSend = {
      "username": params.user,
      "password": params.password
    }

    await fetch('http://127.0.0.1:8000/auth/login/', {
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(paramsToSend)
    }).then( async function (response){
      let data = await response.json() 
      const authtoken = data.token;     
      localStorage.setItem('authtoken', authtoken);      
      if (response.ok) {             
        window.location.href = "http://127.0.0.1:8000/web/admin";        
      }
    });        
  });  
});