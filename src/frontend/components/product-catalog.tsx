"use client"

import { useState } from "react"
import ProductCard from "./product-card"

const CATEGORIES = {
  jackets: {
    name: "Jackets",
    products: [
      { id: 1, name: "Leather Biker Jacket", price: "$450", image: "/luxury-leather-biker-jacket.jpg" },
      { id: 2, name: "Silk Blazer", price: "$380", image: "/elegant-silk-blazer-jacket.jpg" },
      { id: 3, name: "Cashmere Coat", price: "$620", image: "/luxury-cashmere-coat.png" },
      { id: 4, name: "Denim Jacket", price: "$220", image: "/designer-denim-jacket.jpg" },
    ],
  },
  dresses: {
    name: "Dresses",
    products: [
      { id: 5, name: "Silk Evening Gown", price: "$850", image: "/elegant-silk-evening-gown.jpg" },
      { id: 6, name: "Minimalist Maxi Dress", price: "$420", image: "/minimalist-luxury-maxi-dress.jpg" },
      { id: 7, name: "Cocktail Dress", price: "$550", image: "/luxury-cocktail-dress.jpg" },
      { id: 8, name: "Day Dress", price: "$280", image: "/luxury-minimalist-day-dress.jpg" },
    ],
  },
  jewelry: {
    name: "Jewelry",
    products: [
      { id: 9, name: "Pearl Necklace", price: "$420", image: "/luxury-pearl-necklace.jpg" },
      { id: 10, name: "Diamond Ring", price: "$1200", image: "/luxury-diamond-ring.jpg" },
      { id: 11, name: "Gold Bracelet", price: "$680", image: "/luxury-gold-bracelet.jpg" },
      { id: 12, name: "Emerald Earrings", price: "$890", image: "/luxury-emerald-earrings.jpg" },
    ],
  },
}

export default function ProductCatalog() {
  const [activeCategory, setActiveCategory] = useState("jackets")

  const categories = Object.entries(CATEGORIES)

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Section Title */}
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-balance mb-4" style={{ color: "#6a329f" }}>
            Discover Our Latest Collections
          </h2>
          <p className="text-lg text-foreground/70">Curated selections for the discerning eye</p>
        </div>

        {/* Category Tabs */}
        <div className="flex justify-center gap-4 mb-12 flex-wrap">
          {categories.map(([key, category]) => (
            <button
              key={key}
              onClick={() => setActiveCategory(key)}
              className={`px-6 py-2 rounded-full font-semibold transition-all duration-300 ${
                activeCategory === key
                  ? "text-white shadow-lg scale-105"
                  : "text-foreground hover:text-[#c90076] border border-transparent"
              }`}
              style={{
                background:
                  activeCategory === key ? "linear-gradient(135deg, #c90076 0%, #8e7cc3 100%)" : "transparent",
              }}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {CATEGORIES[activeCategory as keyof typeof CATEGORIES].products.map((product) => (
            <ProductCard key={product.id} {...product} />
          ))}
        </div>
      </div>
    </section>
  )
}
