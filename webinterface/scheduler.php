<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
  <link rel="icon" href="data:;base64,iVBORw0KGgo=">
  <link rel="stylesheet" type="text/css" href="css/scheduler.css"/>
  <title>IOThermostat - Scheduler</title>
  <script src="scripts/jquery-min-3.2.1.js" type="text/javascript"></script>	
  <script src="scripts/mqttws31.js" type="text/javascript"></script>
  <script src="scripts/mqttclient.js" type="text/javascript"></script>
  <script src="scripts/mqttconf.js" type="text/javascript"></script>
  <script src="scripts/scheduleUI.js" type="text/javascript"></script>  
</head>

<body bgcolor="#1602f4" text="#FFFFFF" link="#FFFFFF" vlink="#FFFFFF" class="nocursor">
<table id='scheduletable'>
  <tr>
    <td>Day</td><td>From</td><td></td><td>To</td><td></td><td>Set temperature &emsp;</td>
    <td>
      <input type="button" id='masteraddbutton' class="button-css-s" value="+" onclick="addRow(this)"/>
    </td>
  </tr>
</table>
<p>
  <input type="button" class='button-css' onclick="saveSchedule()" value="Save"/>
</p>
<p id="status"></p>
</body>

</html>
