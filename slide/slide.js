// H2 处理为章
// H3 处理为一个 slide
//
// 空格翻页
//

var slides; // 用于保存所有的 H3 对象
var Position;
var HEIGHT = document.body.clientHeight;

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

$(document).ready(function()
{
    Slides();
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
            HEIGHT =  window.screen.availHeight;
        }
        else{
            HEIGHT = document.body.clientHeight;
        }
        Slides();
    });

})


function page(p)
{
    var offset = $(document).scrollTop()
    for (var i in slides)
    {
        var node = slides[i];
        var top = node.offset().top;
        if (offset > top - HEIGHT/5 && offset < top + HEIGHT * 4/5)
        {
            gotoslide(i * 1 + 1);
            return;
        }
    }
}

function gotoslide(n)
{
    console.log("Goto Slide:", n);
    node = slides[n];
    if (node == undefined) return;

    $(document).scrollTop(node.offset().top);

    Position.text((n + 1) + "/" + slides.length);
}

function Slides()
{
    var nodes =  $('body > *');
    var heights = [];
    var last_top = undefined;
    var chapter_name = '';
    slides = [];

    //HEIGHT = document.body.clientHeight;
    console.log("HEIGHT: ", HEIGHT);
    $('body > *').each(function()
        {
            node = $(this);
            var nodeName = this.nodeName;
            if ('H2' == nodeName)
            {
                chapter_name = node.text();
                node.hide();
                return;
            }
            if ('H3' == nodeName)
            {
                if (last_top != undefined)
                {
                    heights.push(node.offset().top - last_top);
                }
                last_top = node.offset().top;

                if (node[0]._text == undefined) node[0]._text = node.text();
                node.text(chapter_name + " > " + node[0]._text);
                slides.push(node)
                console.log("Get Slide: ", node.text());
            }
        }
    );

    heights.push(document.body.scrollHeight - last_top);

    makeslide(slides, heights);

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
