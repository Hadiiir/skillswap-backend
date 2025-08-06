import type {
  User,
  Skill,
  Category,
  Order,
  PointsPackage,
  Transaction,
  Payment,
  ChatRoom,
  ChatMessage,
  ApiResponse,
  LoginResponse,
  RegisterResponse,
} from "../types"

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api"

class ApiService {
  private baseURL: string
  private token: string | null

  constructor() {
    this.baseURL = API_BASE_URL
    this.token = localStorage.getItem("token")
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    }

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`
    }

    if (options.headers) {
      Object.assign(headers, options.headers)
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: "Network error" }))
      throw new Error(error.message || `HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  setToken(token: string | null) {
    this.token = token
    if (token) {
      localStorage.setItem("token", token)
    } else {
      localStorage.removeItem("token")
    }
  }

  // Auth endpoints
  async login(credentials: { email: string; password: string }): Promise<LoginResponse> {
    return this.request<LoginResponse>("/auth/login/", {
      method: "POST",
      body: JSON.stringify(credentials),
    })
  }

  async register(userData: {
    first_name: string
    last_name: string
    email: string
    password: string
  }): Promise<RegisterResponse> {
    return this.request<RegisterResponse>("/auth/register/", {
      method: "POST",
      body: JSON.stringify(userData),
    })
  }

  async getProfile(): Promise<User> {
    return this.request<User>("/auth/profile/")
  }

  async updateProfile(data: Partial<User>): Promise<User> {
    return this.request<User>("/auth/profile/", {
      method: "PATCH",
      body: JSON.stringify(data),
    })
  }

  // Skills endpoints
  async getSkills(params?: any): Promise<ApiResponse<Skill>> {
    const queryString = params ? new URLSearchParams(params).toString() : ""
    return this.request<ApiResponse<Skill>>(`/skills/${queryString ? `?${queryString}` : ""}`)
  }

  async getSkill(id: number): Promise<Skill> {
    return this.request<Skill>(`/skills/${id}/`)
  }

  async createSkill(data: any): Promise<Skill> {
    return this.request<Skill>("/skills/", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async updateSkill(id: number, data: any): Promise<Skill> {
    return this.request<Skill>(`/skills/${id}/`, {
      method: "PATCH",
      body: JSON.stringify(data),
    })
  }

  async deleteSkill(id: number): Promise<void> {
    return this.request<void>(`/skills/${id}/`, {
      method: "DELETE",
    })
  }

  async getCategories(): Promise<ApiResponse<Category>> {
    return this.request<ApiResponse<Category>>("/skills/categories/")
  }

  // Points endpoints
  async getPackages(): Promise<ApiResponse<PointsPackage>> {
    return this.request<ApiResponse<PointsPackage>>("/points/packages/")
  }

  async purchasePackage(packageId: number): Promise<any> {
    return this.request("/points/purchase/", {
      method: "POST",
      body: JSON.stringify({ package_id: packageId }),
    })
  }

  async getTransactions(): Promise<ApiResponse<Transaction>> {
    return this.request<ApiResponse<Transaction>>("/points/transactions/")
  }

  async getPointTransactions(): Promise<Transaction[]> {
    const response = await this.request<ApiResponse<Transaction>>("/points/transactions/")
    return response.results
  }

  async purchasePoints(amount: number): Promise<any> {
    return this.request("/points/purchase/", {
      method: "POST",
      body: JSON.stringify({ amount }),
    })
  }

  async createOrder(data: { skill: number; message?: string }): Promise<Order> {
    return this.request<Order>("/points/orders/", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async getOrders(): Promise<ApiResponse<Order>> {
    return this.request<ApiResponse<Order>>("/points/orders/")
  }

  // Payments endpoints
  async getPaymentHistory(): Promise<ApiResponse<Payment>> {
    return this.request<ApiResponse<Payment>>("/payments/history/")
  }

  async createPayment(data: any): Promise<Payment> {
    return this.request<Payment>("/payments/", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  // Chat endpoints
  async getRooms(): Promise<ApiResponse<ChatRoom>> {
    return this.request<ApiResponse<ChatRoom>>("/chat/rooms/")
  }

  async getRoom(id: number): Promise<ChatRoom> {
    return this.request<ChatRoom>(`/chat/rooms/${id}/`)
  }

  async getMessages(roomId: number): Promise<ApiResponse<ChatMessage>> {
    return this.request<ApiResponse<ChatMessage>>(`/chat/rooms/${roomId}/messages/`)
  }

  async sendMessage(roomId: number, message: string): Promise<ChatMessage> {
    return this.request<ChatMessage>(`/chat/rooms/${roomId}/messages/`, {
      method: "POST",
      body: JSON.stringify({ message }),
    })
  }

  async createRoom(participantId: number, skillId?: number): Promise<ChatRoom> {
    return this.request<ChatRoom>("/chat/rooms/", {
      method: "POST",
      body: JSON.stringify({
        participant_id: participantId,
        skill_id: skillId,
      }),
    })
  }
}

const api = new ApiService()

// Export individual API modules
export const authAPI = {
  login: api.login.bind(api),
  register: api.register.bind(api),
  getProfile: api.getProfile.bind(api),
  updateProfile: api.updateProfile.bind(api),
}

export const skillsAPI = {
  getSkills: api.getSkills.bind(api),
  getSkill: api.getSkill.bind(api),
  createSkill: api.createSkill.bind(api),
  updateSkill: api.updateSkill.bind(api),
  deleteSkill: api.deleteSkill.bind(api),
  getCategories: api.getCategories.bind(api),
}

export const pointsAPI = {
  getPackages: api.getPackages.bind(api),
  purchasePackage: api.purchasePackage.bind(api),
  purchasePoints: api.purchasePoints.bind(api),
  getTransactions: api.getTransactions.bind(api),
  getPointTransactions: api.getPointTransactions.bind(api),
  createOrder: api.createOrder.bind(api),
  getOrders: api.getOrders.bind(api),
}

export const paymentsAPI = {
  getPaymentHistory: api.getPaymentHistory.bind(api),
  createPayment: api.createPayment.bind(api),
}

export const chatAPI = {
  getRooms: api.getRooms.bind(api),
  getRoom: api.getRoom.bind(api),
  getMessages: api.getMessages.bind(api),
  sendMessage: api.sendMessage.bind(api),
  createRoom: api.createRoom.bind(api),
}

// Export the main API service as default and named export
export const apiService = api
export default api
