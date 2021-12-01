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

    /*
    Msg log 에 History 불러오기
     */
    for (let i = 0; i < rms.length; i++) {
        if (rms[i].pk === pk) {
            for (let j = 0; j < rms[i].msgs.length; j++) {
                let newMsg = document.createElement('div');
                rms[i].msgs[j].sender === member ? newMsg.setAttribute('class', 'outgoing_msg')
                    : newMsg.setAttribute('class', 'incoming_msg');
                let sender = document.createElement('div');
                rms[i].msgs[j].sender === member ? sender.setAttribute('class', 'outgoing_sender')
                    : sender.setAttribute('class', 'incoming_sender');
                let senderName = document.createTextNode(rms[i].msgs[j].senderName);
                sender.appendChild(senderName);
                newMsg.appendChild(sender);


                let innerNewMsg = document.createElement('div');
                rms[i].msgs[j].sender === member ? innerNewMsg.setAttribute('class', 'sent_msg')
                    : innerNewMsg.setAttribute('class', 'received_msg');

                let msg = document.createElement('div');
                if (rms[i].msgs[j].sender !== member) msg.setAttribute('class', 'received_withd_msg');

                let p = document.createElement('p');
                let text = document.createTextNode(rms[i].msgs[j].message);

                let time = document.createElement('span');
                let timeText = document.createTextNode(rms[i].msgs[j].timestamp);

                p.appendChild(text);
                time.setAttribute('class', 'time_date');
                time.appendChild(timeText);

                msg.appendChild(p);
                msg.appendChild(time);

                innerNewMsg.appendChild(msg);
                newMsg.appendChild(innerNewMsg);

                msgHistory.appendChild(newMsg);
            }
        }
    }
    $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);

    /*
    chatSocket 연결
     */
    const makeConnection = () => {
        chatSocket = new WebSocket(
            'ws://' + window.location.host +
            '/ws/chat/' + pk + '/' + member_pk + '/');
        // Other logic codes here
        chatSocket.onmessage = function (e) {
            let data = JSON.parse(e.data);
            let sender = data['sender'];
            let message = data['message'];
            let timestamp = data['timestamp'];
            console.log(data['message']);
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

        let keyDown = false;
        document.querySelector('#write_msg').focus();
        document.querySelector('#write_msg').onkeypress = function (e) {
            if (e.keyCode === 13) {  // enter, return
                keyDown = true;
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
        chatSocket.onclose = () => {
            chatSocket = null
        };
    };
    if (chatSocket) {
        chatSocket.onclose = makeConnection;
        chatSocket.close();
    } else {
        makeConnection();
    }
}
