<?php
header("Access-Control-Allow-Origin: *");

/**********************************************************************
 * Ajax による呼び出しなら true を返す関数．
 * function isAjax() {
  if(isset($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest'){

    return true;
  }
  return false;
}

// Ajax 以外での呼び出し時はエラーを出力．
if(!isAjax()) {
  echo 'Error: Ajax 以外での呼び出しは禁止されています．';
  exit;
}

 **********************************************************************/



$file_name = $_POST['file_name'];
$file_data = $_POST['file_data'];
$condition = $_POST['condition'];
$appID = $_POST['appId'];
#print_r($file_data);
$outPutArry=array();
foreach ($file_data as $d) {
    $cmd = "python3 /home/ubuntu/coconara/call_ebayAPI.py $file_name $d $condition $appID";
    exec($cmd,$output,$rc);
    #$outPutArray[] = $output;//outputは配列で帰るArray
    #print_r($output);    
}

foreach($output as $line){
    print($line."\n");
}

?>
