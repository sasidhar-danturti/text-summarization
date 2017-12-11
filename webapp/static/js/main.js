$(document).ready(function() {
    $("#textArticle").on("input", function() {
        limit = 200
        text = this.value
        words = 0
        if (text !== ""){
            words = text.match(/\S+/g).length;
        }
        if (words > limit) {
            // Split the string on first 200 words and rejoin on spaces
            var trimmed = $(this).val().split(/\s+/, limit).join(" ");
            // Add a space at the end to keep new typing making new words
            $(this).val(trimmed + " ");
            wrapWordCount(1, limit, limit);
        }
        else {
             wrapWordCount(1, limit, words);
        }
    });

    $("#textSumm").on("keyup", function() {
        limit = 30
        text = this.value
        words = 0
        if (text !== ""){
            words = text.match(/\S+/g).length;
        }
        if (words > limit) {
            // Split the string on first 30 words and rejoin on spaces
            var trimmed = $(this).val().split(/\s+/, limit).join(" ");
            // Add a space at the end to keep new typing making new words
            $(this).val(trimmed + " ");
            wrapWordCount(2, limit, limit);
        }
        else {
             wrapWordCount(2, limit, words);
        }
    });
 });

 function wrapWordCount(id, limit, count){
    $("#displayCount"+id).text(count);
    $("#wordLeft"+id).text(limit-count);
 }

function decodeData(){
    $("#textResult").val("");
    article = $("#textArticle").val();
    if(article == ""){
        alert("Empty Article!")
        return
    }
     $.ajax({
        url: "https://35.227.22.13:5000/decode",
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({"input": article}),
        async: false,
        success: function(data){
            $("#textResult").val(data.responseText);
        },
        error: function(data){
            alert("Error");
        }
    });
}

function getUUID(){
    return new Date().valueOf();
}

function trainData() {
    var checkedValues = $("li input[type=checkbox]:checked").map(function () {
        return $(this).val();
    });

    job_id = "JobID_" + getUUID();
    $.ajax({
        url: "https://35.227.22.13:5000/train",
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "input": job_id,
            "files_to_exclude": checkedValues.get()
        }),
        success: function(data){
            alert(data.responseText);
        },
        error: function(data){
            alert("Error");
        }
    });
}

function saveData() {
    article = $("#textArticle").val();
    if(article == ""){
        alert("Empty Article!")
        return
    }
    summary = $("#textSumm").val();
    if(summary == ""){
        alert("Empty Summary!")
        return
    }
    var title = $("#textFileName").val();
    if(title == ""){
        alert("Empty title!")
        return
    }
    title = title.replace(/\s+/g, '_')
    file_name = title + '_' + getUUID();
    requestData = {
        "data": {
           "article": article,
           "summary": summary,
           "file_name": file_name,
           "tag_name": "data"
        },
        "operation_type": "save"
    }
    $.ajax({
        url: "/save-article",
        type: "POST",
        contentType:"application/json",
        dataType: "json",
        data: JSON.stringify(requestData),
        success: function(data){
            alert(data.responseType);
        },
        error: function(data){
            alert("Error");
        }
    });
}

function clearText(){
    $("#textArticle").val("");
    $("#textResult").val("");
    $("#textSumm").val("");
    $("#textFileName").val("");
}

function showArticle(){
    clearText();
    $("#boxArticle").show();
    $(".text-center").show();
    $( "#trainNav" ).bind("click", renderFileList);
}

function renderFileList(){
   clearText();
   $("#boxArticle").hide();
   $(".text-center").hide();
   $.ajax({
        url: "/files",
        type: "GET",
        success: function(data){
            var files = data.file_list.data;
            $("#fileListDisplay").append(renderList(files));
        },
        error: function(data){
            alert("Error");
        }
    });
}

function renderList(files){
    if ($("#fileList").parent().length){
        $("#fileList").remove();
    }
    var newUl = $('<ul id="fileList" style="list-style-type: none;">');

    $.each(files, function(index, file_name){
        var newLi = $("<li class='list-group-item list-group-item-default'/>");
        newLi.append(
            '<div class="btn-group" data-toggle="buttons">' +
            '<label class="btn btn-info">' +
			'<input type="checkbox" autocomplete="off" value='+
			file_name +'>' + '<i class="fa fa-check" aria-hidden="true"></i>' +
			'</label>' + '<span class="text-list">'+ file_name +'</span>' +
			'</div>'
        );
        newUl.append(newLi);
    })
    return newUl;
}
