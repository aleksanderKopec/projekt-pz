package com.example.chatapp

import io.ktor.util.*
import java.sql.Timestamp
import java.time.LocalDate
import java.time.LocalDateTime
import android.util.Base64

class Message {
    var message: String? = null
    var senderId: String ? = null
    var timestamp: LocalDateTime ? = null


    var is_encrypted: Boolean? = false
    constructor(){}

    constructor(message: String?, senderId: String?, timestamp: LocalDateTime, isEncrypted: Boolean = false){

        this.senderId = senderId
        this.timestamp = timestamp
        this.is_encrypted = isEncrypted
        this.message = Base64.encodeToString(message!!.toByteArray(),Base64.DEFAULT)

    }

    override fun toString(): String
    {

        return "message: $message, is_encrypted: $is_encrypted"
    }


}