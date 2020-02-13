
# Volatility插件

## Firefoxhistory 插件
* 网址
> http://downloads.volatilityfoundation.org/contest/2014/DaveLasalle_ForensicSuite.zip

* 命令
``` 
/usr/lib/python2.7/dist-packages/volatility/plugins/
volatility -f 7.raw --profile=Win7SP1x64 firefoxhistory
```

## USN 日志记录插件

* 描述
> NTFS特性，用于跟踪硬盘内容变化（不记录具体变更内容）


* 网址
> https://raw.githubusercontent.com/tomspencer/volatility/master/usnparser/usnparser.py

* 命令
``` 
volatility -f 7.raw --profile=Win7SP1x64 usnparser --output=csv --output-file=usn.csv 
```

## Timeline 插件
> 从多个位置收集大量系统活动信息
``` 
 volatility -f 7.raw --profile=Win7SP1x64 timeliner
```


## 内存取证发现恶意软件
* 网址
> https://github.com/volatilityfoundation/volatility/wiki/Memory-Samples  
> https://code.google.com/archive/p/volatility/wikis/SampleMemoryImages.wiki


## 内存取证发现恶意软件
* 命令
``` 
// XP：建立 meterpreter session 后 dump 内存分析
volatility -f xp.raw --profile=WinXPSP3x86 pstree
volatility connscan 　　# 网络连接
volatility getsids -p 111,222 　　# SID
volatility dlllist -p 111,222 　　# 数量
volatility malfind -p 111,222 -D test 　　# 检查结果查毒
```


