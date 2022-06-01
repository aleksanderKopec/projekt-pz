package com.example.chatapp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import java.util.concurrent.Executors

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setupButton()


    }
    fun setupButton(){
        val button = findViewById<Button>(R.id.button)
        button.setOnClickListener{
            val loginView = findViewById<EditText>(R.id.login)
            val codeView = findViewById<EditText>(R.id.code)
            if(loginView.text.isNullOrBlank() || codeView.text.isNullOrBlank()){
                Toast.makeText(this@MainActivity, "Wrong", Toast.LENGTH_LONG).show()
                return@setOnClickListener
            }
            val intent: Intent = Intent(button.context, Chat:: class.java)
            intent.putExtra("senderId", loginView.text.toString())
            intent.putExtra("code", codeView.text.toString())


            startActivity(intent)

        }
    }
}