function getAsync(query, callback) {
    const request = new XMLHttpRequest();
    request.open('GET', query, true);

    request.onload = () => {
        if (request.status === 200) {
            callback(JSON.parse(request.responseText));
        } else {
            alert ('Request failed');
        }
    }

    request.send();
}

function getSync(query) {
    const request = new XMLHttpRequest();
    request.open('GET', query, false);
    request.send(null);

    if (request.status === 200) {
        return JSON.parse(request.responseText);
    } else {
        alert ('GET request ' + query + ' failed!');
    }
}
