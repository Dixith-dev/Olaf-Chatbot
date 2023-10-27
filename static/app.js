class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.mesage = [];

    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({key}) => {
            if (key === 'Enter') {
                this.onSendButton(chatBox)
            }
        })

    }


    toggleState(chatBox) {
        this.state = !this.state;
        
        if (this.state) {
            chatBox.classList.add('chatbox--active');
        } else {
            chatBox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatBox) {
        var textFiled = chatBox.querySelector('input');
        let text1 = textFiled.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }

        this.mesage.push(msg1)

        // 'http://127.0.0.1:5000/predict
        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.mesage.push(msg2)
            this.updateChatText(chatBox)
            textFiled.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatBox)
            textFiled.value = ''
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.mesage.slice().reverse().forEach(function(item) {
            if (item.name === "Sam") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatmessage = this.args.chatBox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

}

function sendRequest(message) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", $SCRIPT_ROOT + '/predict', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var json = JSON.parse(xhr.responseText);
      let msg2 = { name: "Sam", message: json.answer };
      chatbox.mesage.push(msg2)
      chatbox.updateChatText(chatbox.args.chatBox)
    }
  };
  var data = JSON.stringify({"message": message});
  xhr.send(data);
}

const chatbox = new Chatbox();
chatbox.display();