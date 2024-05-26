document.addEventListener('DOMContentLoaded', () => {
    let socket = io();

    // Listen for console output
    socket.on('console_output', function(msg) {
        let textarea = document.getElementById('console');
        if (textarea) {
            textarea.value += msg + '\n';  // Append message to textarea
            textarea.scrollTop = textarea.scrollHeight;
        }
    });

    // Form submission to send command
    const commandForm = document.getElementById('command-form');
    if (commandForm) {
        commandForm.onsubmit = function(e) {
            e.preventDefault();
            var input = document.getElementById('command-input');
            if (input) {
                socket.emit('console_input', input.value);  // Send command to server
                input.value = '';  // Clear input after sending
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
            color: 'black'
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
            color: 'black'
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
        }
    };

    // Initialize small map
    if (document.getElementById('small-map')) {
        let smallMap = L.map('small-map').setView([53.809, -1.5235], 14);

        L.vectorGrid.protobuf('http://aaron.local:8000/services/leeds_map/tiles/{z}/{x}/{y}.pbf', {
            vectorTileLayerStyles,
            maxZoom: 14,
            attribution: '© OpenStreetMap contributors'
        }).addTo(smallMap);

        let planeMarker = L.marker([53.827, -1.593]).addTo(fullMap);
        planeMarker.bindPopup("AutoPiLot 1").openPopup();

    }

    // Initialize full map
    if (document.getElementById('full-map')) {
        let fullMap = L.map('full-map').setView([53.827, -1.593], 14);

        L.vectorGrid.protobuf('http://aaron.local:8000/services/leeds_map/tiles/{z}/{x}/{y}.pbf', {
            vectorTileLayerStyles,
            maxZoom: 14,
            attribution: '© OpenStreetMap contributors'
        }).addTo(fullMap);

        let planeMarker = L.marker([53.827, -1.5938]).addTo(fullMap);
        planeMarker.bindPopup("AutoPiLot 1").openPopup();
    }
});