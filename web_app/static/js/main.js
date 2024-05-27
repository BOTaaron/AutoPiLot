document.addEventListener('DOMContentLoaded', () => {
    let socket = io();

    // Listen for console output
    socket.on('console_output', function(msg) {
        let consoleOutput = document.getElementById('console-output');
        if (consoleOutput) {
            let timestamp = new Date().toLocaleTimeString();
            consoleOutput.innerHTML += `<div><span class="timestamp">${timestamp}</span> ${msg}</div>`;
            consoleOutput.scrollTop = consoleOutput.scrollHeight;
        }
    });

    // Form submission to send command
    const commandForm = document.getElementById('command-form');
    if (commandForm) {
        commandForm.onsubmit = function(e) {
            e.preventDefault();
            let input = document.getElementById('command-input');
            if (input) {
                socket.emit('console_input', input.value);  // Send command to server
                input.value = '';  // Clear input after sending
            }
        };
    }

    // Clear console button
    const clearConsoleButton = document.getElementById('clear-console');
    if (clearConsoleButton) {
        clearConsoleButton.onclick = function() {
            let consoleOutput = document.getElementById('console-output');
            if (consoleOutput) {
                consoleOutput.innerHTML = '';
            }
        };
    }


    // Initialize small map, setting attribute values from http://aaron.local:8000/services/leeds_map
 const vectorTileLayerStyles = {
        water: {
            weight: 1,
            color: '#8080ff',
            fillColor: 'blue',
            fillOpacity: 0.3
        },
        landcover: {
            weight: 1,
            color: 'green',
            fillColor: 'green',
            fillOpacity: 0.3
        },
        landuse: {
            weight: 1,
            color: '#043927',
            fillColor: '#043927',
            fillOpacity: 0.3
        },
        building: {
            weight: 1,
            color: 'gray',
            fillColor: 'gray',
            fillOpacity: 0.7
        },
        transportation: {
            weight: 1,
            color: 'black',
            opacity: 0.5
        },
        waterway: {
            weight: 1,
            color: '#000080',
            fillColor: 'blue',
            fillOpacity: 0.3
        },
        boundary: {
            weight: 1,
            color: 'magenta'
        },
        place: {
            weight: 1,
            color: 'rgb(253,153,0)',
            fillColor: 'black'
        },
        park: {
            weight: 1,
            color: 'green',
            fillColor: 'green',
            fillOpacity: 0.3
        },
        poi: {
            weight: 0, // Hide POIs
            color: 'none',
            fillColor: 'none'
        },
        mountain_peak: {
            weight: 0, // Hide mountain peaks
            color: 'none',
            fillColor: 'none'
        },
        aerodrome_label: {
            weight: 0, // Hide aerodrome labels
            color: 'none',
            fillColor: 'none'
        },
        place: {
            weight: 1,
            color: 'black',
            fillColor: 'black'
        },
        transportation_name: {
            weight: 1,
            color: '#f24'
        },
         housenumber: {
                weight: 1,
                color: '#f24'
         },
        aeroway: {
            weight: 1,
            color: '#f24'
        }

    };

    // Initialize small map
    const smallMap = document.getElementById('small-map') // check map is on page before loading
    if (smallMap) {
        let smallMap = L.map('small-map').setView([53.809, -1.5235], 13); // create map with initial coordinates with Leaflet

        // load the map from the map file hosted by mbtileserver
        L.vectorGrid.protobuf('http://aaron.local:8000/services/leeds_map/tiles/{z}/{x}/{y}.pbf', {
            vectorTileLayerStyles,
            maxZoom: 13,
            attribution: '© OpenStreetMap contributors'
        }).addTo(smallMap);

        // dummy coordinates to represent the plane's location, to be replaced by GPS when connection is available
        let planeMarker = L.marker([53.827, -1.593]).addTo(smallMap);
        planeMarker.bindPopup("AutoPiLot 1").openPopup();

    }

    // Initialize full map
    const fullMap = document.getElementById('full-map'); // check map is on page before loading
    if (fullMap) {
        let fullMap = L.map('full-map').setView([53.827, -1.593], 13); // create map with initial coordinates with leaflet

        // load the map from the map file hosted by mbtileserver
        L.vectorGrid.protobuf('http://aaron.local:8000/services/leeds_map/tiles/{z}/{x}/{y}.pbf', {
            vectorTileLayerStyles,
            maxZoom: 13,
            attribution: '© OpenStreetMap contributors'
        }).addTo(fullMap);

        // dummy coordinates to represent the plane's location, to be replaced by GPS when connection is available
        let planeMarker = L.marker([53.827, -1.5938]).addTo(fullMap);
        planeMarker.bindPopup("AutoPiLot 1").openPopup();
    }
});

function sendCommand(command) {
    fetch(`/motor/${command}`, { method: 'POST' })
    .then(response => response.json())
    .then(data => console.log(data.status))
    .catch(error => console.error('Error:', error));
}