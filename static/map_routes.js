function showRoutes(content) {
    $("#showroutes").html(content);
    // jquery to display in div
}

function getRoutes(evt) {
    evt.preventDefault();

    var formInputs = {
        "rider_destination" : $("#rider_destination").val(),
        "rider_destination1" : $("#rider_destination1").val(),
        "date" : $("#date").val(),
        "time" : $("#time").val(),
        "num_seats": $("#seats").val(),
    }

    var form_okay = true;
    for (var key in formInputs) {
        if (!formInputs[key]){ // if any of the inputs are empty
            form_okay = false;
        }
    }

    if (form_okay){
        $.get("/match_ride_rider",
                formInputs,
                showRoutes);
    } else {
        $("#showroutes").html("<p>Please complete all fields</p>");
    }
}

$("#rideform").on("submit", getRoutes);