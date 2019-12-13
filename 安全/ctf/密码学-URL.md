
# URL编码

* url编码

---

## URL编码

* 描述
> url编码是一种浏览器用来打包表单输入的格式。


* 规则
> 编码前：I love you
> 编码后：theName=I+love+you


* 在线解密

* python编码

```python
# 编码
from urllib import  parse

# url编码
url ='http://www.baidu.com?query=python基础教程'
data=parse.quote_plus(url)  #使用parse.quote_plus方法
print(data)

#运行结果:http%3A%2F%2Fwww.baidu.com%3Fquery%3Dpython%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B
```
```python
# 解密
from urllib import  parse

baidu_url= 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=' \
           'python%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B&oq=python&rsv_pq=b6c92ffc00023232&rsv_t=be4d%2FdgIVLHbmdj5jU9bfpJTXGIAcO4y2u%2BfKsxWWJW2wIKbEuXL6tNXiug&rqlang=cn&rsv_enter=1&inputT=878&rsv_sug3=9&rsv_sug1=3&rsv_sug7=100&rsv_sug2=0&prefixsug=python&rsp=1&rsv_sug4=2134&rsv_sug=1'
print(parse.unquote_plus(baidu_url))#url解码
```

