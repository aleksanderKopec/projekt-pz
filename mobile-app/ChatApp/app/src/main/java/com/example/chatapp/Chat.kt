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
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import org.json.JSONObject
import java.net.ConnectException
import java.util.concurrent.Executor
import java.util.concurrent.Executors


class Chat : AppCompatActivity() {
    lateinit var session: DefaultClientWebSocketSession
    lateinit var adapter: MessageAdapter
    lateinit var messagelist: ArrayList<Message>
    private var scope = CoroutineScope(Dispatchers.IO)



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
            scope.launch {session.send(m.message!!)}


        }
    }

    fun runWebSiocketClient(){
        val client = HttpClient(CIO){
            install(WebSockets)
        }
        scope.launch {
            try{
                client.webSocket(method = HttpMethod.Get , host = "10.0.2.2", port = 3100, path = "/"){
                    session = this
                    session.send("XDXD")
                    while (true){
                        val receiveMessage = incoming.receive() as? Frame.Text
                        val message = receiveMessage?.readText()
                        Log.d("debug", message!!)
                        valz messageContent = JSONObject(message)
                        val m = Message(messageContent.getString("message"),messageContent.getString("author"))
                        runOnUiThread {
                            adapter.addNewMessage(m)
                        }

                    }
                }
            }
            catch(e:ConnectException){
                Toast.makeText(this@Chat, "Connection refused", Toast.LENGTH_SHORT).show()
                finish()
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