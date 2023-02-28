chat_init = (messages) => {

    document.addEventListener('DOMContentLoaded', function () {

        const messagesContainer = document.querySelector("#message_container");
        const messageInput = document.querySelector("[name=message_input]");
        const sendMessageButton = document.querySelector("[name=send_message_button]");


        const newMessage = document.createElement("div");
        for (let message in messages) {
            newMessage.innerHTML = message;
            messagesContainer.appendChild(newMessage);
        }


        sendMessageButton.onclick = function () {
            sendMessage(messageInput.value);
        };

    }, false);

};


