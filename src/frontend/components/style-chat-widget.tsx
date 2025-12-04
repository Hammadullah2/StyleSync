"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { MessageCircle, X, Send, Upload, Paperclip } from "lucide-react"

interface ChatMessage {
  id: string
  role: "user" | "stylist"
  content: string
  timestamp: Date
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
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSendMessage = () => {
    if (input.trim()) {
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        role: "user",
        content: input,
        timestamp: new Date(),
      }
      setMessages([...messages, userMessage])
      setInput("")

      // Simulate stylist response
      setTimeout(() => {
        const stylistMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          role: "stylist",
          content: generateStyleistResponse(input),
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, stylistMessage])
      }, 800)
    }
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        const dataUrl = event.target?.result as string
        setUploadedImage(dataUrl)

        const userMessage: ChatMessage = {
          id: Date.now().toString(),
          role: "user",
          content: "[Image uploaded for style analysis]",
          timestamp: new Date(),
        }
        setMessages([...messages, userMessage])

        setTimeout(() => {
          const stylistMessage: ChatMessage = {
            id: (Date.now() + 1).toString(),
            role: "stylist",
            content:
              "Love the style! Based on the image, I can see you prefer classic elegance. This piece would pair beautifully with our new collection. Would you like some recommendations?",
            timestamp: new Date(),
          }
          setMessages((prev) => [...prev, stylistMessage])
        }, 1000)
      }
      reader.readAsDataURL(file)
    }
  }

  const generateStyleistResponse = (userInput: string): string => {
    const responses = [
      "That's a wonderful choice! This style complements your taste perfectly.",
      "I have several pieces in our collection that would match what you're looking for.",
      "Your aesthetic is impeccable! Let me suggest some curated options.",
      "I absolutely understand. Our new arrivals section has exactly what you need.",
      "Excellent question! This pairing would create a stunning ensemble.",
    ]
    return responses[Math.floor(Math.random() * responses.length)]
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
        className={`fixed top-0 right-0 h-screen w-210 max-w-full z-50 transition-all duration-300 ease-out ${isOpen ? "translate-x-0 opacity-100" : "translate-x-full opacity-0 pointer-events-none"
          }`}
        style={{
          background: "rgba(255, 255, 255, 0.1)",
          backdropFilter: "blur(30px)",
        }}
      >
        {/* Glassmorphic backdrop container */}
        <div className="h-full w-full flex flex-col border-l border-white/20 shadow-2xl bg-gradient-to-b from-white/10 to-white/5">
          {/* Header */}
          <div
            className="px-6 py-5 text-white font-bold text-xl flex items-center justify-between border-b border-white/20"
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
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-xs px-4 py-3 rounded-2xl text-white text-sm ${message.role === "user" ? "rounded-br-none" : "rounded-bl-none"
                    }`}
                  style={{
                    background:
                      message.role === "user" ? "#c90076" : "linear-gradient(135deg, #6a329f 0%, #8e7cc3 100%)",
                  }}
                >
                  <p>{message.content}</p>
                </div>
              </div>
            ))}
            {uploadedImage && (
              <div className="flex justify-end">
                <img
                  src={uploadedImage || "/placeholder.svg"}
                  alt="uploaded"
                  className="max-w-xs rounded-2xl border-2 border-[#c90076]"
                />
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div
            className="px-5 py-4 border-t border-white/20 space-y-3"
            style={{
              background: "rgba(255, 255, 255, 0.05)",
            }}
          >

            {/* Text Input + Paperclip Upload */}
            <div className="relative w-full">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="What goes well with...?"
                className="w-full px-4 py-3 pr-12 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:border-white/50 transition-all duration-200"
              />

              {/* Paperclip Upload Button */}
              <button
                onClick={() => fileInputRef.current?.click()}
                className="absolute right-3 top-1/2 -translate-y-1/2 group"
              >
                <Paperclip size={20} className="text-white opacity-80 hover:opacity-100" />

                {/* Tooltip */}
                <span className="absolute right-8 top-1/2 -translate-y-1/2 hidden group-hover:block bg-black/70 text-white text-xs px-2 py-1 rounded-md whitespace-nowrap">
                  Upload Image
                </span>
              </button>

              {/* Hidden File Input */}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
              />
            </div>

            {/* Send Button */}
            <div className="flex justify-end mt-2">
              <button
                onClick={handleSendMessage}
                className="p-3 rounded-lg transition-all duration-300 text-white hover:shadow-lg"
                style={{
                  background: "#c90076",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.opacity = "0.9")}
                onMouseLeave={(e) => (e.currentTarget.style.opacity = "1")}
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>

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
