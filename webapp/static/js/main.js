function decodeData(){
    article = $("#textArticle").val();
    if(article == ""){
        alert("Empty Article!")
        return
    }
    requestData = {
       "data": {
           "article": article
       },
       "operationType": "decode"
    }
     $.ajax({
        url: "https://104.196.169.174:5000/decode",
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({"input": article}),
        success: function(data){
            $("#textResult").text(data.responseText);
        },
        error: function(data){
            $("#textResult").text(data.responseText);
        }
    });
}

function trainData() {
    requestData = {
       "data": {},
       "operationType": "train"
    }
    processData(requestData);
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
            if (requestData["operationType"] == "decode"){
                $("#textResult").text(data.responseType);
            }else{
                  alert(data.responseType);
            }
        },
        error: function(data){
            alert("Error");
        }
    });
}