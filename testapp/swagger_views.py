from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Define API URLs
SUBSCRIPTION_PLAN_DETAILS_URL = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionPlanDetails"
SUBSCRIPTION_REQUEST_URL = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionRequestWatchoOmni"

# Define Subscription Plan Schema
subscription_plan_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "SubscriptionPlanID": openapi.Schema(type=openapi.TYPE_INTEGER),
        "SubscriptionPlanName": openapi.Schema(type=openapi.TYPE_STRING),
        "SubscriptionPlanDescription": openapi.Schema(type=openapi.TYPE_STRING),
        "SubscriptionPlanDuration": openapi.Schema(type=openapi.TYPE_INTEGER),
        "SubscriptionPrice": openapi.Schema(type=openapi.TYPE_INTEGER),
        "Discount": openapi.Schema(type=openapi.TYPE_INTEGER),
        "SubscriptionActualPrice": openapi.Schema(type=openapi.TYPE_INTEGER),
        "IsSubscribed": openapi.Schema(type=openapi.TYPE_INTEGER),
        "AutoDebitMode": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "AutoDebitModeValue": openapi.Schema(type=openapi.TYPE_INTEGER),
        "SubscriptionSeqNo": openapi.Schema(type=openapi.TYPE_INTEGER),
        "SubscriptionGroupNo": openapi.Schema(type=openapi.TYPE_INTEGER),
        "MonthlyPrice": openapi.Schema(type=openapi.TYPE_INTEGER),
        "SubscriptionApps": openapi.Schema(type=openapi.TYPE_STRING, default=None),
        "SubscriptionRule": openapi.Schema(type=openapi.TYPE_STRING, default=None),
        "PGSubscriptionID": openapi.Schema(type=openapi.TYPE_STRING, default=""),
    },
)

@swagger_auto_schema(
    method="post",
    operation_summary="Fetch Subscription Plans",
    operation_description="API to fetch available subscription plans for a user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "OTTSubscriberID": openapi.Schema(type=openapi.TYPE_STRING, default="-1"),
            "UserID": openapi.Schema(type=openapi.TYPE_STRING, default="152"),
            "UserType": openapi.Schema(type=openapi.TYPE_STRING, default="DS"),
            "Source": openapi.Schema(type=openapi.TYPE_STRING, default="IS"),
        },
    ),
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, default="success"),
            "message": openapi.Schema(type=openapi.TYPE_STRING, default="Static response for demo"),
            "api_url": openapi.Schema(type=openapi.TYPE_STRING, default=SUBSCRIPTION_PLAN_DETAILS_URL),
            "data": openapi.Schema(type=openapi.TYPE_ARRAY, items=subscription_plan_schema),
        },
    )},
)
@api_view(["POST"])
def subscription_plan_details(request):
    """Returns static subscription plan details for demo purposes."""
    
    static_response = {
        "status": "success",
        "message": "Static response for demo",
        "api_url": SUBSCRIPTION_PLAN_DETAILS_URL,
        "data": [
            {
                "SubscriptionPlanID": 1762,
                "SubscriptionPlanName": "Watcho Basic",
                "SubscriptionPlanDescription": "Basic Plan with limited features",
                "SubscriptionPlanDuration": 1,
                "SubscriptionPrice": 49,
                "Discount": 10,
                "SubscriptionActualPrice": 39,
                "IsSubscribed": 0,
                "AutoDebitMode": False,
                "AutoDebitModeValue": 0,
                "SubscriptionSeqNo": 1,
                "SubscriptionGroupNo": 1,
                "MonthlyPrice": 33,
                "SubscriptionApps": None,
                "SubscriptionRule": None,
                "PGSubscriptionID": "",
            }
        ],
    }
    
    return Response(static_response)

# Define Subscription Request Schema
subscription_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "UserID": openapi.Schema(type=openapi.TYPE_STRING, description="Only numeric values", default="112235"),
        "UserType": openapi.Schema(type=openapi.TYPE_STRING, description="String Value", default="DS"),
        "MobileNo": openapi.Schema(type=openapi.TYPE_STRING, description="String Value", default="8126631764"),
        "PlanId": openapi.Schema(type=openapi.TYPE_INTEGER, description="Numeric value (10 digit)", default=1762),
        "Amount": openapi.Schema(type=openapi.TYPE_NUMBER, description="Pack price", default=39.00),
        "TransactionNo": openapi.Schema(type=openapi.TYPE_STRING, description="IS Transaction ID", default="TRAN00101"),
        "Source": openapi.Schema(type=openapi.TYPE_STRING, description="Default value ‘IS’", default="IS"),
    },
)

@swagger_auto_schema(
    method="post",
    operation_summary="Subscribe to a Plan",
    operation_description="API to request a subscription to a Watcho plan.",
    request_body=subscription_request_schema,
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "AccessToken": openapi.Schema(type=openapi.TYPE_STRING, default=None),
            "TokenType": openapi.Schema(type=openapi.TYPE_STRING, default=None),
            "ResultType": openapi.Schema(type=openapi.TYPE_INTEGER, default=0),
            "ResultCode": openapi.Schema(type=openapi.TYPE_INTEGER, default=0),
            "ResultDesc": openapi.Schema(type=openapi.TYPE_STRING, default="Success"),
            "Result": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "OrderID": openapi.Schema(type=openapi.TYPE_STRING, default="UREPR1009241459772713"),
                    "Description": openapi.Schema(type=openapi.TYPE_STRING, default=None),
                    "IsAutoCommitted": openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
                    "ActualPayableAmount": openapi.Schema(type=openapi.TYPE_NUMBER, default=39.0),
                    "PaymentGetwayToken": openapi.Schema(type=openapi.TYPE_STRING, default=None),
                    "AlgorithmKey": openapi.Schema(type=openapi.TYPE_STRING, default=""),
                    "PaymentGatewayID": openapi.Schema(type=openapi.TYPE_STRING, default=None),
                    "MobileNo": openapi.Schema(type=openapi.TYPE_STRING, default=None),
                    "SubscriptionParam": openapi.Schema(type=openapi.TYPE_STRING, default=None),
                },
            ),
        },
    )},
)
@api_view(["POST"])
def subscription_request_watcho_omni(request):
    """Handles subscription requests for Watcho Omni plans."""
    
    static_response = {
        "AccessToken": None,
        "TokenType": None,
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "Success",
        "Result": {
            "OrderID": "UREPR1009241459772713",
            "Description": None,
            "IsAutoCommitted": False,
            "ActualPayableAmount": 39.0,
            "PaymentGetwayToken": None,
            "AlgorithmKey": "",
            "PaymentGatewayID": None,
            "MobileNo": None,
            "SubscriptionParam": None,
        },
    }
    
    return Response(static_response)
