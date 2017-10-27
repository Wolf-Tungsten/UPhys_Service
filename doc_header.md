### 关于身份认证

用户身份以token的形式暂存在客户端cookie中。
需要身份验证的接口在请求Headers里面添加 Access-token
如果遇到身份过期需要重新使用登录接口更新，token会在请求结果返回的同时写入cookie


### 关于请求

参数全部为json格式

### 正确返回结果格式约定

```
{
    "status": "success",
    "code": "200",
    "result":<前端关心的结果>
}
```