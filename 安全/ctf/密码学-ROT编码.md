

# ROT编码

* ROT5
* ROT13
* ROT18
* ROT47
---

## ROT5
* 描述
> 只对数字进行编码，用当前数字往前数的第5个数字替换当前数字，例如当前为0，编码后变成5，当前为1，编码后变成6，以此类推顺序循环。
## ROT13
* 描述
> 只对字母进行编码，用当前字母往前数的第13个字母替换当前字母，例如当前为A，编码后变成N，当前为B，编码后变成O，以此类推顺序循环。

* 规则
> 原文本: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz  
> 加密后: NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm

* 在线解密

* python编码

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
s1 = "a1zLbgQsCESEIqRLwuQAyMwLyq2L5VwBxqGA3RQAyumZ0tmMvSGM2ZwB4tws"
rot13_1 = string.ascii_lowercase[:13]
rot13_2 = string.ascii_lowercase[13:]
result = []
for i in s1:
    find_1 = rot13_1.find(i.lower())
    if find_1 != -1:
        if i.isupper():
            result.append(rot13_2[find_1].upper())
            continue
        result.append(rot13_2[find_1])
    find_2 = rot13_2.find(i.lower())
    if find_2 != -1:
        if i.isupper():
            result.append(rot13_1[find_2].upper())
            continue
        result.append(rot13_1[find_2])
    if find_1 == -1 and find_2 == -1:
        result.append(i)
    
print("". join(result))

```

## ROT8
* 描述
> 这是一个异类，本来没有，它是将ROT5和ROT13组合在一起，为了好称呼，将其命名为ROT18。


## ROT47

* 描述
> 对数字、字母、常用符号进行编码，按照它们的ASCII值进行位置替换，用当前字符ASCII值往前数的第47位对应字符替换当前字符，例如当前为小写字母z，编码后变成大写字母K，当前为数字0，编码后变成符号_。用于ROT47编码的字符其ASCII值范围是33－126
