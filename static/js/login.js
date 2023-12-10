document.addEventListener("DOMContentLoaded", function(){
    let btn = document.querySelector('input[type=submit]');
    btn.addEventListener('click', async function(event){
        event.preventDefault();
        // let username = document.querySelector('input[name=username]').value;
        // let password = document.querySelector('input[name=password]').value;
        
        let response = await fetch("/login", {
                method: 'POST',

                // headers: {
                // // "Content-Type": "application/json",
                // 'Content-Type': 'application/x-www-form-urlencoded',
                // },
                // body: `{"username": "${username}", "password": "${password}"}`
                body: new FormData(document.querySelector("form"))
            }
        );
        let response_json = await response.json();
        // console.log(response_json)
        if (!response_json.success) {
            inputs = document.querySelectorAll("input")
            for (let i = 0; i < inputs.length; i++) {
                inputs[i].style.border = "2px solid red";
            }
            
        }
        else {
            location.replace("/admin/");
        }
    })
})