


function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function sendRequest() {
    let points = document.getElementById("id_points").value;
    let url = window.location.href
    var lastPart = url.split("/")
    var currency_code = lastPart[lastPart.length - 2]





        var obj = new Object()
        obj.currency_code = currency_code;
        obj.points = points;
        var csrftoken = readCookie('csrftoken');
        var string = JSON.stringify(obj);



        fetch(`${window.origin}/rest/currency-plot/`, {
            method: "POST",
            credentials: "include",
            body: string,
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json",
                "X-CSRFToken": csrftoken


            })


        })
            .then(response => response.json())
            .then(data =>document.getElementById("plot").src= "data:image/png;base64, " + data.plot )}
