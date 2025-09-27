import os
import json
import traceback
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import configparser

# 初始化HTTP服务
app = FastAPI()
# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 读取配置文件
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.conf')
config.read(config_path)

@app.post("/wx-login")
async def wx_login(request: Request):
    try:
        _data = request.query_params
        try:
            js_code = _data.get("js_code", "")
            # 获取密钥配置
            appid = _data.get("appid", "")
            appSecret = config.get(appid, 'appSecret')
            if js_code == "":
                return {"errcode": -1001, "errmsg": "Invalid Parameter"}
            if appid == "" or appSecret == "":
                return {"errcode": -1002, "errmsg": "Invalid Secret"}
        except:
            return {"errcode": -1003, "errmsg": "Invalid Parameter"}
        
        url = "https://api.weixin.qq.com/sns/jscode2session"
        querystring = {"grant_type": "authorization_code", "appid": appid, "secret": appSecret, "js_code": js_code}
        payload = ""
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
            "Connection": "keep-alive"
        }
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        res = response.text
        res = json.loads(res)
            
        openid = res.get("openid", "")
        session_key = res.get("session_key", "")
        unionid = res.get("unionid", "")
        
        # 错误码透传
        return {
            "errcode": res.get("errcode", 0),
            "errmsg": res.get("errmsg", "ok"),
            "data": {
                "openid": openid,
                "session_key": session_key,
                "unionid": unionid
            } if res.get("errcode", 0) == 0 else None
        }
    except Exception as e:
        print(traceback.format_exc())
        return {"errcode": -1, "errmsg": str(e)}

# 运行
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=36842, reload=False)
  
