var player_options = {
    file:  "/media/what_is_love.flv",
    image: "/media/what_is_love_cover.jpg",
    //autostart: true,
    //mute: true,
    repeat: true,
    controls: false,
    width: 640,
    height: 360
};

var total_secs = 36000;

var start_time = 0;

function im_start() {
    $.get('/start', {}, function (data){
        if (data == 'OK') {
            $('.video, .messages, .stats').show();
            $('.landing').hide();
            animate_by_time('.messages');
            jwplayer.key="BSxpAaTPudTB38Uc3YCYtneTFkEHaq90o/XEUw==";
            var player;
            player = jwplayer("main_video").setup(player_options);
            player.play();
            setTimeout(im_finish, total_secs * 1000);
            start_time = +new Date;
        } else {
            setTimeout(im_start, 500);
        }
    });
}

function im_finish() {
    $.get('/finish', {}, function (data){
        if (data == '1') {
            $('.messages .complete').show();
        } else {
            setTimeout(im_finish, 1000);
        }
    });
}

function animate_by_time(container){
    var css_before = {
        'font-size': '0.1em',
        'opacity': .01
    }
    var css_after = {
        'font-size': '1em',
        'opacity': 1
    }
    $(container + ' [data-animate]').each(function(idx, el){
        var $el = $(el);
        var data = $el.attr('data-animate').split(';');
        var animate_at = parseFloat(data[0]) * 1000;
        var animate_duration = parseFloat(data[1]) * 1000;
        var hide_at = parseFloat(data[2]) * 1000;
        var hide_fn = function(){ $el.hide(); }
        var animate_fn = function(){
            $el.show()
                .css(css_before)
                .animate(css_after, animate_duration);
        };
        $el.hide();
        setTimeout(animate_fn, animate_at);
        if (hide_at) setTimeout(hide_fn, hide_at);
    });
}

var update_timer_locked = false;
function update_timer(){
    if (update_timer_locked) return;
    if (start_time == 0) return;

    update_timer_locked = true;

    // Statistics: seconds elapsed
    var millis_passed = +new Date - start_time;
    seconds = millis_passed / 1000;
    $('.stat_timer .spent').html(seconds.toFixed(2));

    // Statistics: percent completion
    var percent = (seconds * 100 / total_secs).toFixed(2) + '%';
    $('.stat_progress .percent').html(percent);
    $('.stat_progress .bar').css('width', percent);

    // Switch statistics
    var stats = $('.stats.pull-left').children();
    var show_idx = Math.round(millis_passed / 8000) % stats.length;
    var cur_stat = stats.eq(show_idx);
    stats.not(cur_stat).hide();
    if (cur_stat.is(':hidden')) {
        cur_stat.show().css('opacity', 0).animate({'opacity': 1}, 400);
    }

    update_timer_locked = false;
}

$(function(){
    animate_by_time('.landing');
    setInterval(update_timer, 50);
});
