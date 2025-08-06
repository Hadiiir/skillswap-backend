"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../../contexts/AuthContext"
import { skillsAPI } from "../../services/api"
import type { Category } from "../../types"
import { toast } from "react-toastify"
import { ArrowLeftIcon } from "@heroicons/react/24/outline"

interface FormData {
  title: string
  description: string
  category: string
  points_required: number
  duration_hours: number
  difficulty_level: "beginner" | "intermediate" | "advanced"
}

interface FormErrors {
  title?: string
  description?: string
  category?: string
  points_required?: string
  duration_hours?: string
  difficulty_level?: string
}

const CreateSkill: React.FC = () => {
  const navigate = useNavigate()
  const { user, isAuthenticated } = useAuth()
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<FormErrors>({})
  const [formData, setFormData] = useState<FormData>({
    title: "",
    description: "",
    category: "",
    points_required: 10,
    duration_hours: 1,
    difficulty_level: "beginner",
  })

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login")
      return
    }
    fetchCategories()
  }, [isAuthenticated, navigate])

  const fetchCategories = async () => {
    try {
      const response = await skillsAPI.getCategories()
      setCategories(response.results)
    } catch (error) {
      console.error("Failed to fetch categories")
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: name === "points_required" || name === "duration_hours" ? Number.parseInt(value) || 0 : value,
    }))

    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {}

    if (!formData.title.trim()) {
      newErrors.title = "Title is required"
    } else if (formData.title.length < 5) {
      newErrors.title = "Title must be at least 5 characters"
    }

    if (!formData.description.trim()) {
      newErrors.description = "Description is required"
    } else if (formData.description.length < 20) {
      newErrors.description = "Description must be at least 20 characters"
    }

    if (!formData.category) {
      newErrors.category = "Category is required"
    }

    if (formData.points_required < 1) {
      newErrors.points_required = "Points required must be at least 1"
    } else if (formData.points_required > 1000) {
      newErrors.points_required = "Points required cannot exceed 1000"
    }

    if (formData.duration_hours < 0.5) {
      newErrors.duration_hours = "Duration must be at least 0.5 hours"
    } else if (formData.duration_hours > 100) {
      newErrors.duration_hours = "Duration cannot exceed 100 hours"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm()) return

    setLoading(true)
    try {
      const newSkill = await skillsAPI.createSkill(formData)
      toast.success("Skill created successfully!")
      navigate(`/skills/${newSkill.id}`)
    } catch (error: any) {
      const message = error.response?.data?.detail || "Failed to create skill"
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      {/* Back Button */}
      <button
        onClick={() => navigate("/skills")}
        className="flex items-center text-primary-600 hover:text-primary-700 mb-6"
      >
        <ArrowLeftIcon className="h-5 w-5 mr-2" />
        Back to Skills
      </button>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Create New Skill</h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Skill Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              className={`input-field ${errors.title ? "border-red-500" : ""}`}
              placeholder="Enter skill title"
            />
            {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={4}
              className={`input-field ${errors.description ? "border-red-500" : ""}`}
              placeholder="Describe what students will learn in this skill"
            />
            {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description}</p>}
          </div>

          {/* Category and Difficulty */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                Category *
              </label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                className={`input-field ${errors.category ? "border-red-500" : ""}`}
              >
                <option value="">Select a category</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.name}>
                    {category.name}
                  </option>
                ))}
              </select>
              {errors.category && <p className="mt-1 text-sm text-red-600">{errors.category}</p>}
            </div>

            <div>
              <label htmlFor="difficulty_level" className="block text-sm font-medium text-gray-700 mb-2">
                Difficulty Level *
              </label>
              <select
                id="difficulty_level"
                name="difficulty_level"
                value={formData.difficulty_level}
                onChange={handleInputChange}
                className="input-field"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
          </div>

          {/* Points and Duration */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="points_required" className="block text-sm font-medium text-gray-700 mb-2">
                Points Required *
              </label>
              <input
                type="number"
                id="points_required"
                name="points_required"
                value={formData.points_required}
                onChange={handleInputChange}
                min="1"
                max="1000"
                className={`input-field ${errors.points_required ? "border-red-500" : ""}`}
              />
              {errors.points_required && <p className="mt-1 text-sm text-red-600">{errors.points_required}</p>}
            </div>

            <div>
              <label htmlFor="duration_hours" className="block text-sm font-medium text-gray-700 mb-2">
                Duration (hours) *
              </label>
              <input
                type="number"
                id="duration_hours"
                name="duration_hours"
                value={formData.duration_hours}
                onChange={handleInputChange}
                min="0.5"
                max="100"
                step="0.5"
                className={`input-field ${errors.duration_hours ? "border-red-500" : ""}`}
              />
              {errors.duration_hours && <p className="mt-1 text-sm text-red-600">{errors.duration_hours}</p>}
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate("/skills")}
              className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create Skill"}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateSkill
