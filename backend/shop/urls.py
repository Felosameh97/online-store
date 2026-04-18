from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/best-sellers/", views.BestSellerProductsView.as_view(), name="best-seller-products"),

    path("subscriptions/plans/", views.SubscriptionPlanListView.as_view(), name="subscription-plan-list"),
    path("subscriptions/purchase/", views.SubscriptionPurchaseView.as_view(), name="subscription-purchase"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("payments/paymob/", views.PaymobCheckoutView.as_view(), name="paymob-checkout"),
    path("payments/webhook/", views.PaymobWebhookView.as_view(), name="paymob-webhook"),

    path("dashboard/metrics/", views.StoreDashboardView.as_view(), name="store-dashboard"),
    path("automation/amazon-import/", views.AmazonProductImportView.as_view(), name="amazon-import"),
    path("automation/amazon-create/", views.AmazonProductCreateView.as_view(), name="amazon-create"),
    path("automation/refresh-featured/", views.RefreshFeaturedProductsView.as_view(), name="refresh-featured-products"),
]
