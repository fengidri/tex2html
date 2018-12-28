$.get("/store", function(data)
    {
        var file;
        for (i in data)
        {
            file = data[i];
            var a = $('<a>').attr("href", "/markdown.html?f=store/" + file.name).text(file.name)
            console.log(a)
            $('ul').append($('<li>').append(a))

        }

    })
