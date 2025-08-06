"use client"

import type React from "react"
import { useState, useEffect, useCallback } from "react"
import { Link } from "react-router-dom"
import { skillsAPI } from "../../services/api"
import type { Skill, Category } from "../../types"
import { toast } from "react-toastify"
import {
  MagnifyingGlassIcon,
  FunnelIcon,
  StarIcon,
  ClockIcon,
  CurrencyDollarIcon,
  UserIcon,
} from "@heroicons/react/24/outline"

const Skills: React.FC = () => {
  const [skills, setSkills] = useState<Skill[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("")
  const [selectedDifficulty, setSelectedDifficulty] = useState("")
  const [sortBy, setSortBy] = useState("created_at")

  const fetchSkills = useCallback(async () => {
    try {
      setLoading(true)
      const params: any = {}

      if (searchTerm) params.search = searchTerm
      if (selectedCategory) params.category = selectedCategory
      if (selectedDifficulty) params.difficulty_level = selectedDifficulty
      if (sortBy) params.ordering = sortBy

      const response = await skillsAPI.getSkills(params)
      setSkills(response.results || [])
    } catch (error) {
      toast.error("Failed to fetch skills")
    } finally {
      setLoading(false)
    }
  }, [searchTerm, selectedCategory, selectedDifficulty, sortBy])

  const fetchCategories = useCallback(async () => {
    try {
      const response = await skillsAPI.getCategories()
      setCategories(response.results || [])
    } catch (error) {
      console.error("Failed to fetch categories:", error)
    }
  }, [])

  useEffect(() => {
    fetchSkills()
    fetchCategories()
  }, [fetchSkills, fetchCategories])

  useEffect(() => {
    fetchSkills()
  }, [fetchSkills])

  const getDifficultyColor = (level: string | undefined) => {
    if (!level) return "bg-gray-100 text-gray-800"

    switch (level) {
      case "beginner":
        return "bg-green-100 text-green-800"
      case "intermediate":
        return "bg-yellow-100 text-yellow-800"
      case "advanced":
        return "bg-orange-100 text-orange-800"
      case "expert":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const renderStars = (rating: number | undefined) => {
    const safeRating = rating || 0
    return Array.from({ length: 5 }, (_, i) => (
      <StarIcon
        key={i}
        className={`h-4 w-4 ${i < Math.floor(safeRating) ? "text-yellow-400 fill-current" : "text-gray-300"}`}
      />
    ))
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Explore Skills</h1>
        <p className="text-gray-600">Discover and learn new skills from expert instructors</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Search */}
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search skills..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10"
            />
          </div>

          {/* Category Filter */}
          <div className="relative">
            <FunnelIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="input-field pl-10 appearance-none"
            >
              <option value="">All Categories</option>
              {categories.map((category) => (
                <option key={category.id} value={category.name}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>

          {/* Difficulty Filter */}
          <div>
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              className="input-field"
            >
              <option value="">All Levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
              <option value="expert">Expert</option>
            </select>
          </div>

          {/* Sort */}
          <div>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="input-field">
              <option value="created_at">Newest First</option>
              <option value="-created_at">Oldest First</option>
              <option value="rating">Highest Rated</option>
              <option value="points_required">Lowest Points</option>
              <option value="-points_required">Highest Points</option>
            </select>
          </div>
        </div>
      </div>

      {/* Skills Grid */}
      {skills.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {skills.map((skill) => (
            <div key={skill.id} className="card hover:shadow-lg transition-shadow duration-200">
              <div className="card-header">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="card-title text-lg mb-2">
                      <Link to={`/skills/${skill.id}`} className="hover:text-primary-600 transition-colors">
                        {skill.title}
                      </Link>
                    </h3>
                    <span
                      className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(skill.difficulty_level)}`}
                    >
                      {skill.difficulty_level || "Unknown"}
                    </span>
                  </div>
                </div>
              </div>

              <div className="card-content">
                <p className="text-gray-600 text-sm mb-4 line-clamp-3">{skill.description}</p>

                {/* Instructor */}
                <div className="flex items-center mb-4">
                  <div className="h-8 w-8 bg-gray-200 rounded-full flex items-center justify-center mr-3">
                    <UserIcon className="h-4 w-4 text-gray-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {skill.instructor?.first_name && skill.instructor?.last_name
                        ? `${skill.instructor.first_name} ${skill.instructor.last_name}`
                        : "Unknown Instructor"}
                    </p>
                    <div className="flex items-center">
                      {renderStars(skill.rating)}
                      <span className="text-xs text-gray-500 ml-1">({skill.reviews_count || 0})</span>
                    </div>
                  </div>
                </div>

                {/* Skill Details */}
                <div className="space-y-2">
                  <div className="flex items-center text-sm text-gray-600">
                    <ClockIcon className="h-4 w-4 mr-2" />
                    <span>{skill.duration_hours || 0} hours</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <CurrencyDollarIcon className="h-4 w-4 mr-2" />
                    <span>{skill.points_required || 0} points</span>
                  </div>
                </div>
              </div>

              <div className="card-footer">
                <Link to={`/skills/${skill.id}`} className="btn btn-primary w-full">
                  View Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="max-w-md mx-auto">
            <MagnifyingGlassIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No skills found</h3>
            <p className="text-gray-600">Try adjusting your search criteria or browse all categories.</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Skills
