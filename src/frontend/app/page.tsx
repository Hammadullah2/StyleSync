"use client"

import { useState } from "react"
import Header from "@/components/header"
import HeroSection from "@/components/hero-section"
import ProductCatalog from "@/components/product-catalog"
import StyleChatWidget from "@/components/style-chat-widget"
import Footer from "@/components/footer"

export default function Home() {
  const [isChatOpen, setIsChatOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#faf9f7] via-[#f5f3f0] to-[#ede8e3]">
      <div className={isChatOpen ? "overflow-hidden" : ""}>
        <Header />
        <HeroSection />
        <ProductCatalog />
        <Footer />
      </div>

      <StyleChatWidget isOpen={isChatOpen} onToggle={setIsChatOpen} />
    </div>
  )
}
