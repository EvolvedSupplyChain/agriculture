from flask import Flask
import paho.mqtt.client as mqtt

app = Flask(__name__)

topic = 'viperControl'
#topic2 = 'bar'
port = 5000
recievedMessage = ""

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    #client.publish(topic2, "STARTING SERVER")
    #client.publish(topic2, "CONNECTED")
    client.publish(topic, "returnSettings")


def on_message(client, userdata, msg):
    #client.publish(topic2, "MESSAGE")
    #if msg == "r
    global recievedMessage = msg

@app.route('/')
def hello_world():
    #return 'Hello World! I am running on port ' + str(port)
    return "Current Settings: " + recievedMessage 

if __name__ == '__main__':
    client = mqtt.Client()
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(20.236.13.82)
    client.loop_start()

    app.run(host='0.0.0.0', port=port)