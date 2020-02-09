

# 弱点扫描

* VNC
``` 
// VNC 密码破解
use auxiliary/scanner/vnc/vnc_login
// VNC 无密码访问
use auxiliary/scanner/vnc/vnc_none_auth

```

* RDP
``` 
// RDP 远程桌面漏洞
// 检查不会造成DoS攻击
use auxiliary/scanner/rdp/ms12_020_check
```

* 设备后门
``` 
use auxiliary/scanner/ssh/juniper_backdoor
use auxiliary/scanner/ssh/fortinet_backdoor
```

* VMWare ESXi 
``` 
// VMWare ESXi 密码爆破
use auxiliary/scanner/vmware/vmauthd_login
use auxiliary/scanner/vmware/vmware_enum_vms

```


* WEB API 远程开启虚拟机
``` 
use auxiliary/admin/vmware/poweron_vm
```

* HTTP 弱点扫描
``` 
// 过期证书
use auxiliary/scanner/http/cert

// 显示目录及文件
use auxiliary/scanner/http/dir_listing
use auxiliary/scanner/http/files_dir

// WebDAV Unicode 编码身份验证绕过
use auxiliary/scanner/http/dir_webdav_unicode_bypass

// Tomcat 管理登录页面
use auxiliary/scanner/http/tomcat_mgr_login

// 基于 HTTP方法的身份验证绕过
use auxiliary/scanner/http/verb_auth_bypass

// Wordpress 密码爆破
use auxiliary/scanner/http/wordpress_login_enum
set URI /wordpress/wp-login.php

```


* WMAP WEB应用扫描器
``` 
// 根据SQLMAP的工作方式开发
load wmap
wmap_sites -a http://1.1.1.1
wmap_targets -t http://1.1.1.1/mutillidae/index.php
wmap_run -t
wmap_run -e
wmap_vulns -l
vulns
```

* Openvas
``` 
Load openvas
// 导入nbe格式扫描文件
db_import openvas.nbe
```

* Nexpose

* MSF 直接调用 NESSUS 执行扫描
``` 
Load nessus
nessus_help
nessus_connect admin:toor@1.1.1.1
nessus_policy_list
nessus_scan_new
nessus_report_list
```


