

editFlightHotel = document.querySelector('#add-flight-and-hotel');

    editFlightHotel.addEventListener('click', () => {

        const newFlight = document.querySelector('#flight-info').value;
        const newHotel = document.querySelector('#hotel-info').value;

        const formInputs = {
            updated_flight: newFlight,
            itin_id: window.location.href.split("/")[4],
            updated_hotel: newHotel,
        };

        fetch('/add-flight-and-hotel',  {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers:  {
                'Content-Type': 'application/json',
            },
        }).then((response) => {
            if (response.ok)  {
                document.querySelector('#display-flight').innerHTML = newFlight;
                document.querySelector('#display-hotel').innerHTML = newHotel;
            } else {
                alert('Failed to update trip.');
            }
        });

    });