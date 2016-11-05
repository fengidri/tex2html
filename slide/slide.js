// H2 处理为章
// H3 处理为一个 slide
//
// 空格翻页
//

var SLIDES = []; // 用于保存所有的 H3 对象
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

function slice_bottom(n)
{
    var pos = $('<div>')
    pos.css('margin', 0);
    pos.css('padding', 0);
    pos.css('border', 'None');
    pos.css('display', 'inline-block');
    pos.css('position', 'absolute');
    pos.css('bottom', 12);
    pos.css('right', 12);
    pos.css('cursor', 'pointer');
    $('body').append(pos);

    //var full = $('<div id=Full>').text("Full");
    //full.css('margin', 0);
    //full.css('padding', 0);
    //full.css('border', '1px');
    //full.css('display', 'inline-block');
    //full.css('position', 'fixed');
    //full.css('bottom', 42);
    //full.css('right', 12);
    //full.css('cursor', 'pointer');
    //$('body').append(full);

    pos.click(function(){
        // 启动全屏!
        launchFullScreen(document.documentElement); // 整个网页
    //    full.hide();
        //launchFullScreen(document.getElementById("videoElement")); // 某个页面元素
    });
    pos.text(n)

    return pos;

}

function page(p)
{
    var offset = $(document).scrollTop()
    var n = offset / document.body.clientHeight;
    n = Math.floor(n)
    n = n + p;
    gotoslide(n);
    localStorage.setItem("current_page_num", n );
}

function gotoslide(n)
{
    console.log("Goto Slide:", n, t);
    n = n * 1;

    var t = SLIDES[n];
    if (!t) return;

    $(document).scrollTop($(t).offset().top);

}

function mkbox(vector, height)
{
    //-----------------
    // header
    //-----------------
    // content
    //
    //-----------------
    // bottom
    //-----------------
    var box = $('<div>');
    vector.append(box);

    if (height)
    {
        box.css('height', height);
        box.css('width', height);
    }

    box.css('position', "relative");
    box.css('padding', "0");
    box.css('margin-top', "0");
    box.css('margin-bottom', "0");

    var header = $('<div>');
    var content = $('<div>');
    var bottom = $('<div>');

    content.css('width', '100%');

    bottom.css('margin', 0);
    bottom.css('padding', 0);
    bottom.css('border', 'None');
    //bottom.css('display', 'inline-block');
    bottom.css('position', 'absolute');
    bottom.css('bottom', 10);
    bottom.css('text-align', "right");
    bottom.css('width', '100%');
    //bottom.css('right', 12);
    //bottom.css('cursor', 'pointer');

    box.append(header);
    box.append(content);
    box.append(bottom);

    return [box, header, content, bottom];
}

function Slides(objs)
{
    var chapter_name = '';

    if (!HEIGHT)
        HEIGHT = document.body.clientHeight;
    console.log("HEIGHT: ", HEIGHT);

    var slice_number = 0;
    var content, box;

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
                slice_number += 1;
                box = mkbox($('body'), document.body.clientHeight);

                if (chapter_name.length > 0)
                {
                    node.text(chapter_name + '-' + node.text())
                }

                box[1].append(node);
                box[3].append(slice_number);
                content = box[2];
                box[0].attr('class', 'slide')
                content.attr('class', "content")

                SLIDES.push(box[0][0]);
                return;
            }
            if ('H4' == nodeName)
            {
                content[0]._no_resize = 1;
            }

            if (content) content.append(node);
        }
    );

    adjust_content();

    //scale($("div.slide_content"));
    prettyPrint();
}



function slide_resize(obj)
{
    //var obj = obj.find('div');

}

function slide_all_resize()
{
    console.log("resize")
    HEIGHT = document.body.clientHeight;
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

function adjust_content()
{
    var H = document.body.clientHeight;
    $(".content").each(function(){
        if (this._no_resize) return;
        var obj = $(this);

        obj.css("transform", "None");
        obj.css("transform-origin", "0% 0%");

        if (obj.height() > H * 0.8)
        {
            return;
        }

        obj.css("transform", "translateY(" +  (H - obj.height())* 2/5 + "px)");
    });
}

function slide_show()
{
    Slides($("#slide_orgin >  *"));
    $("img").load(adjust_content);
    //AddTools();

    var n = localStorage.getItem("current_page_num")
    if (!n)
        n = 0
    gotoslide(n);

    $('body').keypress(function(event){
        event.preventDefault();
        console.log(event.keyCode)
        if (32 == event.keyCode) // space
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
//    $(window).resize(slide_all_resize);

    //FullEvent(function () {
    //    if (HEIGHT == document.body.clientHeight)
    //    {
    //        //HEIGHT =  window.screen.availHeight;
    //        HEIGHT =  window.screen.height;
    //    }
    //    else{
    //        HEIGHT = document.body.clientHeight;
    //    }
    //    slide_all_resize();
    //});
    //
}



