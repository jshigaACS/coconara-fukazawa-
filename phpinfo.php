<?php
header("Access-Control-Allow-Origin: *");
 
/**********************************************************************
 * Ajax による呼び出しなら true を返す関数．
*/
function isAjax() {
  if(isset($_POST['credential']) && strtolower($_POST['credential']) == 'credential'){

    return true;
  }
  return false;
}

// Ajax 以外での呼び出し時はエラーを出力．
if(!isAjax()) {
  $ip = $_SERVER['REMOTE_ADDR'];
  print('<script type="text/javascript">alert("あなたのIPアドレス:'.$ip.'を管理者へ通報しました。");</script>');
  exit;

}else{

  $file_name = $_POST['file_name'];
  $file_data = $_POST['file_data'];
  $condition = $_POST['condition'];
  $appID = $_POST['appId'];
  //print_r($file_data);
  $outPutArry=array();
  foreach ($file_data as $d) {
      //$cmd = "python3 /home/ubuntu/coconara/call_ebayAPI.py $file_name $d $condition $appID";
      $cmd = "~/.pyenv/shims/python3 /home/kouenjizack/usedfuruichi.com/public_html/item_manage_src/dist/call_ebayAPI.py ".$file_name." ".$d." ".$condition." ".$appID;
      
      exec($cmd,$output,$rc);
      #$outPutArray[] = $output;//outputは配列で帰るArray

    }

    foreach($output as $line){
    print($line."\n");
  }

}






?>
