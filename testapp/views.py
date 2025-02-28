from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import base64
from drf_yasg.utils import swagger_auto_schema

# Define API URLs
SUBSCRIPTION_PLAN_DETAILS_URL = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionPlanDetails"


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
    tags=["Watcho"],
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
            "SubscriptionPlanName": "Watcho Plan",
            "SubscriptionPlanDescription": "Watcho Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 49,
            "Discount": 20,
            "SubscriptionActualPrice": 39,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 1,
            "MonthlyPrice": 33,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 1764,
            "SubscriptionPlanName": "WATCHO EXCLUSIVES",
            "SubscriptionPlanDescription": "WATCHO EXCLUSIVES",
            "SubscriptionPlanDuration": 12,
            "SubscriptionPrice": 599,
            "Discount": 50,
            "SubscriptionActualPrice": 299,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 12,
            "SubscriptionGroupNo": 1,
            "MonthlyPrice": 253,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 84869,
            "SubscriptionPlanName": "Watcho Masti",
            "SubscriptionPlanDescription": "14 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 1208,
            "Discount": 92,
            "SubscriptionActualPrice": 99,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 4,
            "MonthlyPrice": 84,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 84870,
            "SubscriptionPlanName": "Watcho Dhamaal ",
            "SubscriptionPlanDescription": "16 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 1341,
            "Discount": 85,
            "SubscriptionActualPrice": 199,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 5,
            "MonthlyPrice": 169,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 84871,
            "SubscriptionPlanName": "WATCHO MAX OLD",
            "SubscriptionPlanDescription": "17 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 1740,
            "Discount": 83,
            "SubscriptionActualPrice": 299,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 6,
            "MonthlyPrice": 253,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 102634,
            "SubscriptionPlanName": "WATCHO MAX NEW",
            "SubscriptionPlanDescription": "20 Apps in One Plan",
            "SubscriptionPlanDuration": 12,
            "SubscriptionPrice": 11137,
            "Discount": 82,
            "SubscriptionActualPrice": 1999,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 12,
            "SubscriptionGroupNo": 6,
            "MonthlyPrice": 1694,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 84873,
            "SubscriptionPlanName": "Watcho Super Max ",
            "SubscriptionPlanDescription": "21 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 2010,
            "Discount": 83,
            "SubscriptionActualPrice": 349,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 12,
            "MonthlyPrice": 296,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 12737,
            "SubscriptionPlanName": "Flexi-Max",
            "SubscriptionPlanDescription": "14 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 299,
            "Discount": 0,
            "SubscriptionActualPrice": 299,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 16,
            "MonthlyPrice": 253,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 11360,
            "SubscriptionPlanName": "Flexi-Max Annual",
            "SubscriptionPlanDescription": "14 Apps in One Plan",
            "SubscriptionPlanDuration": 12,
            "SubscriptionPrice": 2499,
            "Discount": 0,
            "SubscriptionActualPrice": 2499,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 12,
            "SubscriptionGroupNo": 16,
            "MonthlyPrice": 2118,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 84865,
            "SubscriptionPlanName": "Flexi-3 ",
            "SubscriptionPlanDescription": "9 Apps in One Plan",
            "SubscriptionPlanDuration": 12,
            "SubscriptionPrice": 0,
            "Discount": 0,
            "SubscriptionActualPrice": 0,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 12,
            "SubscriptionGroupNo": 16,
            "MonthlyPrice": 0,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 102889,
            "SubscriptionPlanName": "Watcho Mirchi",
            "SubscriptionPlanDescription": "5 Apps in One Plan",
            "SubscriptionPlanDuration": 12,
            "SubscriptionPrice": 2685,
            "Discount": 85,
            "SubscriptionActualPrice": 399,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 12,
            "SubscriptionGroupNo": 37,
            "MonthlyPrice": 338,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 106314,
            "SubscriptionPlanName": "Flexi - 3",
            "SubscriptionPlanDescription": "15 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 229,
            "Discount": 0,
            "SubscriptionActualPrice": 229,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 41,
            "MonthlyPrice": 194,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 106333,
            "SubscriptionPlanName": "South Max",
            "SubscriptionPlanDescription": "19 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 1860,
            "Discount": 83,
            "SubscriptionActualPrice": 309,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 43,
            "MonthlyPrice": 262,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 106334,
            "SubscriptionPlanName": "South Max",
            "SubscriptionPlanDescription": "19 Apps in One Plan",
            "SubscriptionPlanDuration": 12,
            "SubscriptionPrice": 12234,
            "Discount": 83,
            "SubscriptionActualPrice": 2099,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 12,
            "SubscriptionGroupNo": 43,
            "MonthlyPrice": 1779,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 107029,
            "SubscriptionPlanName": "Watcho Max",
            "SubscriptionPlanDescription": "16 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 1691,
            "Discount": 82,
            "SubscriptionActualPrice": 299,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 52,
            "MonthlyPrice": 253,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 107030,
            "SubscriptionPlanName": "Watcho Max",
            "SubscriptionPlanDescription": "16 Apps in One Plan",
            "SubscriptionPlanDuration": 12,
            "SubscriptionPrice": 11137,
            "Discount": 82,
            "SubscriptionActualPrice": 1999,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 12,
            "SubscriptionGroupNo": 52,
            "MonthlyPrice": 1694,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 2762,
            "SubscriptionPlanName": "Titanium Marathi HD",
            "SubscriptionPlanDescription": "Titanium Marathi HD",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 479,
            "Discount": 0,
            "SubscriptionActualPrice": 479,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 53,
            "MonthlyPrice": 406,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 2760,
            "SubscriptionPlanName": "Titanium HD",
            "SubscriptionPlanDescription": "Titanium HD",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 456,
            "Discount": 0,
            "SubscriptionActualPrice": 456,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 54,
            "MonthlyPrice": 386,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 134083,
            "SubscriptionPlanName": "Watcho_Bhoomika_Platinum",
            "SubscriptionPlanDescription": "10 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 199,
            "Discount": 0,
            "SubscriptionActualPrice": 199,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 55,
            "MonthlyPrice": 169,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 134085,
            "SubscriptionPlanName": "Watcho_AA2",
            "SubscriptionPlanDescription": "Watcho_AA2",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 229,
            "Discount": 0,
            "SubscriptionActualPrice": 229,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 56,
            "MonthlyPrice": 194,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 134087,
            "SubscriptionPlanName": "Watcho_K2",
            "SubscriptionPlanDescription": "17 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 229,
            "Discount": 0,
            "SubscriptionActualPrice": 229,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 57,
            "MonthlyPrice": 194,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 134088,
            "SubscriptionPlanName": "Watcho_K3",
            "SubscriptionPlanDescription": "17 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 229,
            "Discount": 0,
            "SubscriptionActualPrice": 229,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 58,
            "MonthlyPrice": 194,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 134089,
            "SubscriptionPlanName": "Watcho_K4",
            "SubscriptionPlanDescription": "17 Apps in One Plan",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 229,
            "Discount": 0,
            "SubscriptionActualPrice": 229,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 59,
            "MonthlyPrice": 194,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        },
        {
            "SubscriptionPlanID": 134084,
            "SubscriptionPlanName": "Watcho_AA1",
            "SubscriptionPlanDescription": "Watcho_AA1",
            "SubscriptionPlanDuration": 1,
            "SubscriptionPrice": 209,
            "Discount": 0,
            "SubscriptionActualPrice": 209,
            "IsSubscribed": 0,
            "AutoDebitMode": True,
            "AutoDebitModeValue": 0,
            "SubscriptionSeqNo": 1,
            "SubscriptionGroupNo": 60,
            "MonthlyPrice": 177,
            "SubscriptionApps": None,
            "SubscriptionRule": None,
            "PGSubscriptionID": ""
        }
            
        ],
    }
    
    return Response(static_response)


