//Jonathan Dereje
//Homework 3
//Clock Function

function updateClock() {
    var now = new Date();
    var hours = now.getHours();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12 || 12;
    var minutes = ('0' + now.getMinutes()).slice(-2);
    var seconds = ('0' + now.getSeconds()).slice(-2);

    document.getElementById('hourLabel').textContent = 'Hours';
    document.getElementById('minuteLabel').textContent = 'Minutes';
    document.getElementById('secondLabel').textContent = 'Seconds';
    document.getElementById('ampmLabel').textContent = 'AM/PM';

    document.getElementById('hours').textContent = hours;
    document.getElementById('minutes').textContent = minutes;
    document.getElementById('seconds').textContent = seconds;
    document.getElementById('ampm').textContent = ampm;
}

setInterval(updateClock, 1000);

window.onload = function () {
    updateClock();
};