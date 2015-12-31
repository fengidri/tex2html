// H2 处理为章
// H3 处理为一个 slide
//
// 空格翻页
//
//
//
//
var slides = []; // 用于保存所有的 H3 对象

$(document).ready(function()
{
    set_pos();
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
})


function page(p)
{
    var offset = $(document).scrollTop()
    var win_height = $(window).height()
    for (var i in slides)
    {
        var node = slides[i];
        var top = node.offset().top;
        if (offset > top - win_height/5 && offset < top + win_height * 4/5)
        {
            i = 1 * i;
            console.log("Goto Slide:", i+1);
            node = slides[i + 1];
            if (node == undefined) return;
            $(document).scrollTop(node.offset().top);
            return;
        }
    }
}

function set_pos()
{
    var nodes =  $('body > *');
    var heights = [];
    var last_top = undefined;
    var chapter_name = '';
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
                node.text(chapter_name + " > " + node.text());
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
    var total_height = $(window).height();//document.body.clientHeight;
    for (var i in slides)
    {
        var node = slides[i];
        var height = heights[i];
        var space = total_height - height;
        console.log("makeslide :", node.text());
        console.log("makeslide space:", space);
        node.before(make_space(heade_pre));
        node.after(make_space(space * 0.3));
        heade_pre = space * 0.7;
    }
    $('body').append(make_space(heade_pre));
}

function make_space(h)
{
    var space = $('<div>')
    space.css('margin', 0);
    space.css('padding', 0);
    space.css('border', 'None');
    space.css('height', h);
    return space;
}
