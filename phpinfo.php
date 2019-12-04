<?php 
header("Access-Control-Allow-Origin: *");


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
