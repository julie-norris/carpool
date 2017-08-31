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

    $.get("/match_ride_rider",
            formInputs,
            showRoutes);
}

$("#rideform").on("submit", getRoutes);