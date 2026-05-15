import { useEffect, useState } from 'react'
import { getByCarrier, getRecentShipments } from '../api/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const Logistics = () => {
  const [carriers, setCarriers] = useState([])
  const [shipments, setShipments] = useState([])

  useEffect(() => {
    getByCarrier().then(r => setCarriers(r.data))
    getRecentShipments().then(r => setShipments(r.data))
  }, [])

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-1">Logistics Tracker</h2>
      <p className="text-gray-400 text-sm mb-6">Shipment tracking and carrier performance</p>

      <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
        <h3 className="text-sm font-semibold text-gray-600 mb-4">Shipments by Carrier</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={carriers}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="carrier" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="shipments" fill="#8b5cf6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-600 mb-4">Recent Shipments</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Order ID</th>
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Carrier</th>
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Tracking</th>
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Dispatch</th>
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {shipments.map(s => (
                <tr key={s.logistics_id} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-3 px-4 text-gray-800">#{s.order_id}</td>
                  <td className="py-3 px-4 text-gray-500">{s.carrier}</td>
                  <td className="py-3 px-4 text-gray-400 font-mono text-xs">{s.tracking_number}</td>
                  <td className="py-3 px-4 text-gray-500">{s.dispatch_date?.slice(0,10)}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium
                      ${s.status === 'delivered' ? 'bg-green-100 text-green-600'
                      : s.status === 'shipped' ? 'bg-blue-100 text-blue-600'
                      : s.status === 'pending' ? 'bg-yellow-100 text-yellow-600'
                      : 'bg-gray-100 text-gray-600'}`}>
                      {s.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Logistics