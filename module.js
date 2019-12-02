//global ForAjax
var file_data;
var file_name;//handleFileSelectの際にファイルnameを取得する
var res_data;

//拡張子を消す
function baseName(str)
{
   var base = new String(str).substring(str.lastIndexOf('/') + 1); 
    if(base.lastIndexOf(".") != -1)       
        base = base.substring(0, base.lastIndexOf("."));
   return base;
}

//aタグ押下時の処理
function handleDownload(){
    var bom = new Uint8Array([0xEF, 0xBB, 0xBF]);
    var content = res_data;
    var blob = new Blob([ bom, content ], { "type" : "text/csv" });
    
    var a_tag = document.getElementById("download");
        
    if (window.navigator.msSaveBlob) { 
        window.navigator.msSaveBlob(blob, "test.csv"); 

        // msSaveOrOpenBlobの場合はファイルを保存せずに開ける
        window.navigator.msSaveOrOpenBlob(blob, "test.csv"); 
    } else {
        a_tag.href = window.URL.createObjectURL(blob);
    }

}

//ajax成功時にaタグを作る
function add_btn() {
    var a_tabg_div = document.getElementById("add_link");
    var a = document.createElement("a");
    a.href = "#";
    a.id = "download";
    a.download = "test.csv";
    a.innerText = "ファイルをダウンロードします";
    a_tabg_div.appendChild(a);

    //click-event
    handleDownload();

}


//ファイルの内容取得
function handleFileSelect(evt) {
    var file = evt.target.files[0];
    var reader = new FileReader();

    reader.onerror = function(){
     alert('ファイルの読み込みに失敗しました');
    }
    reader.onload = function(){
        var csv = reader.result.replace(/\r?\n/g, "");
        var csvArray = csv.split(',');
        var fName = file.name;
        if (csvArray.length <= 5000){

            //ajax
            file_data = csvArray;
            file_name = baseName(fName);
            console.log(file_data);
            console.log(file_name);
            

        }else{
            alert('5000件以下にしてください');
        }
    }
    reader.readAsText(file);

}

//ファイルアップボタン押下時
$(document).ready(function () {
    var file_up = document.getElementById('upc_file_up');
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

//submit botton押下時
$(function(){
    $('#ajax').on('click',function(btn){
        btn.disabled=true;
        $.ajax({
            url:'http://localhost:80/phpinfo.php',
            type:'POST',
            data: {
                'file_data':file_data,
                'file_name':file_name,
                'condition':1
            }
        })
        //疎通成功
        .done((data) =>{
            res_data = data;
            console.log(res_data)
            add_btn();  
        })
        .fail((data) =>{
            console.log('失敗だよ');
        })
    });
});

