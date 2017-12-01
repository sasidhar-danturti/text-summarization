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
        url: "https://104.196.169.174:5000/decode",
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

function trainData() {
    job_id = "JobID_" + new Date().valueOf();
    $.ajax({
        url: "https://104.196.169.174:5000/train",
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({"input": job_id}),
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
    requestData = {
        "data": {
           "article": article,
           "summary": summary
        },
        "operationType": "save"
    }
    processData(requestData);
}


function processData(requestData){
    $.ajax({
        url: "/process-article",
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
}