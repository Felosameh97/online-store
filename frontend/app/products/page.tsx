import { useEffect, useState } from "react";
import Link from "next/link";

interface Product {
  id: number;
  title: string;
  slug: string;
  description: string;
  category: {
    id: number;
    name: string;
    slug: string;
    description: string;
  };
  price: number;
  discount_price: number | null;
  inventory: number;
  is_active: boolean;
  is_featured: boolean;
  featured_rank: number | null;
  image_url: string | null;
  effective_price: number;
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/products/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setProducts(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 text-slate-900">
        <div className="mx-auto flex min-h-screen max-w-6xl flex-col items-center justify-center px-6 py-12">
          <div className="w-full rounded-3xl border border-slate-200 bg-white p-10 shadow-lg shadow-slate-200/40">
            <h1 className="text-4xl font-semibold text-slate-900">Loading Products...</h1>
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
        <h1 className="text-4xl font-semibold text-slate-900 mb-8">Products</h1>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {products.map((product) => (
            <div key={product.id} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/40">
              {product.image_url && (
                <img
                  src={product.image_url}
                  alt={product.title}
                  className="w-full h-48 object-cover rounded-2xl mb-4"
                />
              )}
              <h3 className="text-xl font-semibold text-slate-900 mb-2">{product.title}</h3>
              <p className="text-slate-600 mb-4 line-clamp-3">{product.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold text-slate-900">${product.effective_price}</span>
                {product.discount_price && (
                  <span className="text-sm text-slate-500 line-through">${product.price}</span>
                )}
              </div>
              <p className="text-sm text-slate-600 mt-2">Category: {product.category.name}</p>
              <p className="text-sm text-slate-600">Stock: {product.inventory}</p>
              {product.is_featured && (
                <span className="inline-block bg-sky-100 text-sky-800 text-xs px-2 py-1 rounded-full mt-2">
                  Featured
                </span>
              )}
            </div>
          ))}
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