#====================================================
SUBSCRIPTION_REQUEST_URL = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionRequestWatchoOmni"
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
    tags=["Watcho"],
    operation_summary="Subscribe to a Plan",
    operation_description="API to request a subscription to a Watcho plan.",
    request_body=subscription_request_schema,
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "api_url": openapi.Schema(type=openapi.TYPE_STRING, default=SUBSCRIPTION_REQUEST_URL),
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



# ===============

# Current Plan Details API
SUBSCRIPTION_REQUEST_URL = "https://beta2-publicapis.dishtv.in/api/WatchoOne/CurrentPlanDeatils"
@swagger_auto_schema(
    method="post",
    tags=["Watcho"],
    operation_summary="Fetch Current Plan Details",
    operation_description="API to fetch the current subscription plan details of a user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "api_url": openapi.Schema(type=openapi.TYPE_STRING, default=SUBSCRIPTION_REQUEST_URL),
            "EntityType": openapi.Schema(type=openapi.TYPE_STRING, default="DS"),
            "EntityID": openapi.Schema(type=openapi.TYPE_STRING, default="112235"),
            "Source": openapi.Schema(type=openapi.TYPE_STRING, default="IS"),
            "SearchBy": openapi.Schema(type=openapi.TYPE_STRING, description="Mobile No as a Text"),
            "SearchValue": openapi.Schema(type=openapi.TYPE_STRING, description="Mobile number"),
        },
    ),
)
@api_view(["POST"])
def current_plan_details(request):
    """Fetches the current subscription plan details"""
    
    # Mock response
    response_data = {
        "AccessToken": None,
        "TokenType": None,
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "Success",
        "Result": {
            "SubscriptionPlanID": 5086,
            "SubscriberName": "JOGINDER",
            "SubscriptionPlanName": "Watcho Max",
            "SubscriptionPlanExpireDate": "2023-10-27T00:00:00",
        }
    }
    
    return Response(response_data)


