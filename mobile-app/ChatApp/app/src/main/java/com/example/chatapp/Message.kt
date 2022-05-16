package com.example.chatapp

import java.sql.Timestamp
import java.util.*

class Message {
    var message: String? = null
    var senderId: String ? = null
    var timestamp: String ? = null
    var is_encrypted: Boolean? = false

    constructor(){}

    constructor(message: String?, senderId: String?, timestamp: String?, isEncrypted: Boolean = false){
        this.message = message
        this.senderId = senderId
        this.timestamp = timestamp
        this.is_encrypted = isEncrypted

    }

    override fun toString(): String
    {
        return "message: $message, is_encrypted: $is_encrypted"
    }
}