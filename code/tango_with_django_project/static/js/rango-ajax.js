
$(document).ready( function() {

$('#likes').click(function(event){
    
    var catid;
    catid = $(this).attr("data-catid");
    alert("cat" + catid + " clicked");
    $.get('/rango/like/', {category_id: catid}, function(data){
        $('#like_count').html(data);
            $('#likes').hide();
    });
   
});


});