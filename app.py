from flask import Flask,render_template ,request, jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
import sqlite3

connection = sqlite3.connect("data.db")

connection.close()




global global_topic
global global_payload

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0 # refresh time in seconds
app.config['SECRET_KEY'] = 'donsky!'
topic = 'flask/delight'

socketio = SocketIO(app, cors_allowed_origins='*')
mqtt_client = Mqtt(app)


@app.route('/')
def index():
    # global global_topic
    # global global_payload
    #return render_template('index.html',topic=global_topic,payload=global_payload)
    return render_template('index.html')


"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    print("Generating random sensor values")
    while True:
        temperature_value = round(random() * 100, 3)
        humidity_value = round(random() * 100, 3)
        socketio.emit('updateSensorData', {'humidity': humidity_value ,'temperature': temperature_value, "date": get_current_datetime()})
        socketio.sleep(10)


"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

#AJAX TO UPDATE TOPIC VA PAYLOAD
@app.route('/get_data')
def get_data():
    global global_topic
    global global_payload
    data = {'topic':global_topic
    , 'payload':global_payload }
    return jsonify(data)


#mqtt function
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
       mqtt_client.publish(topic, "I'm from flask")
   else:
       print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global global_topic
    global global_payload
    data = dict(
       topic=message.topic,
       payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))

    global_topic = data['topic']
    global_payload = data['payload']

def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

#end mqtt function
if __name__ == '__main__':

   app.run(host='127.0.0.1', port=5000)
   socketio.run(app)