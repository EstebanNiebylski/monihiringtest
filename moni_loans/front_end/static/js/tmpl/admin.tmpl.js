let selectedLoanId = -1;

// Events

// Fetching functions
async function getAllLoans() {
    const authtoken = localStorage.getItem('authtoken');
    let data = await fetch('http://127.0.0.1:8000/api/loan/', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + authtoken
        },
        method: 'GET'
    }).then(function (response) {
        return response.json();
    });
    return data;
};

async function deleteLoan(loanId) {
    console.log("id", loanId);
    const authtoken = localStorage.getItem('authtoken');
    fetch('http://127.0.0.1:8000/api/loan/' + loanId + '/', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + authtoken
        },
        method: 'DELETE'
    }).then(function (response) {
        if (response.ok) {
            alert("Pedido de prestamo eliminado correctamente.");
            // Refresh page
            location.reload();
        } else {
            alert("Error al intentar eliminar pedido de prestamo.")
        };        
    });    
}

async function updateLoan(loanId) {
    selectedLoanId = loanId;
    let updateModal = document.getElementById('updateModal');
    $(updateModal).modal('show');
}

// Table loader
document.addEventListener("DOMContentLoaded", async function (event) {
    const tbody = document.getElementById("tbody");
    let loans = await getAllLoans();

    loans.forEach(loan => {
        var tr = document.createElement('tr');
        tr.setAttribute("id", loan.id);
        var id = document.createElement('td');
        var dni = document.createElement('td');
        var name = document.createElement('td');
        var lastname = document.createElement('td');
        var gender = document.createElement('td');
        var amount = document.createElement('td');
        var state = document.createElement('td');

        id.innerText = loan.id;
        dni.innerText = loan.requester.dni;
        name.innerText = loan.requester.name;
        lastname.innerText = loan.requester.lastname;
        gender.innerText = loan.requester.gender;
        amount.innerText = loan.amount;
        state.innerText = loan.state;

        tr.appendChild(id);
        tr.appendChild(dni);
        tr.appendChild(name);
        tr.appendChild(lastname);
        tr.appendChild(gender);
        tr.appendChild(amount);
        tr.appendChild(state);
        var div = document.createElement("div");
        div.className = "acciones-div";
        div.appendChild(createUpdateButton(loan.id));
        div.appendChild(createDeleteButton(loan.id));
        tr.appendChild(div)

        tbody.appendChild(tr)
    });

    // Update btn
    document.getElementById("btn-update").addEventListener("click", () => {
        selectedLoanId;
        let state = $("#new-loan-state").val();
        let amount = $("#new-amount").val();
        const dataToSend = {
            "state": state,
            "amount": amount
        }        

        const authtoken = localStorage.getItem('authtoken');
        fetch('http://127.0.0.1:8000/api/loan/' + selectedLoanId + '/', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + authtoken
            },            
            method: 'PUT',
            body: JSON.stringify(dataToSend)
        }).then( async function(response) {                        
            if (response.ok) {
                alert("Pedido de prestamo modificado correctamente.");
                location.reload();
            } else {
                // Params error
                let errorData = await response.json();  
                if (errorData.amount){
                    alert("amount error: " + errorData.amount);
                }                
                if (errorData.state) {
                    alert("state error: " + errorData.state + ". Choices available: OK, NO");
                }                
            }
        }).catch(function (error){
            console.log("error", error);
        });
        $(updateModal).modal('hide');
    });
});

// Functions

// delete button 
function createDeleteButton(itemId) {
    let deleteButton = document.createElement("button");
    deleteButton.innerHTML = "Delete";
    deleteButton.type = "button";
    deleteButton.name = "delete-button";
    deleteButton.className = "btn btn-outline-danger btn-sm";
    deleteButton.addEventListener("click", () => { deleteLoan(itemId) });
    return deleteButton;
}

// edit button
function createUpdateButton(itemId) {
    let updateButton = document.createElement("button");
    updateButton.innerHTML = "Edit";
    updateButton.type = "button";
    updateButton.name = "update-button";
    updateButton.className = "btn btn-outline-primary btn-sm";
    updateButton.addEventListener("click", () => { updateLoan(itemId) });
    return updateButton;
}


