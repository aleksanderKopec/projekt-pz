package com.example.chatapp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.JsonReader
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.features.websocket.*
import io.ktor.http.*
import io.ktor.http.cio.websocket.*
import kotlinx.coroutines.runBlocking
import org.json.JSONObject


class Chat : AppCompatActivity() {
    lateinit var adapter: MessageAdapter
    lateinit var messagelist: ArrayList<Message>



    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chat_room)
        val login = intent.getStringExtra("senderId")
        val code = intent.getStringExtra("code")

        messagelist = ArrayList()
        adapter = MessageAdapter(context = applicationContext,messagelist, login )
        findViewById<RecyclerView>(R.id.RecyclerView).adapter = adapter
        findViewById<RecyclerView>(R.id.RecyclerView).layoutManager = LinearLayoutManager(this)
        addTestMessage(login)
        setupButton(login)
        runWebSiocketClient()



    }

    fun setupButton(login: String?){
        val button = findViewById<ImageView>(R.id.buttonSend)
        button.setOnClickListener {
            val messageView = findViewById<EditText>(R.id.messageBox)
            val m = Message(messageView.text.toString(), login)
            adapter.addNewMessage(m)
            messageView.text.clear()


        }
    }

    fun runWebSiocketClient(){
        val client = HttpClient(CIO){
            install(WebSockets)
        }
        runBlocking {
            client.webSocket(method = HttpMethod.Get , host = "127.0.0.1", port = 8765, path = "/"){
                while (true){
                    val receiveMessage = incoming.receive() as? Frame.Text
                    val message = receiveMessage?.readText()
                    Log.d("debug", message!!)
                    val messageContent = JSONObject(message)
                    val m = Message(messageContent.getString("message"),messageContent.getString("author"))
                    adapter.addNewMessage(m)

                }
            }
        }

    }
    fun addTestMessage(login: String?){
        val m1 = Message("To moja pierwsza wiadomosc",login )
        val m2 = Message("To wiadomosc od wysylacego", "sad")
        adapter.addNewMessage(m1)
        adapter.addNewMessage(m2)
    }

}