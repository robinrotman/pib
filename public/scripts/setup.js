game_id = null
token = null

$('input').focusout('click', function(e) {
    if ( ($(this)[0].validity.valid == true) && ($(this)[0].value.length > 1) && ($(this)[0].type == "email") ) {
        $(this).addClass('checked')
    }
    else if (($(this)[0].validity.valid == true) && ($(this)[0].value > 0) && ($(this)[0].type == "number") && ($(this)[0].className == "max-score") ) {
        $(this).addClass('checked');
    }
});

$('input').focusin('click', function() {
    $(this).removeClass('checked');
});

function sendToken() {
    token = $('#digit-1').val() + $('#digit-2').val() + $('#digit-3').val() + $('#digit-4').val()

    $.ajax({
        url: 'https://1bj8u6759k.execute-api.us-east-2.amazonaws.com/production/token/' + token,
        headers: {'Content-Type': 'application/json'},
        type: "GET",
        dataType: "json",
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("BOOO")
            errorAlert();
        },
        success: function(data, textStatus, jqXHR) {
            console.log("WOOO")
            console.log(data)
            game_id = data['game_id']
            $('#setup-step-1').toggleClass('hidden shown');
            $('.step-1-submit').toggleClass('hidden shown');
            $('#setup-step-2').toggleClass('hidden shown');
            $('.step-2-submit').toggleClass('hidden shown');
        }
    });
}

function errorAlert() {
    $('html').prepend('<div class="error"> Something is miscompibulated! If you think you pibbed up, fix it or just try again.</div>');
    setTimeout(function() {
        $('.error').addClass('fade-out');
    }, 3000);
    setTimeout(function(){
        $('.error').remove();
    }, 4000);
}

function startGame() {
    $.ajax({
        url: 'https://1bj8u6759k.execute-api.us-east-2.amazonaws.com/production/game',
        headers: {'Content-Type': 'application/json'},
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            token: token,
            player1: $('.email-user-1').val(),
            player2: $('.email-user-2').val(),
            play_to_score: $('.max-score').val()
        }),
        error: function(jqXHR, textStatus, errorThrown) {
            errorAlert();
        },
        success: function(data, textStatus, jqXHR) {
            window.location.href = 'go.html'
        }
    });
}

function autotabTokenInput(current, to) {
    if (current.getAttribute && current.value.length == 1) {
        to.focus()
    }
}