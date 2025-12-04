"use client"

import { useState } from "react"
import { Menu, X } from "lucide-react"

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const navItems = ["New Arrivals", "Clothing", "Accessories", "Sale"]

  return (
    <header className="fixed top-0 left-0 right-0 z-40 backdrop-blur-lg bg-white/30 border-b border-white/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold tracking-widest" style={{ color: "#6a329f" }}>
              LuxeStyle
            </h1>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex gap-8">
            {navItems.map((item) => (
              <a
                key={item}
                href="#"
                className="text-foreground hover:text-[#c90076] transition-colors duration-200 font-medium text-sm tracking-wide"
              >
                {item}
              </a>
            ))}
          </nav>

          {/* Desktop Actions */}
          <div className="hidden md:flex gap-4 items-center">
            <button
              className="px-6 py-2 rounded-full font-semibold transition-all duration-200"
              style={{
                background: "#c90076",
                color: "white",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.opacity = "0.9")}
              onMouseLeave={(e) => (e.currentTarget.style.opacity = "1")}
            >
              Cart
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button className="md:hidden p-2" onClick={() => setIsMenuOpen(!isMenuOpen)} style={{ color: "#6a329f" }}>
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 pb-4 space-y-3">
            {navItems.map((item) => (
              <a
                key={item}
                href="#"
                className="block text-foreground hover:text-[#c90076] transition-colors duration-200 font-medium text-sm"
              >
                {item}
              </a>
            ))}
            <button
              className="w-full px-4 py-2 rounded-full font-semibold transition-all duration-200"
              style={{
                background: "#c90076",
                color: "white",
              }}
            >
              Cart
            </button>
          </div>
        )}
      </div>
    </header>
  )
}
