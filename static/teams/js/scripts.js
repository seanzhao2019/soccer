// Empty JS for your own code to be here
/*function Createtable()
	{
	with(document)
	{
	write("<table border='1' align='center' class='table table-condensed' >");
	write("<caption><b>查詢到的訊息<b></caption>")
	write("<tr align='center'>");
	{% for i in user_dict %}
	write("<td><b>姓名<b></td>");
//	write("<td>user_id</td>");
	write("<td><b>生日</b></td>");
	write("<td><b>性別</b></td>");
//	write("<td>blood_type</td>");
	write("<td><b>電話</b></td>");
//	write("<td>destination</td>");
	write("<td><b>身體狀況</b></td>");
	write("</tr>");
	{% for i in user_dict %}
	write("<tr align='center'>");
	write("<td>{{i.username}}</td>");
//	write("<td>{{i.user_id}}</td>");
	write("<td>{{i.birthday}}</td>");
	write("<td>{{i.gender}}</td>");
//	write("<td>{{i.blood_type}}</td>");
	write("<td>{{i.emergency_number}}</td>");
//	write("<td>{{i.destination}}</td>");
    if ({{health_info}}==2){
	write("<td class='success'>正常</td>");}
    else if({{health_info}}==0){
    write("<td class='danger'>心率過慢</td>");}
    else{write("<td class='warning'>心率過快</td>");}
	write("</tr>");
	{% endfor %}
	write("</table>")
	}
	}
*/
$(document).ready(function() {
	$("#btn1").click(function() {
		alert("ok")
	 });
 });
function sql_result()
{
	if ("{{query_id}}"==4)
	{
	alert("{{query_id}}");
	document.getElementById("tab_result").innerHTML =Createtable() ;
	}
	if ("{{query_id}}"==3)
	{
		alert("{{query_id}}");
	document.getElementById("result").innerHTML ="成功的完成了"+"{{rows_act}}"+"筆UPDATE操作";
	}
        	if ("{{query_id}}"==2)
        	{
        		alert("{{query_id}}");
	document.getElementById("result").innerHTML ="成功的完成了"+"{{rows_act}}"+"筆DELETE操作";
	}
        	if ("{{query_id}}"==1)
        	{
        		alert("{{query_id}}");
	document.getElementById("result").innerHTML ="成功的完成了"+"{{rows_act}}"+"筆INSERT操作";
	}	
}
/*
    var myLatLng ={lat: 23.8980923, lng: 121.5439799};
var image = '{% static "waypoint/Male_man.png" %}';
var marker;
var map;
function initialize() {
	var mapOptions = {
		zoom: 16,
		center: myLatLng
  	};
 map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
{% for i in lanlon %}
	 marker = new google.maps.Marker({
      position: new google.maps.LatLng{{i}},
      map: map,
	//animation: google.maps.Animation.DROP,
      icon: image
  });
{% for j in heart_rate %}
var contentString = '<div id="content" >'+
      '<div id="siteNotice" class="modal-header">'+
      '<h4 id="firstHeading" class="firstHeading">個人狀況與位置訊息</h4>'+
      '</div>'+
      '<div id="bodyContent" class="modal-body">'+
      '<p><b>心跳</b>:{{j}}<br>'+
      '<b>位置</b>:{{i}}<br></p>'
      '</div>'+
      '</div>';
{% endfor %}
var infowindow = new google.maps.InfoWindow({
      content: contentString
  });
  marker.addListener('click',function() {  //google.maps.event.
    infowindow.open(map,marker);
  });
{% endfor %}
}
function toggleBounce() {
  if (marker.getAnimation() != null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
  }
}
//google.maps.event.addDomListener(window, 'load', initialize);
$(document).ready(function(){
  $("#bt3").click(function(){
{% for i in all_lanlon %}
    marker = new google.maps.Marker({
      position: new google.maps.LatLng{{i}},
      map: map,
	//animation: google.maps.Animation.DROP,
      icon: image
  });
{% for j in all_heart_rate %}
var contentString = '<div id="content" >'+
      '<div id="siteNotice" class="modal-header">'+
      '<h4 id="firstHeading" class="firstHeading">個人狀況與位置訊息</h4>'+
      '</div>'+
      '<div id="bodyContent" class="modal-body">'+
      '<p><b>心跳</b>:{{j}}<br>'+
      '<b>位置</b>:{{i}}<br></p>'
      '</div>'+
      '</div>';
//alert(contentString);
var infowindow = new google.maps.InfoWindow({
      content: contentString
  });
  google.maps.event.addListener(marker, 'click',function() {
    infowindow.open(map,marker);
  });
{% endfor %}
{% endfor %}
});
$("#bt3").click(function(){
document.getElementById("userinfo1").innerHTML =
	"<table border='1' align='center' class='table table-condensed' >"+
	"<caption><b>所有登山者訊息<b></caption>"+
	"<tr align='center'>"+
	"<td><b>姓名<b></td>"+
//	write("<td>user_id</td>");
	"<td><b>生日</b></td>"+
	"<td><b>性別</b></td>"+
//	write("<td>blood_type</td>");
	"<td><b>電話</b></td>"+
//	write("<td>destination</td>");
//	"<td><b>身體狀況</b></td>"+
	"</tr>"+
	"{% for i in user_all %}"+
	"<tr align='center'>"+
	"<td>{{i.username}}</td>"+
//	write("<td>{{i.user_id}}</td>");
	"<td>{{i.birthday}}</td>"+
	"<td>{{i.gender}}</td>"+
//	write("<td>{{i.blood_type}}</td>");
	"<td>{{i.emergency_number}}</td>"+
//	write("<td>{{i.destination}}</td>");
//"<td>{{i.pk}}</td>"+    
 // "{% for j in all_health_info %}"+   
 //   "if (j==2){"+
//	"<td class='danger'>正常</td>"+
 //   "}"+
//    "else if(j==0){"+
//    "<td class='success'>心率過慢</td>"+
 //   "}"+
//    "else{"+
//    "<td class='warning'>心率過快</td>"+
//    "}"+
	"</tr>"+
"{% endfor %}"+
//	"{% endfor %}"+
	"</table>"
	
});
$("#bt2").click(function(){
var ctaLayer = new google.maps.KmlLayer({
//    url:'http://140.116.164.154:8000/static/waypoint/doc1.kml'
//url:'http://140.116.164.154:8000/static/waypoint/doc2.kml'
url:'http://140.116.164.154:8000/static/waypoint/doc4.kml'
  });
  ctaLayer.setMap(map);
});
setInterval(function(){
$.get("/test",function(data){
if (data==1)
{
    $( "#dialog1" ).dialog({
    modal: true,
    show: { effect: "shake", duration: 300 },
    buttons: {
        Ok: function() {
            location.replace("http://140.116.164.154:8000/waypoint/views.py?username=Steven&user_id=Q12345678");       
            //$( this ).dialog( "close" );
        }
      }   
    });
}
else if (data==2)
{
    $( "#dialog2" ).dialog({
    modal: true,
    show: { effect: "shake", duration: 300 },
    buttons: {
        Ok: function() {
            location.replace("http://140.116.164.154:8000/waypoint/views.py?username=Steven&user_id=Q12345678");
            //$( this ).dialog( "close" );
        }
      }   
    });
}
else if (data==3)
{
    $( "#dialog3" ).dialog({
    modal: true,
    show: { effect: "shake", duration: 300 },
    buttons: {
        Ok: function() {
            location.replace("http://140.116.164.154:8000/waypoint/views.py?username=Steven&user_id=Q12345678");
            //$( this ).dialog( "close" );
        }
      }   
    });
}
})
},10000);
});
