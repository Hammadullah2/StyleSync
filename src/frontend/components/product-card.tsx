"use client"

export default function ProductCard({ name, price, image }: { name: string; price: string; image: string }) {
  return (
    <div className="group">
      <div className="backdrop-blur-xl bg-white/30 border border-white/40 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-105 h-full flex flex-col">
        {/* Product Image */}
        <div className="relative overflow-hidden h-80 bg-gradient-to-br from-[#f1c232]/10 to-[#c90076]/10">
          <img
            src={image || "/placeholder.svg"}
            alt={name}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        </div>

        {/* Product Info */}
        <div className="p-6 flex flex-col flex-grow">
          <h3 className="text-lg font-semibold text-foreground mb-2 group-hover:text-[#c90076] transition-colors duration-200">
            {name}
          </h3>
          <p className="text-2xl font-bold mb-4 flex-grow" style={{ color: "#ce7e00" }}>
            {price}
          </p>

          {/* Action Buttons */}
          <div className="flex gap-3 flex-col sm:flex-row">
            <button
              className="flex-1 py-3 rounded-lg font-semibold transition-all duration-300 text-white"
              style={{
                background: "#c90076",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.opacity = "0.9")}
              onMouseLeave={(e) => (e.currentTarget.style.opacity = "1")}
            >
              Add to Cart
            </button>
            <button
              className="flex-1 py-3 rounded-lg font-semibold transition-all duration-300 border-2"
              style={{
                borderColor: "#6a329f",
                color: "#6a329f",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "#6a329f"
                e.currentTarget.style.color = "white"
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "transparent"
                e.currentTarget.style.color = "#6a329f"
              }}
            >
              Quick View
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
