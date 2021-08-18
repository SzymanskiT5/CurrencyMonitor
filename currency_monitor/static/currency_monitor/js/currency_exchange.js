function sendRequest() {
    let currency1_amount = document.getElementById("id_currency1_amount").value;
    let currency1_code = document.getElementById("id_currency1_code").value;
    let currency2_code = document.getElementById("id_currency2_code").value;
    if (currency1_amount !== "") {


        let obj = new Object()
        obj.currency1_amount = currency1_amount;
        obj.currency1_code = currency1_code;
        obj.currency2_code = currency2_code;

        let csrftoken = readCookie('csrftoken');
        let string = JSON.stringify(obj);


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







