/*
* Author: Jan Bonne Aans
* Copyright: Jan Bonne Aans
* License: GPLv3
* Version: 1 Development
* Contact: jbaans > gmail.com
*
* Schedule interface for IOThermostat
*
* - Connect to the configured MQTT server
* - Subscribe to schedule topic
* - load schedule
* - validate schedule
* - modify schedule with UI
* - save / Publish schedule
*
**/

var DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
var TEMPERATURE_UNIT = '&#8451;';
var MIN_TEMPERATURE = 5;
var MAX_TEMPERATURE = 25;
var schedule; // Array of Strings

Array.prototype.compare = function(array) {
  if (!array) {
    return false;
  }
  if (this.length !== array.length) {
    return false;
  }
  for (var i = 0, l = this.length; i < l; i++) {
    if (this[i] instanceof Array && array[i] instanceof Array) {
      if (!this[i].compare(array[i])) {
        return false;
      }
    }
    else if (this[i] !== array[i]) {
      return false;
    }
  }
  return true;
}

// generate a select element with options first..last (with zero padding)
function getNumberSelectHTML(first,last,zeropadding){
    var options = "";
    for(var i=first;i<=last;i++){
        if(zeropadding){
            // zero pad first 10 numbers
            for( i=i; i<10 & i<=last;i++){
                options += '<option value="'+i+'">0'+i+'</option>';
            }
        }
        options += '<option value="'+i+'">'+i+'</option>';
    }    
    return '<select class="custom-select">'+options+'</select>';
}

// generate a select element with options first..last (with zero padding)
function getFloatSelectHTML(first,last,step){
    var options = "";
    for(var i=first;i<=last;i+=step){
        options += '<option value="'+i.toFixed(1)+'">'+i.toFixed(1)+'</option>';
    }    
    return '<select class="custom-select">'+options+'</select>';
}

// generate a select element with options from array
function getStringSelectHTML(array){
    var options = "";
    for(var i=0;i<array.length;i++){
        options += '<option value="'+i+'">'+array[i]+'</option>';
    }     
    return '<select class="custom-select">'+options+'</select>';
}

function getAddButtonHTML(){
    return '<input type="button" class="button-css-s" value="+" onclick="addRow(this)"/>';
}

function getRemoveButtonHTML(){
    return '<input type="button" class="button-css-s" value="-" onclick="removeRow(this)"/>';
}  

// return an array with required HTML input elements 
function getInputHTML(removeButton){
    result = [getStringSelectHTML(DAYS)+'&emsp;',   // day
              getNumberSelectHTML(0,23,true)+' :',   // hh
              getNumberSelectHTML(0,59,true)+'&emsp;',   // mm
              getNumberSelectHTML(0,23,true)+' :',   // hh
              getNumberSelectHTML(0,59,true)+'&emsp;',   // mm
              getFloatSelectHTML(MIN_TEMPERATURE,MAX_TEMPERATURE,0.5) + ' ' + TEMPERATURE_UNIT ]; // temperature

    var buttonHTML = getAddButtonHTML();
    if (removeButton){
        buttonHTML += getRemoveButtonHTML();
    }
    result.push( buttonHTML );
               
    return result;
}

// removes the table row the current element is in
function removeRow(currElement) {
    var parentRowIndex = currElement.parentNode.parentNode.rowIndex;
    document.getElementById("scheduletable").deleteRow(parentRowIndex);
}

// add a table row after the one the current element is in
function addRow(currElement) {
    // get current row values
    var parentRowIndex = currElement.parentNode.parentNode.rowIndex;
    var parentRowValues = $('select',currElement.parentNode.parentNode).map(function(){
                                return this.value;
                            }).get();

    // add new row
    var newRow = document.getElementById("scheduletable").insertRow(parentRowIndex+1);
    var inputHTML = getInputHTML(true);
    for ( var i = 0; i < inputHTML.length; i++){
        var cell = newRow.insertCell(i);
        cell.innerHTML=inputHTML[i];
    }
    
    // apply parent values to select elements of new row
    var selectElements = $('select',newRow);
    for(var i = 0;i<parentRowValues.length;i++){
        selectElements.eq(i).val(parentRowValues[i]);
    }
}

//function isOneDecimalFloat(value){
//    return (!isNaN(value) && value.toString().indexOf('.') == value.toString().length-2 );
//}

