import { useEffect, useState } from "react";

interface DashboardMetrics {
  total_customers: number;
  total_orders: number;
  new_orders: number;
  pending_payments: number;
  total_revenue: number;
  low_stock_items: number;
  active_subscriptions: number;
}

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/dashboard/metrics/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setMetrics(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 text-slate-900">
        <div className="mx-auto flex min-h-screen max-w-6xl flex-col items-center justify-center px-6 py-12">
          <div className="w-full rounded-3xl border border-slate-200 bg-white p-10 shadow-lg shadow-slate-200/40">
            <h1 className="text-4xl font-semibold text-slate-900">Loading Dashboard...</h1>
          </div>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-slate-50 text-slate-900">
        <div className="mx-auto flex min-h-screen max-w-6xl flex-col items-center justify-center px-6 py-12">
          <div className="w-full rounded-3xl border border-slate-200 bg-white p-10 shadow-lg shadow-slate-200/40">
            <h1 className="text-4xl font-semibold text-slate-900">Error</h1>
            <p className="mt-4 text-slate-600">{error}</p>
            <a href="/" className="mt-6 inline-block rounded-2xl bg-sky-600 px-6 py-4 text-center text-white shadow-lg shadow-sky-600/10 transition hover:bg-sky-500">
              Back to Home
            </a>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <h1 className="text-4xl font-semibold text-slate-900 mb-8">Store Dashboard</h1>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/40">
            <h3 className="text-lg font-medium text-slate-600">Total Customers</h3>
            <p className="text-3xl font-bold text-slate-900">{metrics?.total_customers}</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/40">
            <h3 className="text-lg font-medium text-slate-600">Total Orders</h3>
            <p className="text-3xl font-bold text-slate-900">{metrics?.total_orders}</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/40">
            <h3 className="text-lg font-medium text-slate-600">New Orders</h3>
            <p className="text-3xl font-bold text-slate-900">{metrics?.new_orders}</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/40">
            <h3 className="text-lg font-medium text-slate-600">Pending Payments</h3>
            <p className="text-3xl font-bold text-slate-900">{metrics?.pending_payments}</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/40">
            <h3 className="text-lg font-medium text-slate-600">Total Revenue</h3>
            <p className="text-3xl font-bold text-slate-900">${metrics?.total_revenue}</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/40">
            <h3 className="text-lg font-medium text-slate-600">Low Stock Items</h3>
            <p className="text-3xl font-bold text-slate-900">{metrics?.low_stock_items}</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/40">
            <h3 className="text-lg font-medium text-slate-600">Active Subscriptions</h3>
            <p className="text-3xl font-bold text-slate-900">{metrics?.active_subscriptions}</p>
          </div>
        </div>

        <div className="mt-10">
          <a href="/" className="inline-block rounded-2xl bg-sky-600 px-6 py-4 text-center text-white shadow-lg shadow-sky-600/10 transition hover:bg-sky-500">
            Back to Home
          </a>
        </div>
      </div>
    </main>
  );
}