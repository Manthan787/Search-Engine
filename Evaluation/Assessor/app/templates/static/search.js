TEXT_LIMIT = 500
GRADES  = [0, 1, 2]
/**
    0 -> non-relevant
    1 -> somewhat-relevant
    2 -> perfectly-relevant
**/

$(document).keypress(function(e) {
    if(e.which == 13) {
        search()
    }
});
function search() {
    $("#results").empty()
    var query = $("#query").val()
    var url = 'search?q='+query
    console.log(url)
    $.ajax({url:url, success: function(result) {
        var list_html;
        var snippets = $("<div class='list-group'>")
        console.log(result.length)
        for (var i = 0; i < result.length; i++)
        {
            list_html = makeSnippet(result[i], query)
            snippets.append(list_html)
        }
        snippets.append("</div>")
        $("#results").html(snippets)
    }});
}

function makeSnippet(result, query) {
    list_item = $("<li class='list-group-item'>")
    var text = ''
    if (result._source.TITLE.length > 0) {
        text = result._source.TITLE
    }
    else {
        text = "NO TITLE FOUND"
    }

    anchor = $("<a></a>").attr("href", result._id)
                         .text(text)
    link = $("<p><i>"+result._id+"</i></p>")
    content = $("<div>").html(highlight(shorten(result._source.TEXT), query))
    grades = $("<select/>").attr("class", "grade").attr("id", result._id)
    for (var j = 0; j < GRADES.length; j++) {
        option = "<option>" + GRADES[j] + "</option>"
        grades.append(option)
    }
    list_item.append(anchor)
    list_item.append(link)
    list_item.append(content)
    list_item.append(grades)
    list_item.append("</li>")
    return list_item
}

function shorten(text) {
    if (text.length > TEXT_LIMIT) {
        return text.substring(0, TEXT_LIMIT) + "..."
    }
    else {
        return text
    }
}

function highlight(text, query) {
    tokens = text.toLowerCase().split(" ")
    keywords = query.toLowerCase().split(" ")
    highlighted_tokens = []
    for (var i = 0; i < tokens.length; i++) {
        token = tokens[i]

        if(keywords.indexOf(token) != -1) {
            token = "<strong>"+token+"</strong>"
        }
        highlighted_tokens[i] = token
    }
    return highlighted_tokens.join(" ")

}

function storeGrades() {
    // Get all the elements with class:grade
    grades = $('*[class*=grade]:visible')
    var data = []
    queryID = $('#queryID').val()
    console.log(data[0])
    var grades_data = []
    for (var i = 0; i < grades.length; i++) {
        grades_data[i] = {'url': grades[i].id, 'grade': grades[i].value}
    }
    data = {'queryID': queryID, 'grades': grades_data}
    console.log(data)
    $.ajax
    ({
        type: "POST",
        url: '/store',
        data: JSON.stringify(data),
        contentType:"application/json; charset=utf-8",
        success: function () {
            console.log("Data stored!")
        }
    })
}
