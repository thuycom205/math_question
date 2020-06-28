function createCookie(name, value, days) {
    var expires;

    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = encodeURIComponent(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ')
            c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0)
            return decodeURIComponent(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}

window.endExam = function () {
eraseCookie('remainingtime');
 if (window.x) clearInterval(window.x)
    window.location = window.location.origin;
}
function  countdown() {
    if (window.x) clearInterval(window.x);

    var d1 = new Date ();
    var d2 = new Date ( d1 );
    d2.setMinutes ( d1.getMinutes() + 60 );

     var hx = readCookie('remainingtime');

    if (hx && hx != NaN && hx != 'NaN') {
       d2.setMinutes ( d1.getMinutes() + parseInt(hx) );
    }

    var deadline = d2.getTime();
    window.x = setInterval(function() {
    var now = new Date().getTime();
    var t = deadline - now;
    var hours = Math.floor((t%(1000 * 60 * 60 * 24))/(1000 * 60 * 60));
    var minutes = Math.floor((t % (1000 * 60 * 60)) / (1000 * 60));

    createCookie('remainingtime',minutes,'1')
    var seconds = Math.floor((t % (1000 * 60)) / 1000);
    if (document.getElementById("hour") != undefined) document.getElementById("hour").innerHTML =hours;
    if (document.getElementById("minute") != undefined) document.getElementById("minute").innerHTML = minutes;
    if (document.getElementById("second") != undefined) document.getElementById("second").innerHTML =seconds;

    if (t < 0) {
         clearInterval(window.x);
         if (document.getElementById("demo") != undefined)    document.getElementById("demo").innerHTML = "TIME UP";
         if (document.getElementById("hour") != undefined)    document.getElementById("hour").innerHTML ='0';
          if (document.getElementById("minute") != undefined)   document.getElementById("minute").innerHTML ='0' ;
          if (document.getElementById("second") != undefined)   document.getElementById("second").innerHTML = '0'; }
    }, 1000);

}
countdown();