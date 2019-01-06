/*
* Author: Jan Bonne Aans
* Copyright: Jan Bonne Aans
* License: GPLv3
* Version: 1 Development
* Contact: jbaans > gmail.com
*
* Main interface for IOThermostat
*
* - Connect to the configured MQTT server
* - Subscribe to relevant topic
* - Run user interface
*
**/

// global variables
var MODES = ['Auto','Boost','On','Off', 'Sleep'];
var MIN_TEMPERATURE = 5;
var MAX_TEMPERATURE = 25;
var windowunloaded = false;
var t_average = 0;
var p_average = 0;
var h_average = 0;
var heateron = '';

function onConnected(){
    // subscribe to the topics
    for(var shorttopic in MQTTTopics){
        MQTTSubscribe( MQTTTopics[shorttopic] );
      }
}


function onMessage(topic, message){
    // process every new message
    MQTTData[topic] = message;
    var shorttopic = MQTTShorttopics[topic];
    
    if ( shorttopic.startsWith('d_') ){
        updateArrowIcon(shorttopic, message);
    }
    else if (shorttopic == 'heateron'){
        updateFlameIcon(message);
    }
    else if (shorttopic == 'mode'){
        setMode(message);
    }
    else if (shorttopic == 'modeendtime'){
        // do nothing
    }
    else{
        elementSetText(shorttopic, message);
    }
    updateModeEndtime();
}


// write data to HTML element
function elementSetText(elementId,data){

    var element = document.getElementById(elementId);
    if ( element !== null ){
        element.innerHTML = data;
    }
}


// get data from HTML element
function elementGetText(elementId){

    var element = document.getElementById(elementId);
    if ( element !== null ){
        return element.innerHTML;
    }
}


function updateArrowIcon(elementId, derivative){
    var elementArrow = document.getElementById(elementId)
    if ( elementArrow !== null ){
        if ( parseFloat(derivative) > 0.00001 ){
            elementArrow.src="img/up_lightblue.png";
            elementArrow.style.visibility = 'visible';
        }
        else if ( parseFloat(derivative) < -0.00001 ){
            elementArrow.src="img/down_lightblue.png";
            elementArrow.style.visibility = 'visible';
        }
        else {
            elementArrow.style.visibility = 'hidden';
        }
    }
}


function updateFlameIcon(enabled){
    var elementId = document.getElementById('flame');
    if ( elementId !== null ){
        if ( enabled == 'False' ){
            elementId.style.visibility = 'hidden';
        }
        else if ( enabled == 'True' ){
            elementId.style.visibility = 'visible';
        }
    }
}


function getRemainingTime(endtime){

    if ( endtime !== null ){
        endtime = endtime.split(','); // 'dayofweek,hour,minute'
        if ( endtime.length == 3){
            var now = new Date();
            var today = (now.getDay() - 1 + 7) % 7;    // getDay() has Sunday = 0, IOThermostat has Monday = 0
            var nowhour = now.getHours();
            var nowminute = now.getMinutes();

            var days = endtime[0] - today;
            var hours = endtime[1] - nowhour;
            var minutes = endtime[2] - nowminute;
            if (minutes < 0){
                hours -= 1;
                minutes = ( minutes + 60 ) % 60;
            }
            if (hours < 0){
                days -= 1;
                hours = ( hours + 24 ) % 24;
            }
            if (days < 0){
                days = ( days + 7 ) % 7;
            }
            return [days,hours,minutes];
        }
    }
}


function updateModeEndtime(){

    var endtime = MQTTData[ MQTTTopics['modeendtime'] ];
    var element = document.getElementById('mode');

    if ( element !== null && endtime !== null && endtime !== ''){

        var mode = getMode();
        var rt = getRemainingTime(endtime);

        if ((mode == 'Sleep' || mode == 'Boost' ) && rt !== null){

            var rtstring = '';

            if (rt[0] > 0){
                rtstring += rt[0] +'d';
            }

            if (rt[1] > 0){
                rtstring += rt[1] +'h';
            }

            if (rt[2] > 0){
                rtstring += rt[2] +'m';
            }

            element.value = mode + ' ('+rtstring+')';
        }
    }
}


// set mode
function setMode(mode){

    if ( MODES.includes(mode) ){
        var element = document.getElementById('mode');
        if ( element !== null ){
            element.value = mode;
        }
    }
}


// get mode
function getMode(){

    var element = document.getElementById('mode');
    if ( element !== null ){
        var mode = element.value;
        if ( mode.includes('Boost') ){
            mode = 'Boost';
        }
        else if ( mode.includes('Sleep') ){
            mode = 'Sleep';
        }
        return mode;
    }
}


//TODO: rename refresh to gotoMain
function refresh(){
    location.href='index.php';
}


function setTemperature(t){
    // set temperature on screen
    t = floatToStr(t)
    elementSetText( 'targettemperature',t );

    // publish set temperature
    MQTTPublish(MQTTTopics['targettemperature'],t);
}


function incrTemperature(negative){

    elementId = document.getElementById("targettemperature")
    if ( elementId !== null ){
        // get current set temperature
        var t = parseFloat( elementId.innerHTML );

        // increase it by 0.5 or negative 0.5 if set and within range
        if ( negative && t > MIN_TEMPERATURE ){
            t -= 0.5;
            setTemperature(t);
        } 
        else if ( !negative && t < MAX_TEMPERATURE ){
            t += 0.5;
            setTemperature(t);
        }
    }
}


function decrTemperature(){
    incrTemperature(true);
}

function nextInArray(array,value){
    index = (array.indexOf(value) + 1) % array.length;
    return array[index];
}

function rotateMode(){

    // update with elementGetText and elementSetText
    var mode = getMode();
    if ( mode !== null ){
        nextMode = nextInArray(MODES,mode);
        setMode(nextMode);
        MQTTPublish(MQTTTopics['mode'],nextMode);
    }
}


function gotoAdvanced(){
    location.href='advanced.php';
}

function gotoIndex(){
    location.href='index.php';
}


window.onunload = window.onbeforeunload = (function(){
    if (!windowunloaded){
        MQTTDisconnect();
        windowunloaded = true;
    }
});

// when page finished loading:
$(document).ready(function(){
    // disable right click / context menu
//    document.addEventListener('contextmenu', event => event.preventDefault());
    document.addEventListener('contextmenu', function(event){ event.preventDefault();}, true);

    // hide cursor if client is on touch screen device itself
    if (location.hostname === "localhost" || location.hostname === "127.0.0.1"){
        document.body.style.cursor = 'none';
        $('.button').css('cursor','none');
    }

    // connect to broker, tell it to call 
    // onConnected() when connecting succeeded
    // onMessage() when message received
    var credentials = MQTTgetCredentials();
    var user = credentials.user;
    var password = credentials.password;
    MQTTSetup(host,port,useSSL,user,password, onConnected, onMessage);  
    MQTTConnect();
});

    
	
