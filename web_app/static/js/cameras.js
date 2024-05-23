let intervalId = null;
/*
allows the camera feed to be toggled on and off when clicking the corresponding buttons in the web page
 */
function toggleCamera(cameraType) {
    let cameraDiv;
    let cameraUrl;

    if (cameraType === 'thermal') {
        cameraDiv = document.getElementById('thermal-camera');
        cameraUrl = '/camera/thermal_feed';
    } else if (cameraType === 'video') {
        cameraDiv = document.getElementById('video-camera');
        cameraUrl = '/camera/video_feed';
    }

    if (cameraDiv.style.display === 'none' || !cameraDiv.style.display) {
        cameraDiv.style.display = 'block';
        if (!cameraDiv.querySelector('img')) {
            let img = document.createElement('img');
            img.src = cameraUrl;
            img.width = cameraDiv.clientWidth;
            img.height = cameraDiv.clientHeight;
            cameraDiv.appendChild(img);
        }
        if (cameraType === 'thermal' && intervalId === null) {
            intervalId = setInterval(() => updateThermalFeed(camersDiv, cameraUrl), 2000)
        }
    } else {
        cameraDiv.style.display = 'none';
        let img = cameraDiv.querySelector('img');
        if (img) {
                cameraDiv.removeChild(img);
        }
    }
}

function updateThermalFeed(cameraDiv, cameraUrl) {
    let img = cameraDiv.querySelector('img');
    if (img) {
        img.src = cameraUrl + '?t=' + new Date().getTime(); // timestamp prevents caching
    }
}