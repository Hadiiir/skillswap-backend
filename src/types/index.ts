export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  bio?: string
  phone?: string
  avatar?: string
  points_balance: number
  skills_taught: number
  skills_learned: number
  total_orders: number
  completed_orders: number
  rating: number
  is_verified: boolean
  is_active: boolean
  date_joined: string
  last_login?: string
  // Additional computed properties for backward compatibility
  points?: number
  skills_count?: number
  orders_count?: number
}

export interface Skill {
  id: number
  title: string
  description: string
  category: string
  price: number
  duration: number
  requirements?: string
  provider: number
  provider_name: string
  is_active: boolean
  created_at: string
  updated_at: string
  // Additional properties from backend
  difficulty_level?: "beginner" | "intermediate" | "advanced" | "expert"
  duration_hours?: number
  points_required?: number
  price_per_hour?: number
  rating?: number
  reviews_count?: number
  instructor?: User
  average_rating?: number
  image?: string
}

export interface Category {
  id: number
  name: string
  description?: string
  skill_count: number
  skills_count?: number
  icon?: string
}

export interface Order {
  id: number
  skill: Skill
  buyer: number
  buyer_name: string
  student?: User
  instructor?: User
  status: "pending" | "accepted" | "completed" | "cancelled" | "confirmed" | "in_progress"
  message?: string
  points_spent?: number
  created_at: string
  updated_at: string
  completed_at?: string
}

export interface PointsPackage {
  id: number
  name: string
  points: number
  price: number
  description?: string
  currency?: string
  bonus_points?: number
  is_popular?: boolean
  is_active: boolean
}

export interface Transaction {
  id: number
  user: number
  amount: number
  transaction_type: "purchase" | "earned" | "spent" | "refund"
  description: string
  created_at: string
  points?: number
  currency?: string
  status?: "pending" | "completed" | "failed"
}

export interface PointTransaction {
  id: number
  amount: number
  transaction_type: string
  description: string
  created_at: string
  user?: number
  points?: number
  currency?: string
  status?: "pending" | "completed" | "failed"
}

export interface Payment {
  id: number
  user: number
  amount: number
  payment_method: string
  status: "pending" | "completed" | "failed" | "cancelled"
  transaction_id?: string
  currency?: string
  created_at: string
  updated_at?: string
  description?: string
}   

export interface Review {
  id: number
  skill: Skill
  reviewer: User
  rating: number
  comment: string
  created_at: string
}

export interface Notification {
  id: number
  user: User
  title: string
  message: string
  type: "info" | "success" | "warning" | "error"
  is_read: boolean
  created_at: string
}

export interface ChatRoom {
  id: number
  participants: User[]
  skill?: Skill
  order?: Order
  created_at: string
  updated_at: string
  last_message?: ChatMessage
}

export interface ChatMessage {
  id: number
  room: number
  sender: number
  sender_name: string
  message: string
  message_type?: "text" | "image" | "file"
  file_url?: string
  is_read?: boolean
  created_at: string
  timestamp?: string
}

export interface ApiResponse<T> {
  results: T[]
  count: number
  next?: string
  previous?: string
}

export interface LoginResponse {
  access?: string
  token?: string
  user?: User
  key?: string
  auth_token?: string
}

export interface RegisterResponse {
  access?: string
  token?: string
  user?: User
  message?: string
  key?: string
  auth_token?: string
}

export interface AuthContextType {
  user: User | null
  loading: boolean
  isAuthenticated: boolean
  login: (credentials: { email: string; password: string }) => Promise<{ success: boolean; error?: any }>
  register: (userData: { first_name: string; last_name: string; email: string; password: string }) => Promise<{
    success: boolean
    error?: any
  }>
  logout: () => void
  updateProfile: (data: Partial<User>) => Promise<{ success: boolean; error?: any }>
  updateUser: (data: Partial<User>) => Promise<void>
}
