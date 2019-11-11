
# web基础-ssrf

* 出现场景

## 出现场景
* 能够对外发起网络请求的地方，就可能存在 SSRF 漏洞
* 从远程服务器请求资源（Upload from URL，Import & Export RSS Feed）
* 数据库内置功能（Oracle、MongoDB、MSSQL、Postgres、CouchDB）
* Webmail 收取其他邮箱邮件（POP3、IMAP、SMTP）
* 文件处理、编码处理、属性信息处理（ffmpeg、ImageMagic、DOCX、PDF、XML）

