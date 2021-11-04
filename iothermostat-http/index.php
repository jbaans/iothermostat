<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <link rel="stylesheet" type="text/css" href="css/stylesheet.css"/>
    <title>IOThermostat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<script src="scripts/jquery-min-3.2.1.js" type="text/javascript"></script>
	<script src="scripts/mqttws31.js" type="text/javascript"></script>
	<script src="scripts/mqttclient.js" type="text/javascript"></script>
	<script src="scripts/mqttconf.js" type="text/javascript"></script>
	<script src="scripts/iothermostat.js" type="text/javascript"></script>
  </head>
<body bgcolor="#1602f4" text="#FFFFFF" link="#FFFFFF" vlink="#FFFFFF" class="nocursor">
<div class="divTable blueTable">
    <div class="divTableBody">
        <div class="divTableRow-s">
            <div class="divTableCell">
                <span class="left-aligned"><img id="flame" src="img/flame_lightblue.png" width="25" height="25" alt=""/></span>
            </div>
            <div class="divTableCell"></div>
            <div class="divTableCell">
                <span onclick="gotoAdvanced(); return false;" id="button-menu" class="right-aligned button">
                    <span id='ibox'>i</span>
                </span>
            </div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell centered"><span id="targettemperature">20.0</span> &deg;</div>
            <div class="divTableCell">
                <img class="icon" src="img/indoor_lightblue.png" alt=""/>
            </div>
            <div class="divTableCell">
                <span id="temperature">20.0</span> &deg;
                <img class="arrow" id="d_temperature" src="img/up_lightblue.png" alt=""/>
            </div>
        </div>
        <div class="divTableRow">
            <div class="divTableCell">
                <input type="button" onclick="decrTemperature(); return false;" id="button-minus" class="button button-plusminus" value="-"/>
                <input type="button" onclick="incrTemperature(); return false;" id="button-plus" class="button button-plusminus" value="+"/>
            </div>
            <div class="divTableCell">
                <img class="icon" src="img/cloud_lightblue.png" alt=""/>
            </div>
            <div class="divTableCell">
                <span id="pressure">100</span>
                <span class="units">hPa</span>
                <img class="arrow" id="d_pressure" src="img/up_lightblue.png" alt=""/>
            </div>
        </div>
        <div class="divTableRow">
	    <div class="divTableCell">
                <input type="button" onclick="rotateMode(); return false;" id="mode" class="button" value="Auto"/>
            </div>
            <div class="divTableCell">
                <img class="icon" src="img/drop_lightblue.png" alt=""/>
            </div>
            <div class="divTableCell">
                <span id="humidity">40</span>
                <span class="units">%</span>
                <img class="arrow" id="d_humidity" src="img/up_lightblue.png" alt=""/>
            </div>
        </div>
    </div>   
</div>
</body>
</html>