#=====
api_url = "https://beta2-publicapis.dishtv.in/api/WatchoOne/VerifyTransaction"

# Verify Transaction API
@swagger_auto_schema(
    method="post",
    tags=["Watcho"],
    operation_summary="Verify Transaction",
    operation_description="API to verify a transaction using MerchantTransactionNo and TransactionNo.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
             "api_url": openapi.Schema(type=openapi.TYPE_STRING, default=api_url),
            "MerchantTransactionNo": openapi.Schema(type=openapi.TYPE_STRING, description="Third Party Merchant Transaction No"),
            "TransactionNo": openapi.Schema(type=openapi.TYPE_STRING, description="Third Party Transaction No (Euronet Transaction ID)"),
            "EntityID": openapi.Schema(type=openapi.TYPE_STRING, default="112235", description="Euronet ID"),
            "Source": openapi.Schema(type=openapi.TYPE_STRING, default="IS", description="Default value IS"),
        },
    ),
)
@api_view(["POST"])
def verify_transaction(request):
    """Verifies a transaction based on MerchantTransactionNo and TransactionNo."""
    
    # Mock response
    response_data = {
        "AccessToken": None,
        "TokenType": None,
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "Success",
        "Result": {
            "TransactionRefNo": "9687547623457",
            "TransactionID": "UR1459628379",
            "OTTSubscriberID": 51055806,
            "Amount": 499.0,
            "TransactionDate": "2023-06-09 19:14:34",
        }
    }
    
    return Response(response_data)

#==========

# API URLs
TRANSACTION_HISTORY_API_URL = "https://beta2-publicapis.dishtv.in/api/WatchoOne/TransactionHistory"

# Transaction History API
@swagger_auto_schema(
    method="post",
    tags=["Watcho"],
    operation_summary="Fetch Transaction History",
    operation_description="API to fetch transaction history based on EntityID and Mobile Number.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "api_url": openapi.Schema(type=openapi.TYPE_STRING, default=TRANSACTION_HISTORY_API_URL),
            "EntityID": openapi.Schema(type=openapi.TYPE_STRING, default="112235", description="Euronet ID"),
            "EntityType": openapi.Schema(type=openapi.TYPE_STRING, default="DS", description="Default Value DS"),
            "MobileNo": openapi.Schema(type=openapi.TYPE_STRING, description="10-digit mobile number"),
            "Source": openapi.Schema(type=openapi.TYPE_STRING, default="IS", description="Default value IS"),
        },
    ),
)
@api_view(["POST"])
def transaction_history(request):
    """Fetches transaction history based on EntityID and Mobile Number."""
    
    # Mock response
    response_data = {
        "AccessToken": None,
        "TokenType": None,
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "Success",
        "Result": [
            {
                "TransactionRefNo": "UREPR2006231459633463",
                "TransactionID": "9687547623457",
                "OTTSubscriberID": 51651665,
                "Amount": 499.00,
                "TransactionDate": "20-06-2023 12:47:53"
            },
            {
                "TransactionRefNo": "UREPR2006231459633466",
                "TransactionID": "9687547623457",
                "OTTSubscriberID": 51651665,
                "Amount": 499.00,
                "TransactionDate": "20-06-2023 13:09:21"
            }
        ]
    }
    
    return Response(response_data)


###

# API URL
SUBSCRIPTION_PLAN_API_URL = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionPlanDetailsWithDuration"

# Encryption function (Mock Implementation)
def encrypt_data(data):
    """Encrypts the given data (Mock base64 encoding for simplicity)."""
    json_data = json.dumps(data)
    encrypted_data = base64.b64encode(json_data.encode()).decode()
    return {"InputData": encrypted_data}

