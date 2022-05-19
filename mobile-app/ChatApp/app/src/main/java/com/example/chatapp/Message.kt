package com.example.chatapp

<<<<<<< HEAD
import io.ktor.util.*
import java.sql.Timestamp
import java.time.LocalDate
import java.time.LocalDateTime
import android.util.Base64
=======
import java.sql.Timestamp
import java.util.*
>>>>>>> 8f0ddd78b0fce2d5d4a77330145ef918f3f29423

class Message {
    var message: String? = null
    var senderId: String ? = null
<<<<<<< HEAD
    var timestamp: LocalDateTime ? = null

=======
    var timestamp: String ? = null
    var is_encrypted: Boolean? = false
>>>>>>> 8f0ddd78b0fce2d5d4a77330145ef918f3f29423

    var is_encrypted: Boolean? = false
    constructor(){}

<<<<<<< HEAD
    constructor(message: String?, senderId: String?, timestamp: LocalDateTime, isEncrypted: Boolean = false){

        this.senderId = senderId
        this.timestamp = timestamp
        this.is_encrypted = isEncrypted
        this.message = Base64.encodeToString(message!!.toByteArray(),Base64.DEFAULT)

=======
    constructor(message: String?, senderId: String?, timestamp: String?, isEncrypted: Boolean = false){
        this.message = message
        this.senderId = senderId
        this.timestamp = timestamp
        this.is_encrypted = isEncrypted

    }

    override fun toString(): String
    {
        return "message: $message, is_encrypted: $is_encrypted"
>>>>>>> 8f0ddd78b0fce2d5d4a77330145ef918f3f29423
    }

    override fun toString(): String
    {

        return "message: $message, is_encrypted: $is_encrypted"
    }


}