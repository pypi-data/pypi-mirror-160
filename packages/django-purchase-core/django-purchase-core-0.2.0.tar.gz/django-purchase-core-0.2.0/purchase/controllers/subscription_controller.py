from purchase.models.choices import Platform
from purchase.verifiers import AppleVerifier


class SubscriptionController:
    __platform = None
    __payload = None
    __subscription_id = None
    __user_token = None

    @staticmethod
    def get_data_from_payload(payload) -> dict:
        pass

    def setup_appstore(self, payload):
        self.__platform = Platform.ios
        self.__payload = payload

    def setup_google(self, subscription_id: str, user_token: str):
        self.__platform = Platform.android
        self.__subscription_id = subscription_id
        self.__user_token = user_token

    def get_verifier(self):
        if self.__platform == Platform.ios:
            return AppleVerifier(**SubscriptionController.get_data_from_payload(self.__payload))

    def validate(self):
        pass
