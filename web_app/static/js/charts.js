// load Google Charts with guage and corechart to display drone data

google.charts.load('current', {'packages':['gauge', 'corechart']});
google.charts.setOnLoadCallback(drawChart);

function sendCommand(command) {
    fetch(`/motor/${command}`, { method: 'POST' })
    .then(response => response.json())
    .then(data => console.log(data.status))
    .catch(error => console.error('Error:', error));
}

// set up and display the gauge
function drawChart() {
    // table containing the data for the gauge
    let motorData = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Motor', 0],
    ]);
    // options for the gauge for size, range of colours, and ticks between major ticks
    let motorOptions = {
        width: 500, height: 200,
        redFrom: 1800, redTo: 2000,
        yellowFrom:1500, yellowTo: 1800,
        minorTicks: 5
    };
    // creates a new chart inside element ID of 'motor_chart_div'
    let motorChart = new google.visualization.Gauge(document.getElementById('motor_chart_div'));
    // draw the chart with default values
    motorChart.draw(motorData, motorOptions);

    let airspeedData = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Speed', 0], // Initial value set to 0
    ]);
    let airspeedOptions = {
        width: 500, height: 200,
        redFrom: 60, redTo: 70,  // red zone starts at 60 MPH up to 70 MPH
        yellowFrom:45, yellowTo: 60, // yellow zone from 45 MPH to 60 MPH
        minorTicks: 5,
        max: 70  // Maximum value for the air speed dial
    };
    let airspeedChart = new google.visualization.Gauge(document.getElementById('airspeed_chart_div'));
    airspeedChart.draw(airspeedData, airspeedOptions);

    // Update motor output periodically
    setInterval(() => updateGauges(motorData, motorChart, motorOptions, airspeedData, airspeedChart), 1000);

}

function updateGauges(motorData, motorChart, motorOptions, airspeedData, airspeedChart) {
    fetch('/motor/output')
    .then(response => response.json())
    .then(data => {
        motorData.setValue(0, 1, data.motor_output);
        motorChart.draw(motorData, motorOptions);
        airspeedData.setValue(0, 1, data.air_speed); // Assume air_speed is also provided
        airspeedChart.draw(airspeedData, airspeedOptions);
    });
}