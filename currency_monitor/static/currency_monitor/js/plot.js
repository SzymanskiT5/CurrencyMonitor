
function sendRequest() {
    let points = document.getElementById("id_points").value;
    let url = window.location.href
    let lastPart = url.split("/")
    let currency_code = lastPart[lastPart.length - 2]


    let obj = new Object()
    obj.currency_code = currency_code;
    obj.points = points;
    let csrftoken = readCookie('csrftoken');
    let string = JSON.stringify(obj);


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
        .then(data => document.getElementById("plot").src = "data:image/png;base64, " + data.plot)
}
