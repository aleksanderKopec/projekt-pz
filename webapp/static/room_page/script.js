const WS_PORT = 8765

const chatLog = document.getElementById("chat-log")
let author = sessionStorage.getItem("author")
if (!author) {
    author = "Anonymous"
}

function prepareMessageDiv(data)
{
    let div = document.createElement("div")
    div.classList.add("message")
    if (author === data.author)
    {
        div.classList.add("my-message")
    }

    let messageAuthorSpan = document.createElement("span")
    messageAuthorSpan.textContent = data.author
    messageAuthorSpan.classList.add("message-author")
    let messageContentSpan = document.createElement("span")
    messageContentSpan.textContent = data.message
    messageContentSpan.classList.add("message-content")

    div.appendChild(messageAuthorSpan)
    div.appendChild(messageContentSpan)
    return div
}

// const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    //`ws://${window.location.host}:${WS_PORT}/chat/${roomName}`
    `ws://${window.location.hostname}:${WS_PORT}`
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    let divMessage = prepareMessageDiv(data)
    chatLog.appendChild(divMessage)
    chatLog.scrollTop = chatLog.scrollHeight
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (!message) return
    chatSocket.send(JSON.stringify({
        'author': author,
        'message': message
    }));
    messageInputDom.value = '';
};