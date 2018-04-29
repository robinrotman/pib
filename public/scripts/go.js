$(function(){
    var timer = setInterval(function(){
        $("#count-num").html(function(i,html){
            if(parseInt(html)>1) {
                return parseInt(html)-1;
            }
            else {
                clearTimeout(timer);
                return '<img id="logo" src="images/pib-logo-white.svg">';
            }
        });
    },1000);
});