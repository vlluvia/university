

# Xsser

* 简介
* 简单使用
* 进行编码
* 使用帮助

## 简介
``` 
命令行 root@kali:~# xsser

图形化 root@kali:~# xsser –gtk
```

## 简单使用
> http://10.10.10.132/dvwa/vulnerabilities/xss_r/?name=a#

* -u 指定 URL
> xsser -u "http://10.10.10.132/dvwa/vulnerabilities/"

* -g GET 请求时使用，内容是当前页面的本层路径
> -g "xss_r/?name="

* -p POST 请求时使用
* -s 统计多少次请求
* –reverse-check
  

* 测试用例
``` 
xsser -u "http://10.10.10.132/dvwa/vulnerabilities/" -g "xss_r/?name=" --cookie="security=low; PHPSESSID=f258647d71bed83d9aa022b4e9fc3a36" -s -v --reverse-check

```  
* –heuristic 检查被过滤的参数
``` 
# 作用是验证过滤了哪些字符，而不是有无漏洞
root@kali:~# xsser -u "http://10.10.10.132/dvwa/vulnerabilities/" -g "xss_r/?name=" --cookie="security=low; PHPSESSID=f258647d71bed83d9aa022b4e9fc3a36" -s -v --heuristic

```  

## 进行编码
* 对 payload 编码，绕过服务器端筛选过滤
``` 
*Select Bypasser(s)*:
    These options can be used to encode vector(s) and try to bypass
    possible anti-XSS filters. They can be combined with other techniques:

    --Str               Use method String.FromCharCode()
    --Une               Use Unescape() function
    --Mix               Mix String.FromCharCode() and Unescape()
    --Dec               Use Decimal encoding
    --Hex               Use Hexadecimal encoding
    --Hes               Use Hexadecimal encoding with semicolons
    --Dwo               Encode IP addresses with DWORD
    --Doo               Encode IP addresses with Octal
    --Cem=CEM           Set different 'Character Encoding Mutations'

```

* 复用编码
> (reversing obfuscators) (ex: 'Mix,Une,Str,Hex')

