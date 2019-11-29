
# unicode

* unicode编码

---

## unicode编码

* 描述
> Unicode 编码共有三种具体实现，分别为utf-8,utf-16,utf-32，其中utf-8占用一到四个字节，utf-16占用二或四个字节，utf-32占用四个字节。

* 规则
> 原文本: You had me at hello  
> 编码后: \u0059\u006f\u0075\u0020\u0068\u0061\u0064\u0020\u006d\u0065\u0020\u0061\u0074\u0020\u0068\u0065\u006c\u006c\u006f

* 在线解密


* python编码
```python
# 加密
> print('我喜欢你'.encode('unicode_escape'))
b'\\u6211\\u559c\\u6b22\\u4f60
```

```python
# 解密
s1='\\u6211\\u559c\\u6b22\\u4f60'
#转为utf-8(明文)
print(s1.encode('utf8').decode('unicode_escape'))
#转为utf-8编码
print(s1.encode('utf8').decode('unicode_escape').encode('utf8'))
```
