/*
* Author: Jan Bonne Aans
* Copyright: Jan Bonne Aans
* License: GPLv3
* Version: 1 Development
* Contact: jbaans > gmail.com
*
* MQTT configuration for IOThermostat
*
**/

var SYSTEMNAME = 'iothermostat0'
var MQTTTopics = { 'temperature':       SYSTEMNAME+'/sensor/temperature',
                   'humidity':          SYSTEMNAME+'/sensor/humidity',
                   'pressure':          SYSTEMNAME+'/sensor/pressure',
                   'd_temperature':     SYSTEMNAME+'/sensor/d_temperature',
                   'd_humidity':        SYSTEMNAME+'/sensor/d_humidity',
                   'd_pressure':        SYSTEMNAME+'/sensor/d_pressure',
                   'mode':              SYSTEMNAME+'/settings/mode',
                   'targettemperature': SYSTEMNAME+'/settings/targettemperature',
                   'schedule':          SYSTEMNAME+'/settings/schedule',
                   'uptime':            SYSTEMNAME+'/state/iothermuptime',
                   'systemuptime':      SYSTEMNAME+'/state/systemuptime',
                   'modeendtime':       SYSTEMNAME+'/state/modeendtime',
                   'py_serverstatus':   SYSTEMNAME+'/state/iothermstatus',
                   'iothermversion':    SYSTEMNAME+'/state/iothermversion',
                   'heateron':          SYSTEMNAME+'/state/heateron'
                                    };

// default secure settings
var useSSL = true;
var port = 9001;

// if on http (i.e. LAN) use insecure settings
if ( location.protocol == 'http:' ) {
    console.log('WARNING: mqttconf.js: Not using SSL for MQTT!');
    useSSL = false;
    port = 9002;
}


function MQTTgetCredentials(){
    return JSON.parse( 
              $.ajax({
                url: 'store.php',
                dataType: 'text',
                cache: false,
                contentType: false,
                processData: false,
                type: 'post',
                async: false,
              }).responseText
           );
}

var host = window.location.hostname;

// generate topic and data objects
var MQTTData = {};
var MQTTShorttopics = {};
for(var shorttopic in MQTTTopics){
    MQTTShorttopics[ MQTTTopics[shorttopic] ] = shorttopic;
    MQTTData[ MQTTTopics[shorttopic] ] = '';
}
