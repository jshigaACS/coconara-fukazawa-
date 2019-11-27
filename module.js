//file-upload-Btn
document.getElementsByClassName('file_up').addEventListener('change', handleFileSelect, false);

function handleFileSelect(evt) {
    var file = evt.target.files;
    console.log('ok')
}

