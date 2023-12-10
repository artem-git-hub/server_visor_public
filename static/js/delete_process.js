document.addEventListener("DOMContentLoaded", function() {


  document.querySelector("#back").addEventListener('click', async function(e) {

    e.preventDefault();
    location.replace("/admin/");
  })


  document.querySelector("#delete").addEventListener('click', async function(e) {

    e.preventDefault();

    let processes = document.querySelectorAll("#process");
    var jsonArr = [];

    for (let i = 0; i < processes.length; i++) {
        const el = processes[i];

        const process_name = el.querySelector("#process_name").innerHTML;
        // console.log(process_name.innerHTML)

        const del_from_db = el.querySelector("#db").checked;
        const del_from_systemd = el.querySelector("#systemd").checked;

        jsonArr.push({
            name: process_name,

            db: del_from_db,
            systemd: del_from_systemd,
        })
        
    }
    
    
    const jsonData = JSON.stringify(jsonArr);

    let response = await fetch("/process/delete", {
      method: 'POST',

      headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: jsonData,
      // body: new FormData(document.querySelector("form"))
    });


    response_json = await response.json()

    console.log(response_json)

    // if (!response_json.success) {
    //     alert(`Произошла ошибка при создании сервиса ${process_name}\n\nMessage: ${response_json.error_msg}`)
    // } else {
    //     location.reload();
    // }
    

  })

})