import requests
import json

class FeiShuAuth(requests.auth.AuthBase):
    def __init__(self, app_id, app_secret):
        """
        Authentication used by Contact Bitable Class

        Args:
            app_id (``str``): Feishu Application ID API Key.
            app_secret (``str``): Feishu Application ID API Secret Key.
        """
        self.app_id = app_id
        self.app_secret = app_secret

    def get_tenant_access_token(self) -> str:
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        req_body = {"app_id": self.app_id,
                    "app_secret": self.app_secret,
                    }
        req = requests.post(url=url, headers=headers, data=json.dumps(req_body))

        if req.status_code == 200:
            rsp_dict = req.json()
            code = rsp_dict.get("code", -1)
            if code != 0:
                print("get tenant_access_token error, code =", code)
            return rsp_dict.get("tenant_access_token", "")
        else:
            return ""

    def __call__(self, request):
        self.api_key = self.get_tenant_access_token()
        auth_token = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.api_key)}
        request.headers.update(auth_token)
        return request
