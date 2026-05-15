import { useEffect, useState } from 'react'
import { getAllInventory, getInventoryByWarehouse } from '../api/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const Inventory = () => {
  const [inventory, setInventory] = useState([])
  const [warehouse, setWarehouse] = useState([])

  useEffect(() => {
    getAllInventory().then(r => setInventory(r.data))
    getInventoryByWarehouse().then(r => setWarehouse(r.data))
  }, [])

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-1">Inventory Management</h2>
      <p className="text-gray-400 text-sm mb-6">Stock levels and warehouse distribution</p>

      <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
        <h3 className="text-sm font-semibold text-gray-600 mb-4">Stock by Warehouse</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={warehouse}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="warehouse" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="total_stock" fill="#10b981" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-600 mb-4">Product Inventory</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Product</th>
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Category</th>
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Stock</th>
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Warehouse</th>
                <th className="text-left py-3 px-4 text-gray-500 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {inventory.map(item => (
                <tr key={item.inventory_id} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-3 px-4 text-gray-800 font-medium">{item.product_name}</td>
                  <td className="py-3 px-4 text-gray-500">{item.category}</td>
                  <td className="py-3 px-4 text-gray-800">{item.quantity_in_stock}</td>
                  <td className="py-3 px-4 text-gray-500">{item.warehouse_location}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium
                      ${item.status === 'Low Stock'
                        ? 'bg-red-100 text-red-600'
                        : 'bg-green-100 text-green-600'}`}>
                      {item.status}
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

export default Inventory