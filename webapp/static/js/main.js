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
    processData(requestData);
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
        contentType:"application/json; charset=utf-8",
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