/*
Copyright (c) Timothy Ings <tim@tim-ings.com>
All Rights Reserved
*/

function OnJsonButtonClick() {
    hreq = new XMLHttpRequest();
    hreq.onreadystatechange = function() {
        if (hreq.readyState === XMLHttpRequest.DONE) {
            if (hreq.status === 200) {
                alert("Response: " + hreq.responseText);
            } else {
                alert("Error: " + hreq.status);
            }
        }
    }
    hreq.open("POST", "/ajax/echo")
    hreq.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    payload = {
        value: document.getElementById('jsonVal').value,
    }
    hreq.send(JSON.stringify(payload))
}
