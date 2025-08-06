"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { useAuth } from "../../contexts/AuthContext"
import { pointsAPI } from "../../services/api"
import type { Order } from "../../types"
import { toast } from "react-toastify"
import {
  AcademicCapIcon,
  ClockIcon,
  UserIcon,
  StarIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline"

const Orders: React.FC = () => {
  const { user } = useAuth()
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>("all")

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    try {
      setLoading(true)
      const response = await pointsAPI.getOrders()
      setOrders(response.results)
    } catch (error) {
      toast.error("Failed to fetch orders")
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-green-100 text-green-800"
      case "in_progress":
        return "bg-blue-100 text-blue-800"
      case "confirmed":
        return "bg-purple-100 text-purple-800"
      case "pending":
        return "bg-yellow-100 text-yellow-800"
      case "cancelled":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />
      case "in_progress":
        return <ClockIcon className="h-5 w-5 text-blue-600" />
      case "confirmed":
        return <CheckCircleIcon className="h-5 w-5 text-purple-600" />
      case "pending":
        return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-600" />
      case "cancelled":
        return <XCircleIcon className="h-5 w-5 text-red-600" />
      default:
        return <ClockIcon className="h-5 w-5 text-gray-600" />
    }
  }

  const filteredOrders = orders.filter((order) => {
    if (filter === "all") return true
    return order.status === filter
  })

  const statusCounts = {
    all: orders.length,
    pending: orders.filter((o) => o.status === "pending").length,
    confirmed: orders.filter((o) => o.status === "confirmed").length,
    in_progress: orders.filter((o) => o.status === "in_progress").length,
    completed: orders.filter((o) => o.status === "completed").length,
    cancelled: orders.filter((o) => o.status === "cancelled").length,
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">My Learning Journey</h1>
        <p className="text-gray-600">Track your enrolled skills and learning progress</p>
      </div>

      {/* Filter Tabs */}
      <div className="bg-white rounded-lg shadow-md mb-8">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6" aria-label="Tabs">
            {[
              { key: "all", label: "All Orders", count: statusCounts.all },
              { key: "pending", label: "Pending", count: statusCounts.pending },
              { key: "confirmed", label: "Confirmed", count: statusCounts.confirmed },
              { key: "in_progress", label: "In Progress", count: statusCounts.in_progress },
              { key: "completed", label: "Completed", count: statusCounts.completed },
              { key: "cancelled", label: "Cancelled", count: statusCounts.cancelled },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setFilter(tab.key)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  filter === tab.key
                    ? "border-primary-500 text-primary-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                {tab.label}
                {tab.count > 0 && (
                  <span
                    className={`ml-2 py-0.5 px-2 rounded-full text-xs ${
                      filter === tab.key ? "bg-primary-100 text-primary-600" : "bg-gray-100 text-gray-600"
                    }`}
                  >
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Orders List */}
      {filteredOrders.length > 0 ? (
        <div className="space-y-6">
          {filteredOrders.map((order) => (
            <div key={order.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      {getStatusIcon(order.status)}
                      <h3 className="text-xl font-semibold text-gray-900 ml-2">{order.skill.title}</h3>
                    </div>
                    <p className="text-gray-600 mb-3 line-clamp-2">{order.skill.description}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <div className="flex items-center">
                        <UserIcon className="h-4 w-4 mr-1" />
                        {order.skill.instructor?.first_name || "Unknown"}{" "}
                        {order.skill.instructor?.last_name || "Instructor"}
                      </div>
                      <div className="flex items-center">
                        <ClockIcon className="h-4 w-4 mr-1" />
                        {order.skill.duration_hours}h
                      </div>
                      <div className="flex items-center">
                        <StarIcon className="h-4 w-4 text-yellow-400 mr-1" />
                        {(order.skill.rating || 0).toFixed(1)}
                      </div>
                    </div>
                  </div>
                  <div className="text-right ml-6">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                      {order.status.replace("_", " ")}
                    </span>
                    <div className="mt-2 text-sm text-gray-500">
                      Enrolled: {new Date(order.created_at).toLocaleDateString()}
                    </div>
                    <div className="mt-1 text-lg font-semibold text-primary-600">{order.points_spent} points</div>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                  <div className="flex items-center space-x-4">
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        order.skill.difficulty_level === "beginner"
                          ? "bg-green-100 text-green-800"
                          : order.skill.difficulty_level === "intermediate"
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-red-100 text-red-800"
                      }`}
                    >
                      {order.skill.difficulty_level}
                    </span>
                    <span className="text-sm text-gray-500">{order.skill.category}</span>
                  </div>
                  <div className="flex space-x-3">
                    <Link
                      to={`/skills/${order.skill.id}`}
                      className="px-4 py-2 text-sm font-medium text-primary-600 bg-primary-50 rounded-lg hover:bg-primary-100"
                    >
                      View Skill
                    </Link>
                    {order.status === "confirmed" || order.status === "in_progress" ? (
                      <Link
                        to={`/chat?skill=${order.skill.id}`}
                        className="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700"
                      >
                        Start Learning
                      </Link>
                    ) : null}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <AcademicCapIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {filter === "all" ? "No orders yet" : `No ${filter.replace("_", " ")} orders`}
          </h3>
          <p className="text-gray-600 mb-6">
            {filter === "all"
              ? "Start your learning journey by enrolling in skills"
              : `You don't have any ${filter.replace("_", " ")} orders at the moment`}
          </p>
          <Link to="/skills" className="btn-primary">
            Browse Skills
          </Link>
        </div>
      )}
    </div>
  )
}

export default Orders
