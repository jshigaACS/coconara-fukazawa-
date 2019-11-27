//globalForAjax
file_data;

function connect_ajax(data){
    var a = data;

}

function handleFileSelect(evt) {
    var file = evt.target.files[0];

    var reader = new FileReader();

    reader.onerror = function(){
     alert('ファイルの読み込みに失敗しました');
    }

    reader.onload = function(){
        var csv = reader.result.replace(/\r?\n/g, "");
        var csvArray = csv.split(',');
        if (csvArray.length <= 5000){

            //ajax
            file_data = csvArray;

        }else{
            alert('5000件以下にしてください');
        }

    }
    reader.readAsText(file);

}

$(document).ready(function () {
    var file_up = document.getElementById('upc_file_up');
    //console.log('aaaa')
    //console.log(file_up)
    var res = [];
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        // Great success! All the File APIs are supported.

        file_up.addEventListener('change', function (evt) {

            handleFileSelect(evt);

        }, false);


    } else {
        alert('The File APIs are not fully supported in this browser.');
    }

});

