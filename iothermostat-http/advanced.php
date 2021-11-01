<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <link rel="stylesheet" type="text/css" href="css/stylesheet.css"/>
    <title>IOThermostat - Advanced</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <?php $today = getdate();?>
	<script src="scripts/jquery-min-3.2.1.js" type="text/javascript"></script>
	<script src="scripts/mqttws31.js" type="text/javascript"></script>
	<script src="scripts/mqttclient.js" type="text/javascript"></script>
        <script src="scripts/mqttconf.js" type="text/javascript"></script>
	<script src="scripts/iothermostat.js" type="text/javascript"></script>
<script>
    var d = new Date(Date.UTC(<?php echo $today['year'].",".$today['mon'].",".$today['mday'].",".$today['hours'].",".$today['minutes'].",".$today['seconds']; ?>));
    d.setHours(d.getHours() + d.getTimezoneOffset()/60 );
    setInterval(function() {
        d.setSeconds(d.getSeconds() + 1);
        hours = d.getHours()
        if ( hours < 10 ){
                hours = '0' + hours;
        }
	minutes = d.getMinutes()
	if ( minutes < 10 ){
		minutes = '0' + minutes;
	}
        seconds = d.getSeconds()
        if ( seconds < 10 ){
                seconds = '0' + seconds;
        }
        $('#timer').text((hours + ':' + minutes + ':' + seconds ));
    }, 1000);
</script> 
  </head>
<body bgcolor="#1602f4" text="#FFFFFF" link="#FFFFFF" vlink="#FFFFFF" class="nocursor">
<div class="divTable blueTable">
    <div class="divTableBody">
        <div class="divTableRow-s">
            <div class="divTableCell">
                <span class="left"><img id="flame" src="img/flame_lightblue.png" width="25" height="25" alt=""/></span>
            </div>
            <div class="divTableCell"></div>
            <div class="divTableCell" id="buttoncell">
                <span onclick="refresh(); return false;" id="button-menu" class="right-aligned button">
                    <img src="img/home_lightblue.png" style="height:27px; width:27px;"/>
                </span>
            </div>
        </div>
        <br/>
        <div class="divTableRow">
            <table style="display:inline; white-space:nowrap">
                <tr><td>IOThermostat v.:</td><td><span id="iothermversion">Waiting for update...</span></td></tr>
                <tr><td>Operating system:</td><td><?php echo php_uname("s");?> <?php echo php_uname("m");?><br><?php echo php_uname("r");?></td></tr>
                <tr><td>System time:</td><td><?php echo date('d/m/Y');?> <label id="timer"></label> </td></tr>
                <tr><td>Backend status:</td><td><span id="py_serverstatus">Waiting for update...</span></td></tr>
                <tr><td>Backend uptime:</td><td><span id="uptime">Waiting for update...</span> <span>days</span></td></tr>
                <tr><td>System uptime:</td><td><span id="systemuptime">Waiting for update...</span> <span>days</span></td></tr>
                <tr><td>Server IP:</td><td><?php include 'getip.php' ?></td></tr>
            </table>
        </div>

    </div>   
</div>
</body>
<script>
$(document).ready(function(){
    // show scheduler button if client is not on touch screen device itself
    if (!(location.hostname === "localhost" || location.hostname === "127.0.0.1")){
        div = document.getElementById("buttoncell");

        var myimg = document.createElement('img');
        myimg.src = "img/schedule_lightblue.png";
        myimg.style= "height:27px; width:27px;";

        var myspan = document.createElement('span');
        myspan.addEventListener("click", function(){location.href="scheduler.php"; return false;});
        myspan.id="button-schedule";
        myspan.className="right-aligned button";

        myspan.appendChild(myimg);
        div.appendChild(myspan);
    }
});
</script>
</html>
