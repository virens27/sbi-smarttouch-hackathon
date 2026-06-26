"use client";
import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

interface Stats {
  total_customers: number;
  disengaged: number;
  active: number;
  disengagement_rate: number;
}

interface Customer {
  customer_id: string;
  age: number;
  disengagement_probability: number;
  nudge_message: string;
}

export default function Home() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [atRisk, setAtRisk] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, atRiskRes] = await Promise.all([
          fetch(`${API}/api/stats`),
          fetch(`${API}/api/at-risk?limit=10`),
        ]);
        const statsData = await statsRes.json();
        const atRiskData = await atRiskRes.json();
        setStats(statsData);
        setAtRisk(atRiskData);
      } catch (error) {
        console.error("Failed to fetch data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-500 text-lg">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          SBI SmartTouch
        </h1>
        <p className="text-gray-500 mt-1">
          Agentic AI Customer Engagement Dashboard
        </p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-sm text-gray-500 mb-1">Total Customers</p>
            <p className="text-3xl font-bold text-gray-900">
              {stats.total_customers.toLocaleString()}
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-sm text-gray-500 mb-1">Active</p>
            <p className="text-3xl font-bold text-green-600">
              {stats.active.toLocaleString()}
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-sm text-gray-500 mb-1">Disengaged</p>
            <p className="text-3xl font-bold text-red-500">
              {stats.disengaged.toLocaleString()}
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-sm text-gray-500 mb-1">Disengagement Rate</p>
            <p className="text-3xl font-bold text-orange-500">
              {stats.disengagement_rate}%
            </p>
          </div>
        </div>
      )}

      {/* At-Risk Customers Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            Top At-Risk Customers
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Customers with highest disengagement probability — 
            personalized nudges auto-generated
          </p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">
                  Customer ID
                </th>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">
                  Age
                </th>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">
                  Risk Score
                </th>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">
                  Recommended Nudge
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {atRisk.map((customer) => (
                <tr key={customer.customer_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-mono text-sm text-gray-900">
                    {customer.customer_id}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {customer.age}
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700">
                      {(customer.disengagement_probability * 100).toFixed(0)}%
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600 max-w-md">
                    {customer.nudge_message}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Footer */}
      <p className="text-center text-gray-400 text-sm mt-8">
        SBI SmartTouch — Team ZeroGap — SBI AI Hackathon @ GFF 2026
      </p>
    </main>
  );
}