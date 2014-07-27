jwplayer.key="BSxpAaTPudTB38Uc3YCYtneTFkEHaq90o/XEUw==";
var player = jwplayer("main_video").setup({
    file:  "/media/what_is_love.flv",
    image: "/media/what_is_love_cover.jpg",
    //autostart: true,
    //mute: true,
    repeat: true,
    controls: false,
    width: 640,
    height: 360
});

var colors = [
    'AliceBlue',
    'AntiqueWhite',
    'Aqua',
    'Aquamarine',
    'Azure',
    'Beige',
    'Bisque',
    'Black',
    'BlanchedAlmond',
    'Blue',
    'BlueViolet',
    'Brown',
    'BurlyWood',
    'CadetBlue',
    'Chartreuse',
    'Chocolate',
    'Coral',
    'CornflowerBlue',
    'Cornsilk',
    'Crimson',
    'Cyan',
    'DarkBlue',
    'DarkCyan',
    'DarkGoldenRod',
    'DarkGray',
    'DarkGreen',
    'DarkKhaki',
    'DarkMagenta',
    'DarkOliveGreen',
    'DarkOrange',
    'DarkOrchid',
    'DarkRed',
    'DarkSalmon',
    'DarkSeaGreen',
    'DarkSlateBlue',
    'DarkSlateGray',
    'DarkTurquoise',
    'DarkViolet',
    'DeepPink',
    'DeepSkyBlue',
    'DimGray',
    'DodgerBlue',
    'FireBrick',
    'FloralWhite',
    'ForestGreen',
    'Fuchsia',
    'Gainsboro',
    'GhostWhite',
    'Gold',
    'GoldenRod',
    'Gray',
    'Green',
    'GreenYellow',
    'HoneyDew',
    'HotPink',
    'IndianRed',
    'Indigo',
    'Ivory',
    'Khaki',
    'Lavender',
    'LavenderBlush',
    'LawnGreen',
    'LemonChiffon',
    'LightBlue',
    'LightCoral',
    'LightCyan',
    'LightGoldenRodYellow',
    'LightGray',
    'LightGreen',
    'LightPink',
    'LightSalmon',
    'LightSeaGreen',
    'LightSkyBlue',
    'LightSlateGray',
    'LightSteelBlue',
    'LightYellow',
    'Lime',
    'LimeGreen',
    'Linen',
    'Magenta',
    'Maroon',
    'MediumAquaMarine',
    'MediumBlue',
    'MediumOrchid',
    'MediumPurple',
    'MediumSeaGreen',
    'MediumSlateBlue',
    'MediumSpringGreen',
    'MediumTurquoise',
    'MediumVioletRed',
    'MidnightBlue',
    'MintCream',
    'MistyRose',
    'Moccasin',
    'NavajoWhite',
    'Navy',
    'OldLace',
    'Olive',
    'OliveDrab',
    'Orange',
    'OrangeRed',
    'Orchid',
    'PaleGoldenRod',
    'PaleGreen',
    'PaleTurquoise',
    'PaleVioletRed',
    'PapayaWhip',
    'PeachPuff',
    'Peru',
    'Pink',
    'Plum',
    'PowderBlue',
    'Purple',
    'Red',
    'RosyBrown',
    'RoyalBlue',
    'SaddleBrown',
    'Salmon',
    'SandyBrown',
    'SeaGreen',
    'SeaShell',
    'Sienna',
    'Silver',
    'SkyBlue',
    'SlateBlue',
    'SlateGray',
    'Snow',
    'SpringGreen',
    'SteelBlue',
    'Tan',
    'Teal',
    'Thistle',
    'Tomato',
    'Turquoise',
    'Violet',
    'Wheat',
    'White',
    'WhiteSmoke',
    'Yellow',
    'YellowGreen',
];

window.color_idx = 0;

function notify(message, time) {
    var li = $('<li>');
    $('.notification').prepend(li);
    var el_msg = $('<div>');
    var el_time = $('<div>');
    li.append(el_msg).append(el_time);
    el_msg.html(message);
    el_time.html(time);
    window.color_idx = ~~(Math.random() * colors.length)
    el_msg.css('color', colors[window.color_idx]);
    //window.color_idx++;
}

function im_start() {
    $.get('/start', {}, function (data){
        if (data == 'OK') {
            setTimeout(first_blood, 5000);
        } else {
            setTimeout(im_start, 500);
        }
    });
}

function im_finish() {
    $.get('/finish', {}, function (data){
        if (data == '1') {
            notify('Finished', '');
        } else {
            setTimeout(im_finish, 1000);
        }
    });
}

function first_blood() {
    notify('FIRST BLOOD!', '5 sec');
    setTimeout(double_kill, 5000);
}

function double_kill() {
    notify('DOUBLE KILL!', '10 sec');
    setTimeout(triple_kill, 5000);
}

function triple_kill() {
    notify('TRIPLE KILL!', '15 sec');
    im_finish();
}

$(function(){
    player.play();
    im_start();
});
