import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col items-center justify-center px-6 py-12">
        <div className="w-full rounded-3xl border border-slate-200 bg-white p-10 shadow-lg shadow-slate-200/40">
          <h1 className="text-4xl font-semibold text-slate-900">Mini Amazon Dashboard</h1>
          <p className="mt-4 max-w-2xl text-slate-600">
            A modern e-commerce frontend for the store, with product discovery, premium subscriptions, and Paymob checkout integration.
          </p>

          <div className="mt-10 grid gap-4 sm:grid-cols-2">
            <Link href="/products" className="rounded-2xl bg-slate-900 px-6 py-4 text-center text-white shadow-lg shadow-slate-900/10 transition hover:bg-slate-700">
              Browse Products
            </Link>
            <Link href="/dashboard" className="rounded-2xl bg-sky-600 px-6 py-4 text-center text-white shadow-lg shadow-sky-600/10 transition hover:bg-sky-500">
              Admin Dashboard
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
