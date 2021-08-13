

function sendRequest() {
    let currency1_amount = document.getElementById("id_currency1_amount").value;
    let currency1_code = document.getElementById("id_currency1_code").value;
    let currency2_code = document.getElementById("id_currency2_code").value;
    if (currency1_amount !== "")
    {


        var obj = new Object()
        obj.currency1_amount = currency1_amount;
        obj.currency1_code = currency1_code;
        obj.currency2_code = currency2_code;

        var csrftoken = readCookie('csrftoken');
        var string = JSON.stringify(obj);


        fetch(`${window.origin}/rest/currency-calculator/`, {
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
            .then(data => document.getElementById("id_currency2_amount").value = data.value)


}
}

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






