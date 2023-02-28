path = '${CONNECT_PATH}';
init()

document.getElementById('enter').addEventListener('click', enterListener);

function enterListener() {

    const loginInput = document.querySelector("[name=login]");
    const passwordInput = document.querySelector("[name=password]");
    const checkboxButton = document.querySelector("[name=register]");

    if (checkboxButton.checked) {
        signUp(loginInput.value, passwordInput.value);
    } else {
        signIn(loginInput.value, passwordInput.value);
    }
}


document.addEventListener('DOMContentLoaded', function () {

    const messagesContainer = document.querySelector("#message_container");
    const messageInput = document.querySelector("[name=message_input]");
    const sendMessageButton = document.querySelector("[name=send_message_button]");

    showMessages = (messages) => {

        const newMessage = document.createElement("div");
        for (let message of messages) {
            // newMessage.textContent += `${message.user_id} : ${message.datetime} : ${message.content}`;
            // messagesContainer.appendChild(newMessage);
            addMessage(message)
        }
    }

    function addMessage(message) {
        let block = document.createElement('div');
        block.classList.add('block');
        block.style.backgroundColor = `hsl(${Math.random()*360},55%,85%)`;
        block.textContent = `${message.user_id} : ${message.datetime} : ${message.content}`;
        setTimeout(e => block.style.opacity = 1);
        messagesContainer.append(block);
    }

    sendMessageButton.onclick = function () {
        sendMessage(messageInput.value);
    };

}, false)



