from rest_framework.throttling import UserRateThrottle

class ProductSubscriptionThrottle(UserRateThrottle):
    scope = "product_subscription"