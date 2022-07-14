// alert("Javascript is connected")

editName = document.querySelector('[name="edit-itin-name"]');

editLocation = document.querySelector('[name="edit-itin-location"]');

editStart = document.querySelector('[name="edit-itin-start"]');

editEnd = document.querySelector('[name="edit-itin-end"]');



    editName.addEventListener('click', () => {

        const newName = prompt('What would you like to call this trip?');
        const formInputs = {
            updated_name: newName,
            itin_id: editName.id,
        };
        updateItinerary(formInputs, "name", newName);
        nameSpan = document.querySelector('#nameEdit');
        nameSpan.innerHTML = newName;
    });


    editLocation.addEventListener('click', () => {

        const newLocation = prompt('What city are you visiting?');
        const formInputs = {
            updated_location: newLocation,
            itin_id: editName.id,
        };
        updateItinerary(formInputs, "location", newLocation);
        locationSpan = document.querySelector('#locationEdit');
        locationSpan.innerHTML = newLocation;
    });


    editStart.addEventListener('click', () => {

        const newStart = prompt('What is the trip start date?');
        const formInputs = {
            updated_start: newStart,
            itin_id: editName.id,
        };
        updateItinerary(formInputs, "start", newStart);
        startSpan = document.querySelector('#startEdit');
        startSpan.innerHTML = newStart;
    });


    editEnd.addEventListener('click', () => {

        const newEnd = prompt('What is the trip end date?');
        const formInputs = {
            updated_end: newEnd,
            itin_id: editName.id,
        };
        updateItinerary(formInputs, "end", newEnd);
        endSpan = document.querySelector('#endEdit');
        endSpan.innerHTML = newEnd;
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