function validateSchedule(s){

    // validate schedule values, should be all true:
    result = true;
      
    if (!s){
        console.log('Warning: Empty schedule!');
        return true;
    }
      
    // number of positions
    if ( (s.length % 6) !== 0 ){
        alert('Error: Bad number of values ('+s.length+') in schedule ("'+s+'")!');
        return false;
    }

    // convert Array of Strings to Array of numbers
    s = s.map(Number);

    var rowCount = s.length / 6;    
    // value format and within range
    for ( var i = 0; i < 6*rowCount; i+=6){
        if (!(  (!isNaN(s[i+0]) && s[i+0] >= 0 && s[i+0] < 7) &&
                (!isNaN(s[i+1]) && s[i+1] >= 0 && s[i+1] < 24) &&
                (!isNaN(s[i+2]) && s[i+2] >= 0 && s[i+2] < 60) &&
                (!isNaN(s[i+3]) && s[i+3] >= 0 && s[i+3] < 24) &&
                (!isNaN(s[i+4]) && s[i+4] >= 0 && s[i+4] < 60) &&
                (!isNaN(s[i+5]) && s[i+5] >= MIN_TEMPERATURE && s[i+3] <= MAX_TEMPERATURE)
            )){
            result = false;
            alert('Error: Bad schedule format in row '+(i/6+1)+'!');
        }
    }
    
    // values are sane
    for ( var i = 0; i < 6*rowCount; i+=6){
                // end hour is after start hour
        if (!(  ((s[i+3] > s[i+1]) ||
                 // or end hour is equal to start hour and start minute is after end minute
                 (s[i+3] === s[i+1] && s[i+4] > s[i+2])
                ) &&
                // and start timepoint should be after previous end timepoint
                (i == 0 || 
                    // start day is after previous start day
                    ((s[i+0] > s[i-6+0]) || 
                    // or start day is previous end day and start hour is after previous end hour
                     (s[i+0] === s[i-6+0] && s[i+1] > s[i-6+3]) || 
                    // or start day is previous end day and start hour is previous end hour and start minute is after previous end minute
                     (s[i+0] === s[i-6+0] && s[i+1] === s[i-6+3] && (s[i+2] > s[i-6+4]))
                    )
                ) 
            )){
            result = false;
            alert('Error: Schedule in row '+(i/6+1)+' makes no sense!');
        }
    }        
                        
    return result;
}

function loadSchedule(schedule_temp){
    
    if ( validateSchedule(schedule_temp) ){
    
        // add/remove the right amount of rows
        var loadRowCount = schedule_temp.length/6;
        var rowCount = $('#scheduletable tr').length-1;
        difference = loadRowCount-rowCount;
        
        if (difference<0){
        
            // remove surplus rows
            $("#scheduletable tr").slice(difference).remove();
        } else if (difference>0){
        
            // or add rows
            for(var i = 0;i<difference;i++){
                document.getElementById('masteraddbutton').click();
            }
        }

        var selectElements = $('select');
        for(var i = 0;i<schedule_temp.length;i++){
        
            selectElements.eq(i).val(schedule_temp[i]);
        }
        schedule = schedule_temp;
        log('Schedule loaded.');
    }
    else {
       log('Loading schedule failed.');
    }
}

    
// get selected values (an array) and send them to the MQTT server as a single string
function saveSchedule(){

    // get schedule values
    var schedule_temp = $('select').map(function(){
                            return this.value;
                        }).get();
                
    if (validateSchedule(schedule_temp) && MQTTTopics['schedule']){
    
        // MQTTPublish accepts a string
        MQTTPublish( MQTTTopics['schedule'], String(schedule_temp) );
        schedule = schedule_temp;
	document.getElementById('status').innerHTML = 'Schedule saved.'
        log('Schedule saved');
    } 
    else {
       log('Saving schedule failed.');
    }
}


function onConnected(){
    // subscribe to the topic
    MQTTSubscribe( MQTTTopics['schedule'] );
}


function onMessage(topic, message){

    if ( topic == MQTTTopics['schedule'] ){
        // MQTTData contains schedule data in one string
        var schedule_temp = [];
	if(message.trim() != ''){
    		schedule_temp = message.split(',');
	}
        if ( !(schedule_temp.compare(schedule)) ){
            log('new schedule:' + schedule_temp)
            log('old schedule:' + schedule)    
	    // loadschedule requires an array of strings
            loadSchedule( schedule_temp );
        }
    }
}


//TODO combine from iothermostat.js
// when page finished loading:
$(document).ready(function(){

    // connect to broker, tell it to call 
    // onConnected() when connecting succeeded
    // onMessage() when message received
    var credentials = MQTTgetCredentials();
    var user = credentials.user;
    var password = credentials.password;
    MQTTSetup(host,port,useSSL,user,password, onConnected, onMessage); 
    MQTTConnect();
});
