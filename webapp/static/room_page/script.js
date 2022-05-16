require.config({
    paths: {
        'crypto-js': '../packages/bower_components/crypto-js/crypto-js'
    }
})

const WS_PORT = 8000

const chatLog = document.getElementById("chat-log")
const roomName = btoa(window.location.pathname.slice(1,-1))
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
    const password = document.querySelector('#chat-message-password').value
    let messageObject = {
        "message": btoa(message),
        "is_encrypted": false
    }
    if (!message) return
    if (password != "")
    {
        require(["crypto-js"], (CryptoJS) => {
            messageObject.is_encrypted = true
            messageObject.message = CryptoJS.AES.encrypt(message, password).toString()
        })
    }
    console.log("Sending:")
    console.log(JSON.stringify(messageObject))
    chatSocket.send(JSON.stringify(messageObject))
    addMessage({message: message, author: author})
    messageInputDom.value = '';
};

//loadPreviousMessages()

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

function getMessages(channelId, messageId, count)
{
    baseUrl = `http://${window.location.hostname}:${WS_PORT}/api/${channelId}`
    url = ''
    if (messageId && count)
    {
        url = baseUrl + `?message_id=${messageId}&number_of_messages=${count}`
    }
    else if (messageId)
    {
        url = baseUrl + `?message_id=${messageId}`
    }
    else if (count)
    {
        url = baseUrl + `?number_of_messages=${count}`
    }
    return fetch(
        url,
        {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        })
}

function loadPreviousMessages()
{
    getMessages(roomName, 5, 5)
    .then((messages) =>{
        console.log(messages)
        messages = JSON.parse(messages)
        messages.json.messages.forEach(message => {
            addMessage(message)
        });
    })
}