@swagger_auto_schema(
    method="post",
    tags=["Watcho"],
    operation_summary="Fetch Subscription Plans",
    operation_description="API to fetch subscription plan details based on OTTSubscriberID and Duration.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "api_url": openapi.Schema(type=openapi.TYPE_STRING, default=SUBSCRIPTION_PLAN_API_URL),
            "OTTSubscriberID": openapi.Schema(type=openapi.TYPE_INTEGER, default=-1, description="For all packs, use -1"),
            "EntityId": openapi.Schema(type=openapi.TYPE_STRING, default="10967703", description="Default Entity ID"),
            "EntityType": openapi.Schema(type=openapi.TYPE_STRING, default="DS", description="Default Value DS"),
            "Source": openapi.Schema(type=openapi.TYPE_STRING, default="IS", description="Default value IS"),
            "Duration": openapi.Schema(type=openapi.TYPE_INTEGER, description="Duration in months"),
        },
    ),
)
@api_view(["POST"])
def subscription_plan_details_with_duration(request):
    """Fetches subscription plan details based on OTTSubscriberID and Duration."""

    request_data = {
        "OTTSubscriberID": request.data.get("OTTSubscriberID", -1),
        "UserID": request.data.get("EntityId", "10967703"),
        "UserType": request.data.get("EntityType", "DS"),
        "Source": request.data.get("Source", "IS"),
        "Duration": request.data.get("Duration", 1),
    }

    # Encrypt the request data (Mocked with base64 for now)
    encrypted_request = encrypt_data(request_data)

    # Mock Response Data
    response_data = {
        "AccessToken": None,
        "TokenType": None,
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "Success",
        "Result": [
            {
                "SubscriptionPlanID": 1762,
                "SubscriptionPlanName": "Watcho Plan",
                "SubscriptionPlanDescription": "Watcho Plan",
                "SubscriptionPlanDuration": 1,
                "SubscriptionPrice": 49,
                "Discount": 20,
                "SubscriptionActualPrice": 39,
                "IsSubscribed": 0,
                "AutoDebitMode": False,
                "MonthlyPrice": 33
            },
            {
                "SubscriptionPlanID": 84869,
                "SubscriptionPlanName": "Watcho Masti",
                "SubscriptionPlanDescription": "14 Apps in One Plan",
                "SubscriptionPlanDuration": 1,
                "SubscriptionPrice": 1208,
                "Discount": 92,
                "SubscriptionActualPrice": 99,
                "IsSubscribed": 0,
                "AutoDebitMode": False,
                "MonthlyPrice": 84
            }
        ]
    }

    return Response(response_data)

##============
# API URL
SUBSCRIPTION_REQUEST_API_URL = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionRequestWatchoplan"

# Encryption function (Mock Implementation)
def encrypt_data(data):
    """Encrypts the given data (Mock base64 encoding for simplicity)."""
    json_data = json.dumps(data)  # Ensure json is imported
    encrypted_data = base64.b64encode(json_data.encode()).decode()
    return {"InputData": encrypted_data}

@swagger_auto_schema(
    method="post",
    tags=["Watcho"],
    operation_summary="Subscription Request for Watcho Plan",
    operation_description="API to request a subscription for a Watcho plan.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "api_url": openapi.Schema(type=openapi.TYPE_STRING, default=SUBSCRIPTION_REQUEST_API_URL),
            "UserID": openapi.Schema(type=openapi.TYPE_STRING, default="112235", description="Only Numeric Value"),
            "UserType": openapi.Schema(type=openapi.TYPE_STRING, default="DS", description="Default Value DS"),
            "MobileNo": openapi.Schema(type=openapi.TYPE_STRING, default="9879067821", description="Mobile Number"),
            "PlanId": openapi.Schema(type=openapi.TYPE_INTEGER, default=84870, description="Plan ID"),
            "TransactionNo": openapi.Schema(type=openapi.TYPE_STRING, default="TRAN00102", description="IS Transaction ID"),
            "Source": openapi.Schema(type=openapi.TYPE_STRING, default="IS", description="Default value IS"),
        },
    ),
)
@api_view(["POST"])
def subscription_request_watchoplan(request):
    """Handles subscription requests for Watcho plans."""

    request_data = {
        "UserID": request.data.get("UserID", "112235"),
        "UserType": request.data.get("UserType", "DS"),
        "MobileNo": request.data.get("MobileNo", "9879067821"),
        "PlanId": request.data.get("PlanId", 84870),
        "TransactionNo": request.data.get("TransactionNo", "TRAN00102"),
        "Source": request.data.get("Source", "IS"),
    }

    # Encrypt the request data (Mocked with base64 for now)
    encrypted_request = encrypt_data(request_data)

    # Mock Response Data
    response_data = {
        "AccessToken": None,
        "TokenType": None,
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "Success",
        "Result": {
            "OrderID": "UREPR1009241459772721",
            "Description": None,
            "IsAutoCommitted": False,
            "ActualPayableAmount": 199.0,
            "PaymentGetwayToken": None,
            "AlgorithmKey": "",
            "PaymentGatewayID": None,
            "MobileNo": None,
            "SubscriptionParam": None
        }
    }

    return Response(response_data)