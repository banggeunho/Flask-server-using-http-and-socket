from flask_socketio import SocketIO
from flask import Flask

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecretMg7Mukhlis7HelloFromThisWorld!'
sio = SocketIO(app)

#sio = socketio.Server()
#app = Flask(__name__)


@app.route('/')
def index():
    """Serve the client-side application."""
    return "Server ROOT DIR"

@sio.on('service')
def receive(data):
    print(data)


# @sio.on('messagedetection', namespace='/')
# def messagedetection(Nickname, msg, uniqueId, userjoined):
#     msg = {"message":msg, "senderNickname":Nickname, "uniqueId":uniqueId}
#     #print(Nickname + " : " + str(msg))
#     sio.emit('message', msg ,broadcast=True)
#
# @sio.on('disconnect')
# def disconnect():
#     sio.emit("userdisconnect"," user has left ",broadcast=True)

if __name__ == '__main__':
    sio.run(app,host="0.0.0.0",port=5001,debug=False)