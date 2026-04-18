from rest_framework import serializers
from .models import User, Category, Product, SubscriptionPlan, Subscription, Order, OrderItem, PaymentTransaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "phone", "is_premium", "premium_since"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "category",
            "price",
            "discount_price",
            "inventory",
            "is_active",
            "is_featured",
            "featured_rank",
            "image_url",
            "created_at",
            "updated_at",
            "effective_price",
        ]


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "slug", "price", "duration_days", "benefits", "is_active"]


class AmazonProductImportSerializer(serializers.Serializer):
    url = serializers.URLField()


class AmazonProductCreateSerializer(serializers.Serializer):
    url = serializers.URLField()
    category_id = serializers.IntegerField(required=False)
    inventory = serializers.IntegerField(default=10)
    discount_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    is_active = serializers.BooleanField(default=True)


class PaymobCheckoutSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    billing_data = serializers.JSONField()
    integration_id = serializers.IntegerField(required=False)


class PaymobWebhookSerializer(serializers.Serializer):
    id = serializers.CharField()
    success = serializers.BooleanField()
    data = serializers.JSONField()


class SubscriptionPurchaseSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    auto_renew = serializers.BooleanField(default=True)


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ["id", "user", "plan", "status", "started_at", "expires_at", "auto_renew", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "payment_status",
            "total_amount",
            "tax_amount",
            "shipping_amount",
            "discount_amount",
            "premium_discount",
            "payment_gateway",
            "shipping_address",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ["id", "order", "provider", "reference", "amount", "status", "payload", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
