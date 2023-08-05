import urllib.parse
from datetime import datetime
from typing import Any, Dict

from requests import Response

from fastel.logistics.ecpay.models import (
    EcpayCVSMapModel,
    EcpayLogisticsModel,
    EcpayPrintOrderInfo,
)
from fastel.payment.cryptors import MD5Cryptor
from fastel.utils import TW, requests


class EcpayLogistics:
    def __init__(
        self,
        merchant_id: str,
        hash_key: str,
        hash_iv: str,
        stage: str = "stg",
    ) -> None:
        self.merchant_id = merchant_id
        self.hash_key = hash_key
        self.hash_iv = hash_iv
        self.stage = stage
        self.cryptor = MD5Cryptor(hash_key=hash_key, hash_iv=hash_iv)

    @property
    def logistics_url(self) -> str:
        if self.stage in ["prod", "production"]:
            return "https://logistics.ecpay.com.tw"
        return "https://logistics-stage.ecpay.com.tw"

    def create_logistics(self, data: EcpayLogisticsModel) -> Dict[str, Any]:
        url = self.logistics_url + "/Express/Create"
        data_dict = data.dict(exclude_none=True)
        now = datetime.now(TW)
        gateway_payload = {
            **data_dict,
            "MerchantID": self.merchant_id,
            "MerchantTradeDate": now.strftime("%Y/%m/%d %H:%M:%S"),
        }
        mac_value = self.cryptor.encrypt(gateway_payload)
        gateway_payload["CheckMacValue"] = mac_value

        print("[Logistics Create Req]", gateway_payload)
        resp: Response = requests.post(url, data=gateway_payload)
        resp.raise_for_status()
        rtn_code, real_resp = resp.text.split("|")
        print("[Logistics Create Resp]", rtn_code, real_resp)

        if rtn_code != "1":
            return {"error": real_resp}
        return dict(urllib.parse.parse_qsl(real_resp))

    @staticmethod
    def build_input(data: Dict[str, Any]) -> str:
        input_row = "\n".join(
            map(
                lambda k: f'<input type="hidden" name="{k[0]}" value="{k[1]}"><br>',
                data.items(),
            )
        )
        return input_row

    def cvs_map(self, data: EcpayCVSMapModel) -> str:
        url = self.logistics_url + "/Express/map"
        data_dict = data.dict(exclude_none=True)
        data_dict["MerchantID"] = self.merchant_id
        row = self.build_input(data=data_dict)
        template = f"""
        <html>
          <body>
              <form name='ecpay' method='post' action='{url}'>
                  {{}}
                  <input type='hidden' value='Submit'>
              </form>
              </body>
              <script type="text/javascript">ecpay.submit();
          </script>
        </html>
        """
        result = template.format(row)
        return result

    def get_shipping_note(self, data: EcpayPrintOrderInfo) -> str:
        request_body = data.dict(exclude_none=True)
        logistics_subtype = request_body.pop("LogisticsSubType")
        if logistics_subtype in [
            "FAMI",
            "UNIMART",
            "UNIMARTFREEZE",
            "HILIFE",
            "TCAT",
            "ECAN",
        ]:
            url = f"{self.logistics_url}/helper/printTradeDocument"
        else:
            url = f"{self.logistics_url}/Express/Print{logistics_subtype}OrderInfo"

        request_body["MerchantID"] = self.merchant_id
        mac_value = self.cryptor.encrypt(request_body)
        request_body["CheckMacValue"] = mac_value
        print(url)
        resp: Response = requests.post(url, data=request_body)
        resp.raise_for_status()
        return resp.content.decode()
