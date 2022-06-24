editName = document.querySelector('.edit-itin-name');

editLocation = document.querySelector('.edit-itin-location');

editStart = document.querySelector('.edit-itin-start');

editEnd = document.querySelector('.edit-itin-end');



    editName.addEventListener('click', () => {

        const newName = prompt('What would you like to call this trip?');
        const formInputs = {
            updated_name: newName,
            itin_id: editName.id,
        };
        updateItinerary(formInputs, "name", newName);

    });


    editLocation.addEventListener('click', () => {

        const newLocation = prompt('What city are you visiting?');
        const formInputs = {
            updated_location: newLocation,
            itin_id: editName.id,
        };
        updateItinerary(formInputs, "location", newLocation);

    });


    editStart.addEventListener('click', () => {

        const newStart = prompt('What is the trip start date?');
        const formInputs = {
            updated_start: newStart,
            itin_id: editName.id,
        };
        updateItinerary(formInputs, "start", newStart);

    });


    editEnd.addEventListener('click', () => {

        const newEnd = prompt('What is the trip end date?');
        const formInputs = {
            updated_end: newEnd,
            itin_id: editName.id,
        };
        updateItinerary(formInputs, "end", newEnd);

    });



function updateItinerary(formInputs, span_id, newValue) {

        fetch('/edit-itinerary-fields',  {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers:  {
                'Content-Type': 'application/json',
            },
        }).then((response) => {
            if (response.ok)  {
                document.querySelector(`span#${span_id}`).innerHTML = newValue;
            } else {
                alert('Failed to update trip name.');
            }
        });

}