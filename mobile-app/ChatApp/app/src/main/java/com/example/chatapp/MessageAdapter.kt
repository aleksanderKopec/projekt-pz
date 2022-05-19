package com.example.chatapp

import android.content.Context
import android.util.Base64
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class MessageAdapter(val context: Context, val messageList: ArrayList<Message>, val yourid: String?):
    RecyclerView.Adapter<RecyclerView.ViewHolder>() {
    val ITEM_RECEIVE = 1
    val ITEM_SENT = 2



    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {

        if (viewType == ITEM_RECEIVE) {
            val view: View = LayoutInflater.from(context).inflate(R.layout.recive, parent, false)
            return  ReceiveViewHolder(view)

        } else {
            val view: View = LayoutInflater.from(context).inflate(R.layout.sent, parent, false)
            return  SentViewHolder(view)
        }
    }
    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        if(holder.javaClass == SentViewHolder:: class.java)
        {
            val currentMessage = messageList[position]
            val viewHolder = holder as SentViewHolder
            holder.sentMessage.text = currentMessage.message
            holder.author.text = currentMessage.senderId
<<<<<<< HEAD
            holder.timestamp.text = "${currentMessage.timestamp?.hour}:${currentMessage.timestamp?.minute}"
=======
            holder.timestamp.text = currentMessage.timestamp
>>>>>>> 8f0ddd78b0fce2d5d4a77330145ef918f3f29423
        }
        else
        {
            val currentMessage = messageList[position]
            val viewHolder = holder as ReceiveViewHolder
            holder.receiveMessage.text = currentMessage.message
            holder.author.text = currentMessage.senderId
<<<<<<< HEAD
            holder.timestamp.text = "${currentMessage.timestamp?.hour}:${currentMessage.timestamp?.minute}"
=======
            holder.timestamp.text = currentMessage.timestamp
>>>>>>> 8f0ddd78b0fce2d5d4a77330145ef918f3f29423
        }

    }


    override fun getItemViewType(position: Int): Int {
        val currentMessage = messageList[position]
        if(currentMessage.senderId == yourid ){
            return ITEM_SENT
        }
        return ITEM_RECEIVE
    }

    override fun getItemCount(): Int {
        return messageList.size
    }
    class SentViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView){
        val sentMessage = itemView.findViewById<TextView>(R.id.txt_sent_message)
        val author = itemView.findViewById<TextView>(R.id.authors)
        val timestamp = itemView.findViewById<TextView>(R.id.times)

    }
    class ReceiveViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView){
        val receiveMessage = itemView.findViewById<TextView>(R.id.txt_recive_message)
        val author = itemView.findViewById<TextView>(R.id.author)
        val timestamp = itemView.findViewById<TextView>(R.id.time)

    }
    fun addNewMessage(message: Message){
        val decode = Base64.decode(message.message, Base64.DEFAULT)
        Log.d("Socket", message.message.toString())
        message.message = decode.decodeToString()
        Log.d("Socket", message.message.toString())
        messageList.add(message)
        notifyItemChanged(messageList.size -1 )


    }
}