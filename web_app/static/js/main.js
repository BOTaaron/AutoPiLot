document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    // Listen for console output
    socket.on('console_output', function(msg) {
        var textarea = document.getElementById('console');
        textarea.value += msg + '\n';  // Append message to textarea
        textarea.scrollTop = textarea.scrollHeight;
    });

    // Form submission to send command
    document.getElementById('command-form').onsubmit = function(e) {
        e.preventDefault();
        var input = document.getElementById('command-input');
        socket.emit('console_input', input.value);  // Send command to server
        input.value = '';  // Clear input after sending
    };
});
