export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
}

export interface Product {
  id: number;
  title: string;
  slug: string;
  description: string;
  category: Category;
  price: number;
  discount_price: number | null;
  inventory: number;
  is_active: boolean;
  is_featured: boolean;
  featured_rank: number | null;
  image_url: string | null;
  effective_price: number;
}

export interface DashboardMetrics {
  total_customers: number;
  total_orders: number;
  new_orders: number;
  pending_payments: number;
  total_revenue: number;
  low_stock_items: number;
  active_subscriptions: number;
}
