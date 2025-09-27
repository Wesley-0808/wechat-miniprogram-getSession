# Wechat Miniprogram getSession
获取微信小程序的会话信息的Python服务模板
[官方文档](https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html)

### 🚀 Feature
- 使用FastAPI框架
- 返回标准JSON格式响应
- 敏感信息通过配置文件管理
- 支持多账号，通过同一服务可用于多个小程序使用

### 📦 使用指南
#### 1. 获取微信凭证
在「开发管理」→「开发设置」中获取小程序的`appid`和`appSecret`

#### 2. 安装依赖
```bash
pip install fastapi uvicorn requests configparser
```

#### 3. 配置服务
修改`config.conf`文件(`config.example.conf`修改后需命名为`config.conf`)，格式如下：
```conf
[appid1]
appsecret = <KEY>

[appid2]
appsecret = <KEY>
```

#### 4. 启动服务
```bash
python service.py
```
服务将运行在 `http://0.0.0.0:36842`

### 🌐 API 接口
- **GET/POST** `/wx-login`
  - 参数：
    |参数名称|类型|是否必填|说明|
    |---|---|---|---|
    |js_code|string|Y|登录时获取的 code，可通过wx.login获取|
    |appid|string|Y|区分账号和获取信息使用|
  - 返回：`{errcode: STATUS_CODE, errmsg: STATUS_MSG, data: DATA}`
