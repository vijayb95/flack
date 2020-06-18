document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        var crt = document.getElementById('create');
        crt.onclick = () => {
            const groupName = document.getElementById('groupName').value;
                socket.emit('submit group', {'group': groupName});
        }
    });

    socket.on('channels', data => {
        document.querySelector('#chnl').innerHTML = data.create;
    });

    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const selection = button.innerHTML;
                socket.emit('messages', {'selection': selection});
            };
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('message', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.selection}`;
        document.querySelector('#msg').append(li);
    });

});