## 使用帮助
``` 
 Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -s, --statistics      show advanced statistics output results
  -v, --verbose         active verbose mode output results
  --gtk                 launch XSSer GTK Interface
  --wizard              start Wizard Helper!

  *Special Features*:
    You can set Vector(s) and Bypasser(s) to build complex scripts for XSS
    code embedded. XST allows you to discover if target is vulnerable to
    'Cross Site Tracing' [CAPEC-107]:

    --imx=IMX           IMX - Create an image with XSS (--imx image.png)
    --fla=FLASH         FLA - Create a flash movie with XSS (--fla movie.swf)
    --xst=XST           XST - Cross Site Tracing (--xst http(s)://host.com)

  *Select Target(s)*:
    At least one of these options must to be specified to set the source
    to get target(s) urls from:

    --all=TARGET        Automatically audit an entire target
    -u URL, --url=URL   Enter target to audit
    -i READFILE         Read target(s) urls from file
    -d DORK             Search target(s) using a query (ex: 'news.php?id=')
    -l                  Search from a list of 'dorks'
    --De=DORK_ENGINE    Use this search engine (default: duck)
    --Da                Search massively using all search engines

  *Select type of HTTP/HTTPS Connection(s)*:
    These options can be used to specify which parameter(s) we want to use
    as payload(s) to inject:

    -g GETDATA          Send payload using GET (ex: '/menu.php?q=')
    -p POSTDATA         Send payload using POST (ex: 'foo=1&bar=')
    -c CRAWLING         Number of urls to crawl on target(s): 1-99999
    --Cw=CRAWLER_WIDTH  Deeping level of crawler: 1-5 (default 3)
    --Cl                Crawl only local target(s) urls (default TRUE)

  *Configure Request(s)*:
    These options can be used to specify how to connect to the target(s)
    payload(s). You can choose multiple:

    --cookie=COOKIE     Change your HTTP Cookie header
    --drop-cookie       Ignore Set-Cookie header from response
    --user-agent=AGENT  Change your HTTP User-Agent header (default SPOOFED)
    --referer=REFERER   Use another HTTP Referer header (default NONE)
    --xforw             Set your HTTP X-Forwarded-For with random IP values
    --xclient           Set your HTTP X-Client-IP with random IP values
    --headers=HEADERS   Extra HTTP headers newline separated
    --auth-type=ATYPE   HTTP Authentication type (Basic, Digest, GSS or NTLM)
    --auth-cred=ACRED   HTTP Authentication credentials (name:password)
    --proxy=PROXY       Use proxy server (tor: http://localhost:8118)
    --ignore-proxy      Ignore system default HTTP proxy
    --timeout=TIMEOUT   Select your timeout (default 30)
    --retries=RETRIES   Retries when the connection timeouts (default 1)
    --threads=THREADS   Maximum number of concurrent HTTP requests (default 5)
    --delay=DELAY       Delay in seconds between each HTTP request (default 0)
    --tcp-nodelay       Use the TCP_NODELAY option
    --follow-redirects  Follow server redirection responses (302)
    --follow-limit=FLI  Set limit for redirection requests (default 50)

  *Checker Systems*:
    These options are useful to know if your target is using filters
    against XSS attacks:

    --hash              send a hash to check if target is repeating content
    --heuristic         discover parameters filtered by using heuristics
    --discode=DISCODE   set code on reply to discard an injection
    --checkaturl=ALT    check reply using: alternative url -> Blind XSS
    --checkmethod=ALTM  check reply using: GET or POST (default: GET)
    --checkatdata=ALD   check reply using: alternative payload
    --reverse-check     establish a reverse connection from target to XSSer to
                        certify that is 100% vulnerable (recommended!)

  *Select Vector(s)*:
    These options can be used to specify injection(s) code. Important if
    you don't want to inject a common XSS vector used by default. Choose
    only one option:

    --payload=SCRIPT    OWN  - Inject your own code
    --auto              AUTO - Inject a list of vectors provided by XSSer

  *Anti-antiXSS Firewall rules*:
    These options can be used to try to bypass specific WAF/IDS products.
    Choose only if required:

    --Phpids0.6.5       PHPIDS (0.6.5) [ALL]
    --Phpids0.7         PHPIDS (0.7) [ALL]
    --Imperva           Imperva Incapsula [ALL]
    --Webknight         WebKnight (4.1) [Chrome]
    --F5bigip           F5 Big IP [Chrome + FF + Opera]
    --Barracuda         Barracuda WAF [ALL]
    --Modsec            Mod-Security [ALL]
    --Quickdefense      QuickDefense [Chrome]

  *Select Bypasser(s)*:
    These options can be used to encode vector(s) and try to bypass
    possible anti-XSS filters. They can be combined with other techniques:

    --Str               Use method String.FromCharCode()
    --Une               Use Unescape() function
    --Mix               Mix String.FromCharCode() and Unescape()
    --Dec               Use Decimal encoding
    --Hex               Use Hexadecimal encoding
    --Hes               Use Hexadecimal encoding with semicolons
    --Dwo               Encode IP addresses with DWORD
    --Doo               Encode IP addresses with Octal
    --Cem=CEM           Set different 'Character Encoding Mutations'
                        (reversing obfuscators) (ex: 'Mix,Une,Str,Hex')

  *Special Technique(s)*:
    These options can be used to inject code using different XSS
    techniques. You can choose multiple:

    --Coo               COO - Cross Site Scripting Cookie injection
    --Xsa               XSA - Cross Site Agent Scripting
    --Xsr               XSR - Cross Site Referer Scripting
    --Dcp               DCP - Data Control Protocol injections
    --Dom               DOM - Document Object Model injections
    --Ind               IND - HTTP Response Splitting Induced code
    --Anchor            ANC - Use Anchor Stealth payloader (DOM shadows!)

  *Select Final injection(s)*:
    These options can be used to specify the final code to inject on
    vulnerable target(s). Important if you want to exploit 'on-the-wild'
    the vulnerabilities found. Choose only one option:

    --Fp=FINALPAYLOAD   OWN    - Exploit your own code
    --Fr=FINALREMOTE    REMOTE - Exploit a script -remotely-
    --Doss              DOSs   - XSS (server) Denial of Service
    --Dos               DOS    - XSS (client) Denial of Service
    --B64               B64    - Base64 code encoding in META tag (rfc2397)

  *Special Final injection(s)*:
    These options can be used to execute some 'special' injection(s) on
    vulnerable target(s). You can select multiple and combine them with
    your final code (except with DCP code):

    --Onm               ONM - Use onMouseMove() event
    --Ifr               IFR - Use <iframe> source tag

  *Reporting*:
    --save              export to file (XSSreport.raw)
    --xml=FILEXML       export to XML (--xml file.xml)

  *Miscellaneous*:
    --silent            inhibit console output results
    --no-head           NOT send a HEAD request before start a test
    --alive=ISALIVE     set limit of errors before check if target is alive
    --update            check for latest stable version

```
