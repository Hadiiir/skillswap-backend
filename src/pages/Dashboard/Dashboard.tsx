"use client"

import type React from "react"
import { useState, useEffect, useCallback } from "react"
import { Link } from "react-router-dom"
import { useAuth } from "../../contexts/AuthContext"
import { apiService } from "../../services/api"
import type { Skill, Order, ApiResponse } from "../../types"
import { toast } from "react-toastify"

interface DashboardData {
  skills: Skill[]
  orders: Order[]
  stats: {
    total_skills: number
    total_orders: number
    total_points: number
    pending_orders: number
  }
}

const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)

  const fetchDashboardData = useCallback(async () => {
    try {
      const [skillsResponse, ordersResponse, profile] = await Promise.all([
        apiService.getSkills() as Promise<ApiResponse<Skill>>,
        apiService.getOrders() as Promise<ApiResponse<Order>>,
        apiService.getProfile(),
      ])

      const userSkills = skillsResponse.results.filter((skill: Skill) => skill.provider === user?.id)
      const userOrders = ordersResponse.results.filter(
        (order: Order) => order.buyer === user?.id || order.skill?.provider === user?.id,
      )

      setData({
        skills: userSkills,
        orders: userOrders,
        stats: {
          total_skills: userSkills.length,
          total_orders: userOrders.length,
          total_points: profile.points_balance || profile.points || 0,
          pending_orders: userOrders.filter((order: Order) => order.status === "pending").length,
        },
      })
    } catch (error) {
      console.error("Error fetching dashboard data:", error)
      toast.error("Error loading dashboard data")
    } finally {
      setLoading(false)
    }
  }, [user?.id])

  useEffect(() => {
    fetchDashboardData()
  }, [fetchDashboardData])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome, {user?.first_name} {user?.last_name}
          </h1>
          <p className="mt-2 text-gray-600">Here's an overview of your activity on the platform</p>
        </div>

        {/* Stats */}
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-bold">S</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">My Skills</dt>
                      <dd className="text-lg font-medium text-gray-900">{data?.stats.total_skills || 0}</dd>
                    </dl>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-5 py-3">
                <div className="text-sm">
                  <Link to="/create-skill" className="font-medium text-blue-600 hover:text-blue-500">
                    Add New Skill
                  </Link>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-bold">O</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Orders</dt>
                      <dd className="text-lg font-medium text-gray-900">{data?.stats.total_orders || 0}</dd>
                    </dl>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-5 py-3">
                <div className="text-sm">
                  <Link to="/orders" className="font-medium text-green-600 hover:text-green-500">
                    View All Orders
                  </Link>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-yellow-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-bold">P</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Points</dt>
                      <dd className="text-lg font-medium text-gray-900">{data?.stats.total_points || 0}</dd>
                    </dl>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-5 py-3">
                <div className="text-sm">
                  <Link to="/points" className="font-medium text-yellow-600 hover:text-yellow-500">
                    Manage Points
                  </Link>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-bold">!</span>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Pending Orders</dt>
                      <dd className="text-lg font-medium text-gray-900">{data?.stats.pending_orders || 0}</dd>
                    </dl>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-5 py-3">
                <div className="text-sm">
                  <Link to="/orders?status=pending" className="font-medium text-red-600 hover:text-red-500">
                    Review Orders
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Skills */}
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">My Recent Skills</h2>
              {data?.skills && data.skills.length > 0 ? (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {data.skills.slice(0, 6).map((skill) => (
                    <div key={skill.id} className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-sm font-medium text-gray-900">{skill.title}</h3>
                      <p className="mt-1 text-sm text-gray-500 line-clamp-2">{skill.description}</p>
                      <div className="mt-2 flex items-center justify-between">
                        <span className="text-sm text-blue-600">
                          {skill.price || skill.points_required || 0} points
                        </span>
                        <Link to={`/skills/${skill.id}`} className="text-sm text-blue-600 hover:text-blue-500">
                          View
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-6">
                  <p className="text-gray-500">You haven't added any skills yet</p>
                  <Link
                    to="/create-skill"
                    className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                  >
                    Add New Skill
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Recent Orders */}
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Orders</h2>
              {data?.orders && data.orders.length > 0 ? (
                <div className="overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Skill
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Date
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {data.orders.slice(0, 5).map((order) => (
                        <tr key={order.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {order.skill?.title || "Deleted skill"}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span
                              className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                order.status === "completed"
                                  ? "bg-green-100 text-green-800"
                                  : order.status === "pending"
                                    ? "bg-yellow-100 text-yellow-800"
                                    : "bg-red-100 text-red-800"
                              }`}
                            >
                              {order.status === "completed"
                                ? "Completed"
                                : order.status === "pending"
                                  ? "Pending"
                                  : "Cancelled"}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {new Date(order.created_at).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <Link to={`/orders/${order.id}`} className="text-blue-600 hover:text-blue-500">
                              View
                            </Link>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-center py-6">
                  <p className="text-gray-500">No orders yet</p>
                  <Link
                    to="/skills"
                    className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                  >
                    Browse Skills
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
