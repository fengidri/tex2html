var LAST_MD = "";

function strcmp(s1, s2)
{
    for (var i = 0; i < s1.length; ++i)
    {
        var c2 = s2.substr(i, 1);
        if (c2 == "") return i;

        var c1 = s1.substr(i, 1);
        if (c1 != c2)
            return i;

    }
    return -1;
}



function onclick_add( ){
    var Y =this.target.offset().top;
    $(document).scrollTop(Y);
}


function index_init(index, list, toggle)
{
    headers = list.find('h1, h2, h3, h4, h5, h6');

    index.html('');
    index.append($('<h3>').text('目录'));
    h2=h3=h4=h5=h6=0;
    nu='';
    headers.each(function(){
        header=$(this);
        switch(header[0].nodeName){
                case 'H2':
                    h2 = h2 + 1;
                    h3=0;
                    id_div='h2';
                    nu= h2 + '. ';
                    break;
                case 'H3':
                    h4=0;
                    h3 = h3 + 1;
                    nu= h2 + '. ' + h3 + '. ';
                    id_div='h3';
                    break;
                case 'H4':
                    id_div='h4';
                    h5=0;
                    h4 = h4 + 1;
                    nu= h2 + '. ' + h3 + '. ' + h4 + '. ';
                    break;
                case 'H5':
                    id_div='h5';
                    h5 = h5 + 1;
                    h6=0;
                    nu= h2 + '. ' + h3 + '. ' + h4 + '. ' + h5 + '. ';
                    break;
                case 'H6':
                    id_div='h6';
                    break;
            }
            var new_obj=$('<div id="' + id_div + '">'+ nu +  header.html() + '</div>' );
            new_obj.click(onclick_add);

            //为这个元素增加一个target属性指向其对应的标题,目的是为了可以通过个
            //属性直接得到对应的标题的信息, 如标题的位置
            //注意这个不能设置为jquery的属性, 因为jquery的属性的生命周期的长度不
            //足
            new_obj[ 0 ].target = header;
            index.append( new_obj );
        });
    if (toggle)
    {
        toggle.click(function(){
            index.toggle();
        })
    }
}


function loadmd()
{
    $.get("../workdoc/work-summary-2016.md", function(data, status){
        //if (status != 200)
        //{
        //    alert("recv status " + status);
        //    return;
        //}
        var pos = strcmp(data, LAST_MD);
        if (-1 == pos) return;
        LAST_MD = data;

        data = data.substr(0, pos) + "<span id=_m></span>" + data.substr(pos);

        $("#content").html(marked(data));

        $("body").animate({scrollTop:$("#_m").offset().top - 100},1000);

        index_init($("#index"), $("#content"));
    })
}

loadmd();
setInterval(loadmd, 500);