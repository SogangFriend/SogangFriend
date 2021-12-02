function loadMessages(msgHistory, msgs, member) {
    /*
Msg log 에 History 불러오기
 */

    for (let j = 0; j < msgs.length; j++) {
        let newMsg = document.createElement('div');
        msgs[j]['sender_id'] == member ? newMsg.setAttribute('class', 'outgoing_msg')
            : newMsg.setAttribute('class', 'incoming_msg');
        let sender = document.createElement('div');
        msgs[j]['sender_id'] == member ? sender.setAttribute('class', 'outgoing_sender')
            : sender.setAttribute('class', 'incoming_sender');
        let senderName = document.createTextNode(msgs[j].sender_name);
        sender.appendChild(senderName);
        newMsg.appendChild(sender);


        let innerNewMsg = document.createElement('div');
        msgs[j]['sender_id'] == member ? innerNewMsg.setAttribute('class', 'sent_msg')
            : innerNewMsg.setAttribute('class', 'received_msg');

        let msg = document.createElement('div');
        if (msgs[j]['sender_id'] != member) msg.setAttribute('class', 'received_withd_msg');

        let p = document.createElement('p');
        let text = document.createTextNode(msgs[j].message);

        let time = document.createElement('span');
        let timeText = document.createTextNode(msgs[j].timestamp);

        p.appendChild(text);
        time.setAttribute('class', 'time_date');
        time.appendChild(timeText);

        msg.appendChild(p);
        msg.appendChild(time);

        innerNewMsg.appendChild(msg);
        newMsg.appendChild(innerNewMsg);

        msgHistory.appendChild(newMsg);
    }
    $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
}

