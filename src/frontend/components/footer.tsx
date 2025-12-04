export default function Footer() {
  return (
    <footer className="bg-white/10 backdrop-blur-lg border-t border-white/30 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <h3 className="text-xl font-bold mb-4" style={{ color: "#6a329f" }}>
              LuxeStyle
            </h3>
            <p className="text-foreground/70 text-sm">
              Discover timeless elegance and contemporary fashion for the modern luxury enthusiast.
            </p>
          </div>

          {/* Shop */}
          <div>
            <h4 className="font-semibold mb-4">Shop</h4>
            <ul className="space-y-2 text-sm text-foreground/70">
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  New Arrivals
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Clothing
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Accessories
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Sale
                </a>
              </li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h4 className="font-semibold mb-4">Customer Service</h4>
            <ul className="space-y-2 text-sm text-foreground/70">
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Contact Us
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Shipping Info
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Returns
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  FAQ
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-sm text-foreground/70">
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-[#c90076] transition-colors">
                  Sustainability
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-white/20 pt-8 text-center text-sm text-foreground/60">
          <p>&copy; 2025 LuxeStyle. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
