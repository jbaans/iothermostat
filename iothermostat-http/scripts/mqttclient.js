/*
* Author: Jan Bonne Aans
* Copyright: Jan Bonne Aans
* License: GPLv3
* Version: 1 Development
* Contact: jbaans > gmail.com
*
* PAHO MQTT Client interface for IOThermostat
*
* - Connect to the configured MQTT server
* - Subscribe to topics
* - Publish to topics
* - Receive data
*
**/


var user;
var password;
var onconnectfun;
var onmessagefun;
var host;
var port;
var useSSL;
var mqtt;
var clientId = 'js-paho-mqttws-client-' + (Math.floor((Math.random() * 1000000) + 1));
var connected_flag = 0;
var reconnectTimeout = 15000;

// set to true to enable logging to console
var DEBUG = true;   


function floatToStr(num) {

    return num.toString().indexOf('.') === -1 ? num.toFixed(1) : num.toString();
}


function log(message){

    if (DEBUG){
        console.log(message);
    }
}


function onConnectionLost(){

    log("MQTT connection lost, reconnecting..");
    connected_flag=0;
    setTimeout(MQTTConnect, reconnectTimeout);
}


function onFailure(message) {

    log('MQTT connection failed, reconnecting..');
    setTimeout(MQTTConnect, reconnectTimeout);
}


function onMessageArrived(message){

    var topic = message.destinationName;
    var message = message.payloadString;
    log('MQTT Received: '+topic+': '+message);

    onmessagefun(topic, message);
    
}


function onConnected(recon,url){

    log(" in onConnected " +reconn);
}


function onConnect() {

    log("Connected to MQTT broker "+host +" on port "+port);
    connected_flag = 1;
    
    onconnectfun();
}


// this is a bit ugly with underscores
function MQTTSetup(_host, _port, _useSSL, _user, _password, _onconnectfun, _onmessagefun){
    host = _host;
    port = _port;
    user = _user;
    useSSL = _useSSL;
    password = _password;
    onconnectfun = _onconnectfun;
    onmessagefun = _onmessagefun;
}


function MQTTConnect(){

    log("Connecting to " + host + " on port " + port);    
    mqtt = new Paho.MQTT.Client(host,port,clientId);
    
    var options = {
        useSSL: useSSL,
        timeout: 3,
        onSuccess: onConnect,
        onFailure: onFailure,
    };

    if (typeof user !== 'undefined'){
            options.userName = user
    }

    if (typeof password !== 'undefined'){
            options.password = password
    }

    mqtt.onConnectionLost = onConnectionLost;
    mqtt.onMessageArrived = onMessageArrived;
    mqtt.onConnected = onConnected;
    mqtt.onConnect = onConnect;

    mqtt.connect(options);
}


function MQTTDisconnect(){
    mqtt.disconnect();
}


function MQTTSubscribe(topic){

    if (connected_flag==0){
        log('Not connected so can\'t subscribe');
        return false;
    }
    log("Subscribing to: "+topic);
    mqtt.subscribe(topic);
    log("Subscribed to: "+topic);
}


function MQTTPublish(topic, message){

    if (connected_flag==0){
        log('Not Connected so can\'t send');
        return false;
    }
    var qos=0;
    var retained=true;
    mqtt.send(topic,message,qos,retained);
    log("Sent: "+topic+":"+message);    
}

	
