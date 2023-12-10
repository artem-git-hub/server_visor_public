document.addEventListener("DOMContentLoaded", function() {

  document.querySelectorAll('#process > td > div > button#show-logs-button').forEach(bttn=>bttn.addEventListener('click',function(e){
    /* create an array from the nodelist so that `indexOf` can be used */
    let col=[...document.querySelectorAll('tr')];
    
    /* find the parent table row of the invoking button */
    let row=this.parentNode.parentNode.parentNode;





    // const row = button.closest(".logs_row");
    
    /* find which table row in the array was the event source */
    let index=col.indexOf( row ) + 1;
    
    /* process the next N records/rows */
    let we_row = col[index]


    let process_name = row.querySelector("#process_name").innerHTML

    let with_logs = we_row.classList.contains("show-logs")

    if (!with_logs) {
      refresh_process(row, with_logs = true);
    }
    
    
    we_row.classList.toggle("show-logs");
    
    const logsText = we_row.querySelector("td > div.logs_text");
    logsText.scrollTop = logsText.scrollHeight;


    
  }))
  
  
  document.querySelector('#logout').addEventListener('click', function(e) {

    document.cookie = "session=;";

    location.reload();
  })

  let processes = document.querySelectorAll('#process')
  for (let i = 0; i < processes.length; i++) {
    const element = processes[i];

    let span = element.querySelector("#process_status");

    let span_status = span.innerHTML.replace(/\s/g, '')

    if ( span_status == 'failed') {
      span.style.backgroundColor = "rgb(185, 72, 72)";
    } else {
      if (span_status == 'inactive') {
        span.style.backgroundColor = "gray";
      }
    }

  }

  


  document.querySelectorAll('#process > td > div > button#restart-process').forEach(bttn=>bttn.addEventListener('click',async function(e){
    let row=this.parentNode.parentNode.parentNode;
    restart_process(row=row);
  }))
  
  document.querySelectorAll('#process > td > div > button#stop-process').forEach(bttn=>bttn.addEventListener('click',async function(e){
    let row=this.parentNode.parentNode.parentNode;
    stop_process(row=row);
  }))

  
  document.querySelectorAll('.slider').forEach(slider=>slider.addEventListener('click', async function(e){
    let checkbox_label = this.parentNode;


    let checkbox = checkbox_label.querySelector("#process_updatе");
    let intervalId;

    checkbox.addEventListener('change', function() {
      if (checkbox.checked) {

        function refresh() {
          let row = checkbox.parentNode.parentNode.parentNode;
          refresh_process(row);
        }
        intervalId = setInterval(refresh, 1750);
      } else {
        clearInterval(intervalId);
      }


    })
  }));


  document.querySelectorAll('#refresh-all').forEach(bttn=>bttn.addEventListener('click',async function(e){
    let col=[...document.querySelectorAll('tr#process')];
    for (let i = 0; i < col.length; i++) {
      let row = col[i];
      refresh_process(row=row);
    }
  }))

  document.querySelectorAll('#stop-all').forEach(bttn=>bttn.addEventListener('click',async function(e){
    let col=[...document.querySelectorAll('tr#process')];
    for (let i = 0; i < col.length; i++) {
      let row = col[i];
      stop_process(row=row);
    }
  }))
  
  document.querySelector('#restart-failed').addEventListener('click',async function(e){
    let col=[...document.querySelectorAll('tr#process')];
    for (let i = 0; i < col.length; i++) {
      let row = col[i];
      
      let process_status = row.querySelector('#process_status').innerHTML
      if (process_status == 'failed') {
        restart_process(row=row);
      }
    }
  })
  
  document.querySelector('#add-process').addEventListener('click',async function(e){
    e.preventDefault();
    location.replace("/process/add/");
  })
  
  document.querySelector('#delete-process').addEventListener('click',async function(e){
    e.preventDefault();
    location.replace("/process/delete/");
  })
  


})



async function stop_process(row) {
  let process_name = row.querySelector('#process_name')
  let response = await fetch(
    `/process/stop/${process_name.innerHTML}`, {
    method: 'GET',
  });

  response_json = await response.json();
  if (!response_json.success) {
    alert(`Произошла ошибка при остановке сервиса ${process_name.innerHTML}\nmessage: ${response_json.error_msg}`)
  }
  refresh_process(row)
}

async function restart_process(row) {
  let process_name = row.querySelector('#process_name')
  let response = await fetch(
    `/process/restart/${process_name.innerHTML}`, {
    method: 'GET',
  });

  response_json = await response.json();
  if (!response_json.success) {
    alert(`Произошла ошибка при обновлении сервиса ${process_name.innerHTML}\nmessage: ${response_json.error_msg}`)
  }
  refresh_process(row)
}



async function refresh_process(row, with_logs = null) {
  let col=[...document.querySelectorAll('tr')];
  let index=col.indexOf( row ) + 1;
  let logs_row = col[index];

  let process_status = row.querySelector('#process_status')
  let process_name = row.querySelector('#process_name')
  let process_pid = row.querySelector('#process_pid')
  let process_uptime = row.querySelector('#process_uptime')

  let logs = logs_row.querySelector('.logs_text')

  let with_logs_for_service
  if (with_logs == null) {
    with_logs_for_service = logs_row.classList.contains("show-logs")
  } else {
    with_logs_for_service = with_logs;
  }


  let response = await fetch(
    `/process/refresh/${process_name.innerHTML}`, {
    method: 'POST',
    headers: {
    "Content-Type": "application/json",
    // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `{"with_logs": ${with_logs_for_service}}`
  });

  response_json = await response.json();

  process_status.innerHTML = response_json.is_failed;

  if ( process_status.innerHTML == 'failed') {
    process_status.style.backgroundColor = "rgb(185, 72, 72)";
  } else {
    if (process_status.innerHTML == 'inactive') {
      process_status.style.backgroundColor = "gray";
    } else {
      process_status.style.backgroundColor = "green";
    }
  }

  process_pid.innerHTML = response_json.pid;
  process_uptime.innerHTML = response_json.uptime;
  
  logs.innerHTML = response_json.logs;

  }