function showRoutes(results) {
    alert(results); 
    // unpack results
    // jquery to display in div
}

function getRoutes(evt) {
    evt.preventDefault();

    var formInputs = {
        "rider_destination" : $("#rider_destination").val(),
        "rider_desitnation1" : $("#rider_desitnation1").val()
        "date" : $("#date").val(),
        "time" : $("#time").val(),
        "seats": $("seats").val(),
    }

    $.get("/match_ride_rider",
            formInputs,
            showRoutes);
}

$("#rideform").on("submit", getRoutes)