// Load Google Charts with gauge and corechart to display drone data
google.charts.load('current', {'packages':['gauge', 'corechart']});
google.charts.setOnLoadCallback(drawChart);

function sendCommand(command) {
    fetch(`/motor/${command}`, { method: 'POST' })
    .then(response => response.json())
    .then(data => console.log(data.status))
    .catch(error => console.error('Error:', error));
}

// Set up and display the gauges
function drawChart() {
    // Motor data
        const commonGaugeOptions = {
        width: 200, height: 200,
        redFrom: 80, redTo: 100,
        yellowFrom: 60, yellowTo: 80,
        minorTicks: 5,
        majorTicks: ['0', '20', '40', '60', '80', '100'],
        max: 100,
        animation: { duration: 500, easing: 'inAndOut' },
        greenColor: '#00ff00',
        yellowColor: '#ffff00',
        redColor: '#ff0000',
        backgroundColor: { fill: '#2e2e2e' },
        fontName: 'Roboto',
        textStyle: {
            color: '#ffffff'
        },
        titleTextStyle: {
            color: '#ffffff'
        }
    };

    let motorData = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Motor', 0],
    ]);
    let motorOptions = {
        ...commonGaugeOptions,
        redFrom: 80, redTo: 100,
        yellowFrom:50, yellowTo: 80,
        minorTicks: 5
    };
    let motorChart = new google.visualization.Gauge(document.getElementById('motor_chart_div'));
    motorChart.draw(motorData, motorOptions);

    // Airspeed data
    let airSpeedData = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Speed', 0],
    ]);
    let airSpeedOptions = {
        ...commonGaugeOptions,
        redFrom: 60, redTo: 70,
        yellowFrom:45, yellowTo: 60,
        minorTicks: 5,
        max: 70
    };
    let airSpeedChart = new google.visualization.Gauge(document.getElementById('airspeed_chart_div'));
    airSpeedChart.draw(airSpeedData, airSpeedOptions);

    // Temperature data
    let temperatureData = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Temp', 0],
    ]);
    let temperatureOptions = {
        ...commonGaugeOptions,
        redFrom: 80, redTo: 100,
        yellowFrom:60, yellowTo: 80,
        minorTicks: 5,
        max: 100
    };
    let temperatureChart = new google.visualization.Gauge(document.getElementById('temperature_chart_div'));
    temperatureChart.draw(temperatureData, temperatureOptions);

    // Barometric pressure data
    let pressureData = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Pressure', 0],
    ]);
    let pressureOptions = {
        ...commonGaugeOptions,
        width: 500, height: 200,
        redFrom: 1100, redTo: 1200,
        yellowFrom: 900, yellowTo: 1100,
        minorTicks: 5,
        max: 1200
    };
    let pressureChart = new google.visualization.Gauge(document.getElementById('barometric_pressure_div'));
    pressureChart.draw(pressureData, pressureOptions);

    // Altitude data
    let altitudeData = new google.visualization.DataTable();
    altitudeData.addColumn('datetime', 'Time');
    altitudeData.addColumn('number', 'Altitude');
    altitudeData.addRow([new Date(), 0]); // Initial row
let altitudeOptions = {
    height: 200,  // Adjust as necessary
    backgroundColor: '#2e2e2e',
    hAxis: {title: 'Time', textStyle: {color: '#ffffff'}, titleTextStyle: {color: '#ffffff'}},
    vAxis: {title: 'Altitude (m)', textStyle: {color: '#ffffff'}, titleTextStyle: {color: '#ffffff'}},
    legend: { position: 'bottom', textStyle: {color: '#ffffff'} },
    curveType: 'function',
    colors: ['#00ff00'],
    fontName: 'Roboto',
    titleTextStyle: {
        color: '#ffffff'
    }
};
    let altitudeChart = new google.visualization.LineChart(document.getElementById('altitude_chart_div'));
    altitudeChart.draw(altitudeData, altitudeOptions);

    // Update all gauges and charts periodically
    setInterval(() => updateGauges(
        motorData, motorChart, motorOptions,
        airSpeedData, airSpeedChart, airSpeedOptions,
        temperatureData, temperatureChart, temperatureOptions,
        pressureData, pressureChart, pressureOptions,
        altitudeData, altitudeChart, altitudeOptions
    ), 1000);
}

function updateGauges(
    motorData, motorChart, motorOptions,
    airSpeedData, airSpeedChart, airSpeedOptions,
    temperatureData, temperatureChart, temperatureOptions,
    pressureData, pressureChart, pressureOptions,
    altitudeData, altitudeChart, altitudeOptions
) {
    // Update motor output
    fetch('/data/motor_output')
    .then(response => response.json())
    .then(data => {
        motorData.setValue(0, 1, parseFloat(data.motor_output));
        motorChart.draw(motorData, motorOptions);
    })
    .catch(error => console.error('Error fetching motor output'));

    // Update barometric data
    fetch('/data/barometric')
    .then(response => response.json())
    .then(data => {
        let temperature = parseFloat(data.temperature);
        let pressure = parseFloat(data.pressure);
        let altitude = parseFloat(data.altitude);

        // Set temperature data
        temperatureData.setValue(0, 1, temperature);

        // Set pressure data
        pressureData.setValue(0, 1, pressure);

        // Update altitude chart
        const currentTime = new Date();
        altitudeData.addRow([currentTime, altitude]);

        // Redraw charts
        temperatureChart.draw(temperatureData, temperatureOptions);
        pressureChart.draw(pressureData, pressureOptions);
        altitudeChart.draw(altitudeData, altitudeOptions);
    })
    .catch(error => console.error('Error fetching barometric data'));
}
