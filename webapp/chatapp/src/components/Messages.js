import moment from "moment";
import React from "react";
import Message from "./Message";
import './Messages.css'

function Messages(props) {
    const messages = props.messages;
    const author = props.author;
    const handleScroll = props.handleScroll
    let last = null
    const messageItems = messages.map((message) => {
        let showTimestamp = false
        if (last == null)
        {
            showTimestamp = true
        }
        else {
            const dateDiff = moment(message.timestamp).diff(last.timestamp, "minutes")
            if (dateDiff > 30){
                showTimestamp = true
            }
        }
        last = message
        return (<Message 
            key={message.message_no} 
            data={message} 
            author={author}
            showTimestamp={showTimestamp}
        ></Message>)    
    });
    messageItems.reverse()
    return (
        <div className="messages" onScroll={handleScroll}>
            {messageItems}
        </div>
    );
  }

export default Messages;