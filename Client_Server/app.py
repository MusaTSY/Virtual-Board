from flask import Flask, render_template, request, jsonify
import datetime
import socket

app = Flask(__name__)

FORMAT = "utf-8"
HEADER = 64
SOCKET_SERVER_IP = "104.162.138.197"
SOCKET_SERVER_PORT = 9999

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((SOCKET_SERVER_IP, SOCKET_SERVER_PORT))


@app.route('/receive_message', methods=['POST'])
def receive_message():
    data = request.form.get('message')
    name = request.form.get('username')
    location = request.form.get('location')
    eventtime= request.form.get('eventtime')
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')

    try:
        message = f"POST: [{name}]:{data}  [LOCATION]:{location}  [EVENTTIME]:{eventtime} [DATE POSTED]:{formatted_date}".encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        socket_client.send(send_length)
        socket_client.send(message)
        response = socket_client.recv(1024).decode('utf-8')
        return render_template('index.html', response=response)
    except Exception as e:
        return render_template('index.html', response=f'Error: {str(e)}')



@app.route('/remove_messages', methods=['POST'])
def remove_message():
    try:
        message_to_remove = request.form.get('message_to_remove')
        message_to_remove = f"REMOVE: {message_to_remove}".encode(FORMAT)
        msg_length = len(message_to_remove)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        socket_client.send(send_length)
        socket_client.send(message_to_remove)
        response = socket_client.recv(4096).decode('utf-8')
        messages = response.split('\n')
        return render_template('board.html', messages=messages)
    except Exception as e:
        return render_template('board.html', messages=[f'Error: {str(e)}'])

     


@app.route('/check_messages', methods=['GET', 'POST'])
def check_messages():
    try:
        check_msg = "CHECK:".encode(FORMAT)
        msg_length = len(check_msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        socket_client.send(send_length)
        socket_client.send(check_msg)
        response = socket_client.recv(4096).decode('utf-8')
        messages = response.split('\n')
        return render_template('board.html', messages=messages)
    except Exception as e:
        return render_template('board.html', messages=[f'Error: {str(e)}'])


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)