"use client"

import type React from "react"
import { useState, useEffect, useCallback } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useAuth } from "../../contexts/AuthContext"
import { apiService } from "../../services/api"
import type { Skill } from "../../types"
import { toast } from "react-toastify"

const SkillDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [skill, setSkill] = useState<Skill | null>(null)
  const [loading, setLoading] = useState(true)
  const [ordering, setOrdering] = useState(false)

  const fetchSkill = useCallback(async () => {
    if (!id) return

    try {
      const data = await apiService.getSkill(Number.parseInt(id))
      setSkill(data)
    } catch (error) {
      console.error("Error fetching skill:", error)
      toast.error("Error loading skill details")
      navigate("/skills")
    } finally {
      setLoading(false)
    }
  }, [id, navigate])

  useEffect(() => {
    fetchSkill()
  }, [fetchSkill])

  const handleOrder = async () => {
    if (!skill || !user) return

    const userPoints = user.points || user.points_balance || 0
    const skillPrice = skill.price || skill.points_required || 0

    if (userPoints < skillPrice) {
      toast.error("Insufficient points to order this skill")
      return
    }

    setOrdering(true)
    try {
      await apiService.createOrder({
        skill: skill.id,
        message: "New skill order",
      })
      toast.success("Your order has been sent successfully!")
      navigate("/orders")
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Error sending order")
    } finally {
      setOrdering(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading skill details...</p>
        </div>
      </div>
    )
  }

  if (!skill) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Skill not found</h2>
          <p className="mt-2 text-gray-600">The requested skill was not found</p>
          <button
            onClick={() => navigate("/skills")}
            className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Back to Skills
          </button>
        </div>
      </div>
    )
  }

  const isOwner = user?.id === skill.provider
  const userPoints = user?.points || user?.points_balance || 0
  const skillPrice = skill.price || skill.points_required || 0

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h1 className="text-3xl font-bold text-gray-900">{skill.title}</h1>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">By {skill.provider_name || `User ${skill.provider}`}</p>
          </div>
          <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
            <dl className="sm:divide-y sm:divide-gray-200">
              <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt className="text-sm font-medium text-gray-500">Description</dt>
                <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{skill.description}</dd>
              </div>
              <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt className="text-sm font-medium text-gray-500">Category</dt>
                <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{skill.category}</dd>
              </div>
              <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt className="text-sm font-medium text-gray-500">Price</dt>
                <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{skillPrice} points</dd>
              </div>
              <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt className="text-sm font-medium text-gray-500">Expected Duration</dt>
                <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  {skill.duration || skill.duration_hours || 0} hours
                </dd>
              </div>
              <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt className="text-sm font-medium text-gray-500">Requirements</dt>
                <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  {skill.requirements || "No special requirements"}
                </dd>
              </div>
              <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt className="text-sm font-medium text-gray-500">Created Date</dt>
                <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  {new Date(skill.created_at).toLocaleDateString()}
                </dd>
              </div>
            </dl>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex justify-center space-x-4">
          <button
            onClick={() => navigate("/skills")}
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Back to Skills
          </button>

          {!isOwner && user && (
            <button
              onClick={handleOrder}
              disabled={ordering || userPoints < skillPrice}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {ordering ? "Sending..." : userPoints < skillPrice ? "Insufficient Balance" : "Order Skill"}
            </button>
          )}

          {isOwner && (
            <button
              onClick={() => navigate(`/skills/${skill.id}/edit`)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
            >
              Edit Skill
            </button>
          )}
        </div>

        {/* User Points Info */}
        {user && !isOwner && (
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-600">
              Current Balance: <span className="font-semibold">{userPoints} points</span>
            </p>
            {userPoints < skillPrice && (
              <p className="text-sm text-red-600 mt-1">You need {skillPrice - userPoints} more points</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default SkillDetail
