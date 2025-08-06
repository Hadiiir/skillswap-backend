"use client"

import type React from "react"
import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import type { User, AuthContextType, LoginResponse, RegisterResponse } from "../types"
import { authAPI } from "../services/api"
import api from "../services/api"
import { toast } from "react-toastify"

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem("token")
      if (token) {
        api.setToken(token)
        try {
          const userData = await authAPI.getProfile()
          setUser(userData)
        } catch (error) {
          console.error("Failed to get user profile:", error)
          localStorage.removeItem("token")
          api.setToken(null)
        }
      }
      setLoading(false)
    }

    initAuth()
  }, [])

  const login = async (credentials: { email: string; password: string }) => {
    try {
      setLoading(true)
      const response: LoginResponse = await authAPI.login(credentials)

      // Handle different response structures
      let token: string
      let userData: User

      if (response.access) {
        // JWT token response
        token = response.access
        userData = response.user || (await authAPI.getProfile())
      } else if (response.token) {
        // Token auth response
        token = response.token
        userData = response.user || (await authAPI.getProfile())
      } else if (response.key) {
        // Key auth response
        token = response.key
        userData = response.user || (await authAPI.getProfile())
      } else if (response.auth_token) {
        // Auth token response
        token = response.auth_token
        userData = response.user || (await authAPI.getProfile())
      } else {
        throw new Error("Invalid response format")
      }

      api.setToken(token)
      setUser(userData)
      toast.success("تم تسجيل الدخول بنجاح!")

      return { success: true }
    } catch (error: any) {
      console.error("Login error:", error)
      const errorMessage = error.message || "فشل في تسجيل الدخول"
      toast.error(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const register = async (userData: {
    first_name: string
    last_name: string
    email: string
    password: string
  }) => {
    try {
      setLoading(true)
      const response: RegisterResponse = await authAPI.register(userData)

      // Handle different response structures
      let token: string | null = null
      let newUser: User | null = null

      if (response.access) {
        // JWT token response
        token = response.access
        newUser = response.user || (await authAPI.getProfile())
      } else if (response.token) {
        // Token auth response
        token = response.token
        newUser = response.user || (await authAPI.getProfile())
      } else if (response.key) {
        // Key auth response
        token = response.key
        newUser = response.user || (await authAPI.getProfile())
      } else if (response.auth_token) {
        // Auth token response
        token = response.auth_token
        newUser = response.user || (await authAPI.getProfile())
      }

      if (token && newUser) {
        api.setToken(token)
        setUser(newUser)
        toast.success("تم إنشاء الحساب وتسجيل الدخول بنجاح!")
      } else {
        toast.success("تم إنشاء الحساب بنجاح! يرجى تسجيل الدخول.")
      }

      return { success: true }
    } catch (error: any) {
      console.error("Registration error:", error)
      let errorMessage = "فشل في إنشاء الحساب"

      if (error.message) {
        if (error.message.includes("email")) {
          errorMessage = "البريد الإلكتروني مستخدم بالفعل"
        } else if (error.message.includes("password")) {
          errorMessage = "كلمة المرور ضعيفة جداً"
        } else {
          errorMessage = error.message
        }
      }

      toast.error(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem("token")
    api.setToken(null)
    setUser(null)
    toast.info("تم تسجيل الخروج")
  }

  const updateProfile = async (data: Partial<User>) => {
    try {
      const updatedUser = await authAPI.updateProfile(data)
      setUser(updatedUser)
      toast.success("تم تحديث الملف الشخصي بنجاح!")
      return { success: true }
    } catch (error: any) {
      console.error("Profile update error:", error)
      const errorMessage = error.message || "فشل في تحديث الملف الشخصي"
      toast.error(errorMessage)
      return { success: false, error: errorMessage }
    }
  }

  const updateUser = async (data: Partial<User>) => {
    try {
      const updatedUser = await authAPI.updateProfile(data)
      setUser(updatedUser)
    } catch (error: any) {
      throw error
    }
  }

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    updateProfile,
    updateUser,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
