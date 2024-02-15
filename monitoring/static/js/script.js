// script.js

document.addEventListener('DOMContentLoaded', function () {
    function updateTime() {
        var currentTimeElement = document.getElementById('current-time');
        var now = new Date();
        var hours = now.getHours();
        var minutes = now.getMinutes();
        var seconds = now.getSeconds();
        var formattedTime = `${hours}:${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        currentTimeElement.textContent = formattedTime;
    }
    updateTime()
    setInterval(updateTime, 1000);

    // Правка времени тк джанго не хочет отдавать фильтрованное
    let spans_time =  document.querySelectorAll(".stuff-table_time");
    for (let i = 0; i < spans_time.length; i++){
        let tmp_str = spans_time[i].innerHTML.split(".");
        spans_time[i].innerHTML = tmp_str[0];
    }
});