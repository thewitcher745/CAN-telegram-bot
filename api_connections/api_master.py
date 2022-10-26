import ccxt
from ccxt.base.errors import AuthenticationError


class Exchange:
    def __init__(self, api_key="", secret_key="", exchange_id="binance", account_type="future"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.exchange_id = exchange_id
        self.account_type = account_type

        exchange_class = getattr(ccxt, "binance")
        self.exchange = exchange_class(
            {
                "apiKey": api_key,
                "secret": secret_key,
                "options": {
                    "defaultType": "future",
                },
            }
        )

    def api_fetch_client_balance(self):
        balances = self.exchange.fetch_balance()
        btc_price = float(self.exchange.fetchTicker("BTC/USDT")["close"])
        return {
            "totalWalletBalance": (
                float(balances["free"]["USDT"]),
                float(balances["free"]["USDT"]) / btc_price,
            ),
            # "totalMarginBalance": (
            #     float(balances["totalMarginBalance"]),
            #     float(balances["totalMarginBalance"]) / btc_price,
            # ),
            # "totalCrossWalletBalance": (
            #     float(balances["totalCrossWalletBalance"]),
            #     float(balances["totalCrossWalletBalance"]) / btc_price,
            # ),
            # "maxWithdrawAmount": (
            #     float(balances["maxWithdrawAmount"]),
            #     float(balances["maxWithdrawAmount"]) / btc_price,
            # ),
        }

    def api_check_api_connection(self):
        try:
            self.exchange.fetch_balance()
            return "Success"
        except AuthenticationError:
            return "AuthError"
        # except Exception:
        #     return "GeneralError"
