"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { useAuth } from "../../contexts/AuthContext"
import { apiService } from "../../services/api"
import type { Transaction } from "../../types"
import { toast } from "react-toastify"

const Points: React.FC = () => {
  const { user, updateUser } = useAuth()
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [purchaseAmount, setPurchaseAmount] = useState("")
  const [purchasing, setPurchasing] = useState(false)

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const data = (await apiService.getPointTransactions()) as Transaction[]
        setTransactions(data)
      } catch (error) {
        console.error("Error fetching point transactions:", error)
        toast.error("Error loading point transactions")
      } finally {
        setLoading(false)
      }
    }

    fetchTransactions()
  }, [])

  const handlePurchasePoints = async (e: React.FormEvent) => {
    e.preventDefault()
    const amount = Number.parseInt(purchaseAmount)

    if (!amount || amount < 10) {
      toast.error("Minimum purchase is 10 points")
      return
    }

    setPurchasing(true)
    try {
      const result = await apiService.purchasePoints(amount)
      toast.success(`Successfully purchased ${amount} points!`)
      setPurchaseAmount("")

      // Update user points
      if (user) {
        updateUser({ ...user, points_balance: (user.points_balance || 0) + amount })
      }

      // Refresh transactions
      const data = (await apiService.getPointTransactions()) as Transaction[]
      setTransactions(data)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Error purchasing points")
    } finally {
      setPurchasing(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading points data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Points Management</h1>
          <p className="mt-2 text-gray-600">View and manage your points on the platform</p>
        </div>

        {/* Current Points */}
        <div className="bg-white overflow-hidden shadow rounded-lg mb-8">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-yellow-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-bold">P</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Current Balance</dt>
                  <dd className="text-3xl font-bold text-gray-900">
                    {user?.points || user?.points_balance || 0} points
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        {/* Purchase Points */}
        <div className="bg-white shadow rounded-lg mb-8">
          <div className="px-4 py-5 sm:p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Purchase Points</h2>
            <form onSubmit={handlePurchasePoints} className="flex items-end space-x-4">
              <div className="flex-1">
                <label htmlFor="amount" className="block text-sm font-medium text-gray-700">
                  Number of Points
                </label>
                <input
                  type="number"
                  id="amount"
                  min="10"
                  step="10"
                  value={purchaseAmount}
                  onChange={(e) => setPurchaseAmount(e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter number of points (minimum 10)"
                />
              </div>
              <button
                type="submit"
                disabled={purchasing}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {purchasing ? "Purchasing..." : "Purchase"}
              </button>
            </form>
            <p className="mt-2 text-sm text-gray-500">Price per point: $1 USD</p>
          </div>
        </div>

        {/* Transactions History */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-4 py-5 sm:p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Transaction History</h2>
            {transactions.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Amount
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Type
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Description
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {transactions.map((transaction) => (
                      <tr key={transaction.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <span className={transaction.amount > 0 ? "text-green-600" : "text-red-600"}>
                            {transaction.amount > 0 ? "+" : ""}
                            {transaction.amount || transaction.points || 0} points
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {transaction.transaction_type === "purchase"
                            ? "Purchase"
                            : transaction.transaction_type === "earned"
                              ? "Earned"
                              : transaction.transaction_type === "spent"
                                ? "Spent"
                                : "Other"}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{transaction.description}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(transaction.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="mx-auto h-12 w-12 text-gray-400">
                  <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                </div>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No transactions</h3>
                <p className="mt-1 text-sm text-gray-500">You haven't made any point transactions yet</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Points
