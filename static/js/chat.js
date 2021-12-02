let chatList = document.getElementsByClassName("chat_list");

let chatSocket = null;
let msgHistory = document.getElementsByClassName("msg_history")[0];

function chatRoom(target, pk, member_pk) {
    if (target.classList[1] === "chat_clicked") {
        target.classList.remove("chat_clicked");
    } else {
        for (let i = 0; i < chatList.length; i++) {
            chatList[i].classList.remove("chat_clicked");
        }
        target.classList.add("chat_clicked");
    }


    while (msgHistory.firstChild) {
        msgHistory.removeChild(msgHistory.firstChild);
    }

    let member = member_pk;
    $.ajax({
        url: "/chat/msgs/" + pk,
        method: "GET",
        dataType: "json",
        processData: false,
        contentType: false,
    }).done((data) => {
        loadMessages(data, member);
        // makeConnection();
    });

    /*
    chatSocket 연결
     */
    if(chatSocket) {
        reconnect(pk, member_pk);
    } else {
        openConnect(pk, member_pk);
    }

}

function loadMessages(msgs, member) {
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

function reconnect(pk, member_pk) {
    chatSocket.close();
    waitForSocketClose(chatSocket, function () {
        openConnect(pk, member_pk);
    });
}

function openConnect(pk, member_pk) {
    let ws = window.location.protocol == "https:" ? "wss" : "ws";
    chatSocket = new WebSocket(
        ws + '://' + window.location.host +
        '/ws/chat/' + pk + '/' + member_pk + '/');
    // Other logic codes here
    chatSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        let sender = data['sender'];
        let message = data['message'];
        let timestamp = data['timestamp'];
        let newMsg = document.createElement('div');
        sender === member ? newMsg.setAttribute('class', 'outgoing_msg')
            : newMsg.setAttribute('class', 'incoming_msg');

        let senderDOM = document.createElement('div');
        sender === member ? senderDOM.setAttribute('class', 'outgoing_sender')
            : senderDOM.setAttribute('class', 'incoming_sender');
        let senderName = document.createTextNode(data['senderName']);
        senderDOM.appendChild(senderName);
        newMsg.appendChild(senderDOM);

        let innerNewMsg = document.createElement('div');
        sender === member ? innerNewMsg.setAttribute('class', 'sent_msg')
            : innerNewMsg.setAttribute('class', 'received_msg');

        let msg = document.createElement('div');
        if (member !== sender) msg.setAttribute('class', 'received_withd_msg');


        let p = document.createElement('p');
        let text = document.createTextNode(message);

        let time = document.createElement('span');
        let timeText = document.createTextNode(timestamp);

        p.appendChild(text);
        time.setAttribute('class', 'time_date');
        time.appendChild(timeText);

        msg.appendChild(p);
        msg.appendChild(time);

        innerNewMsg.appendChild(msg);
        newMsg.appendChild(innerNewMsg);

        msgHistory.appendChild(newMsg);

        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    };

    document.querySelector('#write_msg').focus();
    document.querySelector('#write_msg').onkeypress = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#msg_send_btn').click();
        }
    };
    document.querySelector('#msg_send_btn').onclick = function (e) {
        let messageInputDom = document.querySelector('#write_msg');
        let message = messageInputDom.value;

        chatSocket.send(JSON.stringify({
            'message': message,
            'sender': member_pk
        }));

        messageInputDom.value = '';
    };
}

function waitForSocketClose(socket, callback) {
    setTimeout(function () {
        if (socket.readyState === 3) {
            console.log("closed");
            callback();
        } else {
            waitForSocketClose(socket, callback);
        }
    }, 10);
}