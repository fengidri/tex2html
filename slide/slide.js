// H2 处理为章
// H3 处理为一个 slide
//
// 空格翻页
//

var SLIDES = []; // 用于保存所有的 H3 对象
var Position;
var HEIGHT;// = document.body.clientHeight;

// 判断各种浏览器，找到正确的方法
function launchFullScreen(element) {
    if(element.requestFullscreen) {
        element.requestFullscreen();
    } else if(element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    } else if(element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen();
    } else if(element.msRequestFullscreen) {
        element.msRequestFullscreen();
    }
}

function FullEvent(fun)
{
    document.addEventListener("fullscreenchange",       fun, false);
    document.addEventListener("mozfullscreenchange",    fun, false);
    document.addEventListener("webkitfullscreenchange", fun, false);
    document.addEventListener("msfullscreenchange",     fun, false);
}

function AddTools()
{
    var pos = $('<div>')
    pos.css('margin', 0);
    pos.css('padding', 0);
    pos.css('border', 'None');
    pos.css('display', 'inline-block');
    pos.css('position', 'fixed');
    pos.css('bottom', 12);
    pos.css('right', 12);
    Position = pos;
    $('body').append(pos);

    var full = $('<div>').text("Full");
    full.css('margin', 0);
    full.css('padding', 0);
    full.css('border', '1px');
    full.css('display', 'inline-block');
    full.css('position', 'fixed');
    full.css('bottom', 42);
    full.css('right', 12);
    full.css('cursor', 'pointer');
    $('body').append(full);

    full.click(function(){
        // 启动全屏!
        launchFullScreen(document.documentElement); // 整个网页
        full.hide();
        //launchFullScreen(document.getElementById("videoElement")); // 某个页面元素
    });

}

function page(p)
{
    var offset = $(document).scrollTop()
    var n = offset / HEIGHT;
    n = Math.floor(n)
    gotoslide(n + 1);
}

function gotoslide(n)
{
    console.log("Goto Slide:", n, t);

    var t = SLIDES[n];
    if (!t) return;

    $(document).scrollTop($(t).offset().top);

    Position.text(n + 1 + "/" + SLIDES.length);
}

function mk_one_slide(text)
{
    var vector = $('body');
    var slide_cur = $('<div class=slide>');

    slide_cur.css('height', HEIGHT);
    slide_cur.css('width', HEIGHT);

    SLIDES.push(slide_cur[0]);

    vector.append(slide_cur);

    var slide_next = $('<div>');
    slide_next.css('width', HEIGHT);

    slide_cur.append($('<H3>').text(text));
    slide_cur.append(slide_next);
    return slide_next;
}

function Slides(objs)
{
    var chapter_name = '';

    if (!HEIGHT)
        HEIGHT = document.body.clientHeight;
    console.log("HEIGHT: ", HEIGHT);

    var slide_cur = undefined;
    var slide_item_nu = 0;

    objs.each(function()
        {
            node = $(this);
            var nodeName = this.nodeName;
            if ('H2' == nodeName)
            {
                chapter_name = node.text();
                return;
            }
            if ('H3' == nodeName)
            {
                if (slide_item_nu > 0) slide_item_nu = 0;
                slide_cur = mk_one_slide(chapter_name + " - " + node.text());
                return;
            }
            slide_item_nu += 1;
            if (slide_cur) slide_cur.append(node);
        }
    );

    scale($("div.slide"));
    prettyPrint();
}

function makeslide(slides, heights)
{
    var heade_pre = 0;
    for (var i in slides)
    {
        var node = slides[i];
        var height = heights[i];
        var space = HEIGHT - height;

        console.log("height:", height, " space:", space, " makeslide :", node.text());

        node.before(make_space(heade_pre));
        node.after(make_space(space * 0.3));
        heade_pre = space * 0.7;
    }
    $('body').append(make_space(heade_pre));
}

function make_space(h)
{
    var space = $('<div id=_space >')
    space.css('margin', 0);
    space.css('padding', 0);
    space.css('border', 'None');
    space.css('height', h);
    return space;
}

function slide_resize(obj)
{
    var sub = obj.find('div');

    sub.css("transform", "None");
    sub.css("transform-origin", "0% 0%");

    if (sub.width() > HEIGHT)
    {
        var hsub = Math.max(sub.height(), sub.width());
    }
    else{
        var hsub = sub.height();
    }

    var hmax = obj.height() - sub.offset().top + obj.offset().top - 20;

    if (hsub > hmax)
    {
        sub.css("transform", "scale(" +  hmax / hsub + ")");
    }
    else if (hsub < hmax * 2 /3 ){
        sub.css("transform", "translateY(" +  (hmax - hsub)* 2/5 + "px)");
    }
}

function slide_all_resize()
{
    $('div.slide').each(function(){
        var obj = $(this);
        var sub = obj.find('div');

        obj.css("height", HEIGHT);
        obj.css("width", HEIGHT);

        sub.css("width", HEIGHT);
        slide_resize(obj);
    });
}

function slide_img_resize()
{
    slide_resize($(this).parents(".slide"));
}

function scale(objs)
{
    objs.each(function(){
        slide_resize($(this));
    });

}

function slide_show()
{
    Slides($("#slide_orgin >  *"));
    $("div.slide img").load(slide_img_resize);
    AddTools();

    gotoslide(0);

    $('body').keypress(function(event){
        event.preventDefault();
        if (32 == event.keyCode)
        {
            page(1);
            //event.returnValue = false;
        }else if (40 == event.keyCode)
        {
            page(1);
        }else if (28 == event.keyCode)
        {
            page(-1);
        }
    });

    FullEvent(function () {
        if (HEIGHT == document.body.clientHeight)
        {
            //HEIGHT =  window.screen.availHeight;
            HEIGHT =  window.screen.height;
        }
        else{
            HEIGHT = document.body.clientHeight;
        }
        slide_all_resize();
    });

}

