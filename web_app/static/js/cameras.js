    function toggleCamera(cameraType) {
    let cameraDiv;
    if (cameraType === 'thermal') {
        cameraDiv = document.getElementById('thermal-camera');
    } else if (cameraType === 'video') {
        cameraDiv = document.getElementById('video-camera');
    }

    if (cameraDiv.style.display === 'none') {
        cameraDiv.style.display = 'block'; // Show camera feed
        fetch(`/enable-camera/${cameraType}`);
    } else {
        cameraDiv.style.display = 'none'; // Hide camera feed
        fetch(`/disable-camera/${cameraType}`);
    }
}
