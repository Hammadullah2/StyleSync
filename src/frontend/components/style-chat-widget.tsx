"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { MessageCircle, X, Send } from "lucide-react"

interface ChatMessage {
  id: string
  role: "user" | "stylist"
  content: string
  timestamp: Date
  items?: any[]
}

interface StyleChatWidgetProps {
  isOpen: boolean
  onToggle: (open: boolean) => void
}

export default function StyleChatWidget({ isOpen, onToggle }: StyleChatWidgetProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      role: "stylist",
      content: "Welcome to LuxeStyle! I'm your personal stylist. How can I help you find the perfect piece today?",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [selectedItem, setSelectedItem] = useState<any>(null)

  // Helper to format S3 URL
  const getImageUrl = (s3_uri: string) => {
    if (!s3_uri) return "/placeholder.svg"
    if (s3_uri.startsWith('http')) return s3_uri
    if (s3_uri.startsWith('s3://')) {
      const clean = s3_uri.replace('s3://', '')
      const bucket = clean.split('/')[0]
      const key = clean.split('/').slice(1).join('/')
      return `https://${bucket}.s3.amazonaws.com/${key}`
    }
    return s3_uri
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSendMessage = async () => {
    const trimmed = input.trim()
    if (!trimmed) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: trimmed,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: trimmed }),
      })

      if (!res.ok) throw new Error(`HTTP ${res.status}`)

      const data = await res.json()

      const stylistMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "stylist",
        content: data?.response || "Sorry, I couldn't fetch a reply right now.",
        timestamp: new Date(),
        items: data?.recommended_items || []
      }

      setMessages((prev) => [...prev, stylistMessage])
    } catch (err) {
      console.error(err)
      const errorMsg: ChatMessage = {
        id: (Date.now() + 2).toString(),
        role: "stylist",
        content: "Sorry, I'm having trouble reaching the server right now.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMsg])
    }
  }

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={() => onToggle(!isOpen)}
        className="fixed bottom-6 right-6 z-40 p-4 rounded-full shadow-2xl transition-all duration-300 hover:scale-110 text-white"
        style={{
          background: `linear-gradient(135deg, #c90076 0%, #6a329f 100%)`,
        }}
      >
        {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
      </button>

      <div
        className={`fixed top-0 right-0 h-screen w-96 max-w-full z-50 transition-all duration-300 ease-out ${isOpen ? "translate-x-0 opacity-100" : "translate-x-full opacity-0 pointer-events-none"
          }`}
        style={{
          background: "rgba(20, 20, 20, 0.95)", // Much darker, less transparent
          backdropFilter: "blur(10px)",
          boxShadow: "-5px 0 25px rgba(0,0,0,0.5)"
        }}
      >
        <div className="h-full w-full flex flex-col border-l border-white/10">
          {/* Header */}
          <div
            className="px-6 py-5 text-white font-bold text-xl flex items-center justify-between border-b border-white/10"
            style={{
              background: `linear-gradient(135deg, #c90076 0%, #8e7cc3 100%)`,
            }}
          >
            <span>Ask a Stylist</span>
            <button
              onClick={() => onToggle(false)}
              className="p-1 hover:bg-white/20 rounded-lg transition-all duration-200"
            >
              <X size={20} />
            </button>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-5 space-y-6">
            {messages.map((message) => (
              <div key={message.id} className={`flex flex-col ${message.role === "user" ? "items-end" : "items-start"}`}>
                <div
                  className={`max-w-[85%] px-4 py-3 rounded-2xl text-white text-sm ${message.role === "user" ? "rounded-br-none" : "rounded-bl-none"
                    }`}
                  style={{
                    background:
                      message.role === "user" ? "#c90076" : "#2a2a2a",
                    border: message.role === "stylist" ? "1px solid rgba(255,255,255,0.1)" : "none"
                  }}
                >
                  <p className="leading-relaxed">{message.content}</p>
                </div>

                {/* Embedded Items */}
                {message.items && message.items.length > 0 && (
                  <div className="mt-3 grid grid-cols-1 gap-2 w-full max-w-[85%]">
                    {message.items.map((item: any, idx: number) => (
                      <div
                        key={idx}
                        className="bg-white/10 p-2 rounded-lg flex gap-3 items-center cursor-pointer hover:bg-white/20 transition-colors"
                        onClick={() => setSelectedItem(item)}
                      >
                        {/* Thumbnail */}
                        <div className="w-16 h-16 bg-black/30 rounded-md overflow-hidden flex-shrink-0">
                          {item.s3_uri && (
                            <img
                              src={getImageUrl(item.s3_uri)}
                              alt="product"
                              className="w-full h-full object-cover"
                            />
                          )}
                        </div>
                        {/* Info */}
                        <div className="flex-1 min-w-0">
                          <div className="text-white text-xs font-bold truncate">{item.productDisplayName || "Stylish Item"}</div>
                          <div className="text-white/60 text-[10px]">{item.metadata?.season} • {item.metadata?.baseColour}</div>
                          <div className="text-[#c90076] text-[10px] font-semibold mt-1">
                            Click to view details
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div
            className="px-5 py-4 border-t border-white/10 space-y-3 bg-[#1a1a1a]"
          >
            <div className="relative w-full">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="What goes well with...?"
                className="w-full px-4 py-3 pr-12 rounded-lg bg-[#2a2a2a] border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-[#c90076] transition-all duration-200"
              />
            </div>

            <div className="flex justify-end">
              <button
                onClick={handleSendMessage}
                className="p-3 rounded-lg transition-all duration-300 text-white hover:shadow-lg bg-[#c90076] hover:opacity-90"
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Product Detail Modal */}
      {selectedItem && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-[#1a1a1a] rounded-2xl max-w-md w-full overflow-hidden shadow-2xl border border-white/10 relative">
            <button
              onClick={() => setSelectedItem(null)}
              className="absolute top-4 right-4 p-2 bg-black/50 rounded-full text-white hover:bg-black/70 transition-colors z-10"
            >
              <X size={20} />
            </button>

            <div className="aspect-square w-full bg-black/50 relative">
              <img
                src={getImageUrl(selectedItem.s3_uri)}
                alt={selectedItem.productDisplayName}
                className="w-full h-full object-contain"
              />
            </div>

            <div className="p-6">
              <h3 className="text-xl font-bold text-white mb-2">{selectedItem.productDisplayName}</h3>
              <div className="flex flex-wrap gap-2 mb-4">
                {selectedItem.metadata?.season && (
                  <span className="px-2 py-1 rounded-md bg-white/10 text-xs text-white/80">
                    {selectedItem.metadata.season}
                  </span>
                )}
                {selectedItem.metadata?.baseColour && (
                  <span className="px-2 py-1 rounded-md bg-white/10 text-xs text-white/80">
                    {selectedItem.metadata.baseColour}
                  </span>
                )}
                {selectedItem.metadata?.usage && (
                  <span className="px-2 py-1 rounded-md bg-white/10 text-xs text-white/80">
                    {selectedItem.metadata.usage}
                  </span>
                )}
              </div>

              <button
                className="w-full py-3 rounded-xl bg-gradient-to-r from-[#c90076] to-[#6a329f] text-white font-semibold shadow-lg hover:opacity-90 transition-opacity"
                onClick={() => window.open(getImageUrl(selectedItem.s3_uri), '_blank')}
              >
                View Full Image Source
              </button>
            </div>
          </div>
        </div>
      )}

      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/20 backdrop-blur-sm transition-all duration-300"
          onClick={() => onToggle(false)}
          style={{
            animation: "fadeIn 0.3s ease-out",
          }}
        />
      )}
    </>
  )
}
