import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mini Amazon Store",
  description: "E-commerce platform with premium memberships and Paymob checkout.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
