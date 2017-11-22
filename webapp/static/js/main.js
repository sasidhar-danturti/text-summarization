function decodeData(){
    article = $("#boxText").val();
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
    article = $("#boxText").val();
    if(article == ""){
        alert("Empty Article!")
        return
    }
    summary = $("#boxSumm").val();
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
            $("#boxResultText").text(data.responseType)
        },
        error: function(data){
            alert("Error");
        }
    });
}