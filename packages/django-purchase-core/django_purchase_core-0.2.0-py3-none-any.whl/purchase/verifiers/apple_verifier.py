from dataclasses import dataclass

from purchase.utils import repeatable_request
from purchase.strings.verifiers import APPLE_URL, APPLE_SANDBOX_URL, APPLE_HEADERS


@dataclass
class AppleVerifier:  # pragma: no cover
    receipt: dict
    is_sandbox: bool
    product_id: str
    platform: str
    version: str
    transaction_id: str

    def get_url(self):
        if self.is_sandbox:
            return APPLE_SANDBOX_URL
        return APPLE_URL

    def verify(self) -> (bool, bool):
        data = {"receipt-data": self.receipt["payload"]}
        url = self.get_url()
        is_sandbox, result = self.request(url, data)
        return is_sandbox, result

    def request(self, url: str, data: dict) -> (bool, bool):
        is_sandbox = self.is_sandbox
        result = False

        response = repeatable_request(url=url, json=data, headers=APPLE_HEADERS).json()

        if response["status"] == 21008:  # is not sandbox
            is_sandbox = False
            response = repeatable_request(
                url=APPLE_URL, json=data, headers=APPLE_HEADERS
            ).json()

        if response["status"] == 21007:  # this is sandbox
            is_sandbox = True
            response = repeatable_request(
                url=APPLE_SANDBOX_URL, json=data, headers=APPLE_HEADERS
            ).json()

        if response["status"] == 0:
            products = response["receipt"]["in_app"]
            result = any(
                True
                for product in products
                if product.get("product_id") == self.product_id
                and product.get("transaction_id") == self.transaction_id
                or product.get("original_transaction_id") == self.transaction_id
            )

        return is_sandbox, result
