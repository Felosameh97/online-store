from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404

from .models import Category, Product, SubscriptionPlan, Subscription, Order, OrderItem, PaymentTransaction
from .serializers import (
    AmazonProductCreateSerializer,
    AmazonProductImportSerializer,
    CategorySerializer,
    OrderSerializer,
    PaymobCheckoutSerializer,
    PaymobWebhookSerializer,
    ProductSerializer,
    SubscriptionPlanSerializer,
    SubscriptionPurchaseSerializer,
    SubscriptionSerializer,
)
from .services import fetch_amazon_product_data, get_best_selling_products, update_featured_products
from .paymob import create_payment_key, verify_webhook_signature


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BestSellerProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return get_best_selling_products(days=30, limit=16)


class StoreDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)

        total_customers = Order.objects.values("user").distinct().count()
        total_orders = Order.objects.count()
        new_orders = Order.objects.filter(status=Order.STATUS_NEW).count()
        pending_payments = Order.objects.filter(payment_status=Order.PAYMENT_PENDING).count()
        total_revenue = Order.objects.filter(payment_status=Order.PAYMENT_PAID).aggregate(total=Sum("total_amount"))["total"] or 0
        low_stock = Product.objects.filter(inventory__lte=5, is_active=True).count()
        active_subscriptions = Subscription.objects.filter(status=Subscription.STATUS_ACTIVE).count()

        data = {
            "total_customers": total_customers,
            "total_orders": total_orders,
            "new_orders": new_orders,
            "pending_payments": pending_payments,
            "total_revenue": total_revenue,
            "low_stock_items": low_stock,
            "active_subscriptions": active_subscriptions,
        }
        return Response(data)


class AmazonProductImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AmazonProductImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data["url"]

        try:
            result = fetch_amazon_product_data(url)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)


class AmazonProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AmazonProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data["url"]
        category_id = serializer.validated_data.get("category_id")
        inventory = serializer.validated_data.get("inventory", 10)
        discount_price = serializer.validated_data.get("discount_price")
        is_active = serializer.validated_data.get("is_active", True)

        try:
            data = fetch_amazon_product_data(url)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        category = None
        if category_id:
            category = get_object_or_404(Category, id=category_id)

        product = Product.objects.create(
            title=data["title"],
            slug=data["title"].lower().replace(" ", "-")[:255],
            description=data["description"],
            category=category or Category.objects.first(),
            price=data["price"] or 0,
            discount_price=discount_price,
            inventory=inventory,
            image_url=data["image_url"],
            is_active=is_active,
        )

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class RefreshFeaturedProductsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)

        update_featured_products(days=30, limit=16)
        return Response({"detail": "Featured products refreshed."}, status=status.HTTP_200_OK)


class PaymobCheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymobCheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = get_object_or_404(Order, id=serializer.validated_data["order_id"], user=request.user)
        billing_data = serializer.validated_data["billing_data"]
        integration_id = serializer.validated_data.get("integration_id")

        try:
            result = create_payment_key(order, billing_data, integration_id=integration_id)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)


class PaymobWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        raw_body = request.body.decode("utf-8")
        signature = request.headers.get("X-Callback-Signature", "")
        if not verify_webhook_signature(raw_body, signature):
            return Response({"detail": "Invalid signature."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaymobWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data["data"]
        merchant_order_id = payload.get("order", {}).get("merchant_order_id")
        success = serializer.validated_data["success"]

        if not merchant_order_id:
            return Response({"detail": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=merchant_order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        transaction, _ = PaymentTransaction.objects.get_or_create(
            order=order,
            reference=serializer.validated_data["id"],
            defaults={
                "amount": order.total_amount,
                "status": PaymentTransaction.STATUS_SUCCESS if success else PaymentTransaction.STATUS_FAILED,
                "payload": payload,
            },
        )

        if success:
            order.payment_status = Order.PAYMENT_PAID
            order.status = Order.STATUS_PROCESSING
        else:
            order.payment_status = Order.PAYMENT_FAILED
            order.status = Order.STATUS_FAILED

        order.save()
        transaction.status = PaymentTransaction.STATUS_SUCCESS if success else PaymentTransaction.STATUS_FAILED
        transaction.payload = payload
        transaction.save()

        return Response({"detail": "Webhook processed."}, status=status.HTTP_200_OK)


class SubscriptionPurchaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SubscriptionPurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = get_object_or_404(SubscriptionPlan, id=serializer.validated_data["plan_id"], is_active=True)

        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            status=Subscription.STATUS_PENDING,
            auto_renew=serializer.validated_data["auto_renew"],
        )

        return Response({"subscription_id": subscription.id, "status": subscription.status}, status=status.HTTP_201_CREATED)
