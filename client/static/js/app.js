init = () => {
    handleConnection()
}


handleConnection = () => {
    connection = new Connection(onOpen, onMessage, onClose, onError);
}


onMessage = (msg) => {
    let event = JSON.parse(msg.data);
    const kind = event['kind'];
    const payload = event['payload'];
    console.log(`New event with kind ${kind} and payload ${JSON.stringify(payload)}`);
    if (kind === INITIAL) {
        onFullyConnected(payload);
    } else if (kind === ADD) {

    } else if (kind === MOVE) {

    } else if (kind === REMOVE) {

    } else {
        console.log(`Unsupported event with kind ${kind} and payload ${payload}`)
    }
}

onFullyConnected = (payload) => {
    connection_id = payload[' connection_id'];
    connection.push(CONNECT_EVENT, {
        connection_id: connection_id,
        user_id: user_id,
        nickname: nickname,
        password: password
    });

    for (let user of payload['users']) {

    }

}

ping = () => {
    if (!run) return;
    console.log(`Ping connection: ${id}`);
    connection.push(PING_EVENT, {
        connection_id: connection_id,
    });
}


onOpen = () => {
    console.log('WebSocket connection opened');
}


onClose = () => {
    console.log('WebSocket connection closed');
    connection.push(
        DISCONNECT_EVENT,
        {
            connection_id: connection_id,
        }
    );
    run = false;
}


onError = (e) => {
    console.log(`Connection closed with error ${e}`);
    run = false;
}
