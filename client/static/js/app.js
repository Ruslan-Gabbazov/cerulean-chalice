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
        onOpen();
        onConnected(payload);
        startPing(10000);
    } else if (kind === AUTHORIZE) {
        onAuthorize(payload);
    } else if (kind === SEND) {
        let messages = onSend(payload);
        // showMessages(messages)
        chat_init(messages);
    } else if (kind === REMOVE) {
        onClose(payload);
    } else {
        console.log(`Unsupported event with kind ${kind} and payload ${payload}`)
    }
}


onConnected = (payload) => {
    connection_id = payload['connection_id'];
}

onAuthorize = (payload) => {
    connection_id = payload['connection_id'];
    let allowed = payload['allowed'];

    if (allowed) {
        // показать чат
        document.location.href = "../templates/chat.html"
    }
}


onSend = (payload) => {
    connection_id = payload['connection_id'];
    // showMessages(messages);
    return payload['messages']
}


// onRemove = (payload) => {
//     connection_id = payload['connection_id'];
//
//     // закрыть соединение
// }


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


ping = () => {
    console.log(`Ping connection: ${connection_id}`);
    connection.push(PING_EVENT, {
        connection_id: connection_id,
    });
}

startPing = (timeout) => {
    setInterval(() => {
        if (run) {
            ping();
        }
    }, timeout);
}


signIn = (nickname, password) => {
    console.log(`Sign in of connection: ${connection_id}`);
    connection.push(SIGNIN_EVENT, {
        connection_id: connection_id,
        nickname: nickname,
        password: password
    });
}


signUp = (nickname, password) => {
    console.log(`Sign up of connection: ${connection_id}`);
    connection.push(SIGNUP_EVENT, {
        connection_id: connection_id,
        nickname: nickname,
        password: password
    });
}


sendMessage = (message) => {
    console.log(`Send message from connection: ${connection_id}`);
    connection.push(MESSAGE_EVENT, {
        connection_id: connection_id,
        user_id: user_id,
        content: message
    });
}


disconnect = () => {
    console.log(`Close connection: ${connection_id}`);
    connection.push(DISCONNECT_EVENT, {
        connection_id: connection_id
    });
}
