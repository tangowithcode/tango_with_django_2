

$(document).ready( function() {
    
    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });
    
	$("p").hover( function() {
	    $(this).css('color', 'red');
	}, 
	function() {
	    $(this).css('color', 'black');
	});
    
    $("#about-btn").removeClass('btn-primary').addClass('btn btn-success');
    
	$("#about-btn").click( function(event) {
	    msgstr = $("#msg").html()
	    msgstr = msgstr + "ooo"
	    $("#msg").html(msgstr)
	});
    
  
    
});