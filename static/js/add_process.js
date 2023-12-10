document.addEventListener("DOMContentLoaded", function() {


    document.querySelector('.slider').addEventListener('click', async function(e){

      let checkbox_label = this.parentNode;
  
  
      let checkbox = checkbox_label.querySelector("#add_service_file");
  
      let dataservice_file = document.querySelector('#content_service')

      checkbox.addEventListener('change', function() {
        if (checkbox.checked) {
          dataservice_file.classList.toggle("nonecontent_service")
        } else {
          dataservice_file.classList.remove("nonecontent_service")
        }
      })
    });

  document.querySelector("#back").addEventListener('click', async function(e) {

    e.preventDefault();
    location.replace("/admin/");
  })

  document.querySelector("#create").addEventListener('click', async function(e) {

    e.preventDefault();

    let checkbox = document.querySelector("#add_service_file");
    
    

    let process_name = document.querySelector("#process_name").value;
    let process_group = document.querySelector("#process_group").value;
    let content_service = null;
    if (checkbox.checked) {
      console.log(checkbox.checked)

      content_service = JSON.stringify(document.querySelector("#content_service").value);
      
      console.log(content_service);
      
    }


    let response = await fetch("/process/create", {
      method: 'POST',

      headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `{"process_name": "${process_name}", "process_group": "${process_group}", "content_service": ${content_service}}`,
      // body: new FormData(document.querySelector("form"))
    });

    response_json = await response.json()

    console.log(response_json.success)

    if (!response_json.success) {
      alert(`Произошла ошибка при создании сервиса ${process_name}\n\nMessage: ${response_json.error_msg}`)
    } else {
      location.replace("/admin/");
    }
    

  })

})
  