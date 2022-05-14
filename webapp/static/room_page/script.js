const WS_PORT = 3100

const chatLog = document.getElementById("chat-log")
const roomName = btoa(window.location.pathname.slice(0,-1))
let author = sessionStorage.getItem("author")
if (!author) {
    author = "Anonymous"
}

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
    chatSocket.send(message)
    addMessage({message: message, author: author})
    messageInputDom.value = '';
};


const chatSocket = new WebSocket(
    `ws://${window.location.hostname}:${WS_PORT}/ws/${roomName}?username=${author}`
);

chatSocket.onmessage = function (e) {
    console.log(`Got message: ${e.data}`)
    const data = JSON.parse(e.data);
    if (data.author == author) return
    addMessage(data)
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

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
    messageContentSpan.innerHTML = marked.parse(data.message)
    messageContentSpan.classList.add("message-content")

    div.appendChild(messageAuthorSpan)
    div.appendChild(messageContentSpan)
    return div
}

function addMessage(data)
{
    let divMessage = prepareMessageDiv(data)
    chatLog.appendChild(divMessage)
    chatLog.scrollTop = chatLog.scrollHeight
}