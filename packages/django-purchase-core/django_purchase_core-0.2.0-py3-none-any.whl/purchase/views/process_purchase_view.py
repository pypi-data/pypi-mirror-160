import logging

from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import CreateAPIView

from purchase.exceptions import CustomStatus
from purchase.models.choices import PurchaseResponseStatus
from purchase.serializers import RequestSerialzier, ResponseSerializer
from purchase.controllers import PurchaseProcessController
from purchase.signals import purchase_completed

logger = logging.getLogger(__name__)


class ProcessPurchaseView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    parser_classes = [JSONParser]
    request_serializer = RequestSerialzier
    response_serializer = ResponseSerializer

    @swagger_auto_schema(
        responses={200: response_serializer()},
        request_body=request_serializer(),
        operation_id="Process Purchase",
        tags=["Purchase"],
        operation_description=(
            "API to provide validating purchases from AppStore or GooglePlay.<br>"
            "Statuses:<br>"
            "1. ok - ok :)<br>"
            "2. purchase already created - purchase with given payload was already processed<br>"
            "3. data is not valid - provided data is not valid to create purchase<br>"
            "4. error - some error occurred, check logs"
        ),
    )
    def post(self, request, *args, **kwargs):
        request_data = self.request_serializer(data=request.data)
        request_data.is_valid(raise_exception=True)
        request_data = request_data.validated_data
        try:
            response = self.purchase_process(data=request_data)
            return response
        except CustomStatus as cs:
            return Response(data=self.get_response_data(cs.message), status=200)
        except Exception as err:
            logger.log(logging.ERROR, err)
            return Response(data=self.get_response_data(PurchaseResponseStatus.error), status=200)

    def purchase_process(self, data: dict):
        purchase = PurchaseProcessController(serializer_data=data)

        if purchase.is_create:
            raise CustomStatus(PurchaseResponseStatus.purchase_already_created)

        create_is_done, purchase_model = purchase.try_to_create()
        if not create_is_done:
            raise CustomStatus(PurchaseResponseStatus.data_is_not_valid)

        is_sandbox, is_valid = purchase.verify()
        if is_sandbox:
            response_data = self.get_response_data(status=PurchaseResponseStatus.ok)
            return Response(data=response_data, status=200)

        if is_valid:
            purchase.lc.log(purchase_obj=purchase_model)
        else:
            purchase_model.set_transaction_id_to_fake()

        response_data = self.get_response_data(status=PurchaseResponseStatus.ok)
        purchase_completed.send(sender=self.__class__, instance=purchase)

        return Response(data=response_data, status=200)

    def get_response_data(self, status: str, error: str = None):
        serializable_data = {"status": status}
        if error:
            serializable_data.update({"error": error})
        response_data = self.response_serializer(data=serializable_data)
        response_data.is_valid(raise_exception=True)
        return response_data.validated_data
