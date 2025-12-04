export default function HeroSection() {
  return (
    <section className="pt-32 pb-16 px-4 sm:px-6 lg:px-8 min-h-[70vh] flex items-center justify-center">
      <div className="max-w-4xl mx-auto text-center">
        <div className="backdrop-blur-2xl bg-white/40 border border-white/50 rounded-3xl p-8 sm:p-16 shadow-xl">
          <h2 className="text-5xl sm:text-6xl md:text-7xl font-bold text-balance mb-6" style={{ color: "#6a329f" }}>
            Elegance Redefined
          </h2>
          <p className="text-lg sm:text-xl text-foreground/80 mb-8 max-w-2xl mx-auto">
            Discover our latest collections crafted with precision and passion. From timeless classics to contemporary
            masterpieces.
          </p>
          <button
            className="px-10 py-4 rounded-full font-bold text-lg transition-all duration-300 hover:scale-105"
            style={{
              background: "linear-gradient(135deg, #f1c232 0%, #ce7e00 100%)",
              color: "white",
            }}
          >
            Shop Now
          </button>
        </div>
      </div>
    </section>
  )
}
