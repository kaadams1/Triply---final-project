// alert("Javascript is connected")

document.querySelector('#add-flight-and-hotel').addEventListener('click', (evt)=> {
    evt.preventDefault();

    const formInputs = {
        flightInfo : document.getElementById("flight-info").value,
        hotelInfo : document.getElementById("hotel-info").value,
    };

    fetch('/add-flight-and-hotel', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            // alert(responseJson.status);
            console.log(responseJson)
            document.querySelector('#display-flight').innerHTML = responseJson.flight
            document.querySelector('#display-hotel').innerHTML = responseJson.hotel
        });
})
