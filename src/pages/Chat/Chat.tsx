"use client"

import type React from "react"
import { useState, useEffect, useRef } from "react"
import { useAuth } from "../../contexts/AuthContext"
import { chatAPI } from "../../services/api"
import type { ChatRoom, ChatMessage } from "../../types"
import { toast } from "react-toastify"
import { PaperAirplaneIcon, UserIcon, AcademicCapIcon } from "@heroicons/react/24/outline"

const Chat: React.FC = () => {
  const { user } = useAuth()
  const [rooms, setRooms] = useState<ChatRoom[]>([])
  const [selectedRoom, setSelectedRoom] = useState<ChatRoom | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [newMessage, setNewMessage] = useState("")
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetchRooms()
  }, [])

  useEffect(() => {
    if (selectedRoom) {
      fetchMessages(selectedRoom.id)
    }
  }, [selectedRoom])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const fetchRooms = async () => {
    try {
      setLoading(true)
      const response = await chatAPI.getRooms()
      setRooms(response.results || [])
      if (response.results && response.results.length > 0) {
        setSelectedRoom(response.results[0])
      }
    } catch (error) {
      toast.error("Failed to fetch chat rooms")
    } finally {
      setLoading(false)
    }
  }

  const fetchMessages = async (roomId: number) => {
    try {
      const response = await chatAPI.getMessages(roomId)
      setMessages(response.results || [])
    } catch (error) {
      toast.error("Failed to fetch messages")
    }
  }

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newMessage.trim() || !selectedRoom || sending) return

    setSending(true)
    try {
      const message = await chatAPI.sendMessage(selectedRoom.id, newMessage.trim())
      setMessages((prev) => [...prev, message])
      setNewMessage("")
    } catch (error) {
      toast.error("Failed to send message")
    } finally {
      setSending(false)
    }
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    if (date.toDateString() === today.toDateString()) {
      return "Today"
    } else if (date.toDateString() === yesterday.toDateString()) {
      return "Yesterday"
    } else {
      return date.toLocaleDateString()
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Please login to access chat</h1>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md overflow-hidden" style={{ height: "600px" }}>
        <div className="flex h-full">
          {/* Sidebar - Chat Rooms */}
          <div className="w-1/3 border-r border-gray-200 flex flex-col">
            <div className="p-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Conversations</h2>
            </div>
            <div className="flex-1 overflow-y-auto">
              {rooms.length > 0 ? (
                <div className="space-y-1 p-2">
                  {rooms.map((room) => (
                    <button
                      key={room.id}
                      onClick={() => setSelectedRoom(room)}
                      className={`w-full text-left p-3 rounded-lg hover:bg-gray-50 ${
                        selectedRoom?.id === room.id ? "bg-primary-50 border-l-4 border-primary-500" : ""
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <div className="h-10 w-10 bg-primary-100 rounded-full flex items-center justify-center">
                          <AcademicCapIcon className="h-5 w-5 text-primary-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {room.skill?.title || "General Chat"}
                          </p>
                          <p className="text-xs text-gray-500 truncate">
                            {room.participants
                              .filter((p) => p.id !== user.id)
                              .map((p) => `${p.first_name} ${p.last_name}`)
                              .join(", ")}
                          </p>
                          {room.last_message && (
                            <p className="text-xs text-gray-400 truncate mt-1">{room.last_message.message}</p>
                          )}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center">
                  <AcademicCapIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No conversations yet</p>
                  <p className="text-sm text-gray-400 mt-2">Enroll in skills to start chatting with instructors</p>
                </div>
              )}
            </div>
          </div>

          {/* Main Chat Area */}
          <div className="flex-1 flex flex-col">
            {selectedRoom ? (
              <>
                {/* Chat Header */}
                <div className="p-4 border-b border-gray-200">
                  <div className="flex items-center space-x-3">
                    <div className="h-10 w-10 bg-primary-100 rounded-full flex items-center justify-center">
                      <AcademicCapIcon className="h-5 w-5 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {selectedRoom.skill?.title || "General Chat"}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {selectedRoom.participants
                          .filter((p) => p.id !== user.id)
                          .map((p) => `${p.first_name} ${p.last_name}`)
                          .join(", ")}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                  {messages.length > 0 ? (
                    <>
                      {messages.map((message, index) => {
                        const isOwnMessage = message.sender && message.sender === user.id
                        const messageTimestamp = message.timestamp || message.created_at
                        const showDate =
                          index === 0 ||
                          formatDate(messageTimestamp) !==
                            formatDate(messages[index - 1].timestamp || messages[index - 1].created_at)

                        return (
                          <div key={message.id}>
                            {showDate && (
                              <div className="text-center my-4">
                                <span className="bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-full">
                                  {formatDate(messageTimestamp)}
                                </span>
                              </div>
                            )}
                            <div className={`flex ${isOwnMessage ? "justify-end" : "justify-start"}`}>
                              <div className={`flex items-end space-x-2 max-w-xs lg:max-w-md`}>
                                {!isOwnMessage && (
                                  <div className="h-8 w-8 bg-gray-200 rounded-full flex items-center justify-center">
                                    <UserIcon className="h-4 w-4 text-gray-600" />
                                  </div>
                                )}
                                <div>
                                  <div
                                    className={`px-4 py-2 rounded-lg ${
                                      isOwnMessage ? "bg-primary-600 text-white" : "bg-gray-100 text-gray-900"
                                    }`}
                                  >
                                    <p className="text-sm">{message.message}</p>
                                  </div>
                                  <p className="text-xs text-gray-500 mt-1 px-2">{formatTime(messageTimestamp)}</p>
                                </div>
                              </div>
                            </div>
                          </div>
                        )
                      })}
                      <div ref={messagesEndRef} />
                    </>
                  ) : (
                    <div className="flex-1 flex items-center justify-center">
                      <div className="text-center">
                        <AcademicCapIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                        <p className="text-gray-500">No messages yet</p>
                        <p className="text-sm text-gray-400">Start the conversation!</p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Message Input */}
                <div className="p-4 border-t border-gray-200">
                  <form onSubmit={sendMessage} className="flex space-x-3">
                    <input
                      type="text"
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      placeholder="Type your message..."
                      className="flex-1 input-field"
                      disabled={sending}
                    />
                    <button
                      type="submit"
                      disabled={!newMessage.trim() || sending}
                      className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {sending ? (
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      ) : (
                        <PaperAirplaneIcon className="h-5 w-5" />
                      )}
                    </button>
                  </form>
                </div>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center">
                  <AcademicCapIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Select a conversation</h3>
                  <p className="text-gray-600">Choose a chat room to start messaging</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Chat
