import { useEffect, useState } from 'react'
import KPICard from '../components/KPICard'
import { getSalesSummary, getInventorySummary, getLogisticsSummary } from '../api/api'

const Dashboard = () => {
  const [sales, setSales] = useState(null)
  const [inventory, setInventory] = useState(null)
  const [logistics, setLogistics] = useState(null)

  useEffect(() => {
    getSalesSummary().then(r => setSales(r.data))
    getInventorySummary().then(r => setInventory(r.data))
    getLogisticsSummary().then(r => setLogistics(r.data))
  }, [])

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-1">Dashboard</h2>
      <p className="text-gray-400 text-sm mb-6">Real-time business overview</p>

      <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">Sales KPIs</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <KPICard title="Total Revenue" value={sales ? `$${sales.total_revenue.toLocaleString()}` : '...'} color="border-blue-500" />
        <KPICard title="Total Orders" value={sales ? sales.total_orders.toLocaleString() : '...'} color="border-green-500" />
        <KPICard title="Avg Order Value" value={sales ? `$${sales.avg_order_value}` : '...'} color="border-purple-500" />
        <KPICard title="Total Customers" value={sales ? sales.total_customers.toLocaleString() : '...'} color="border-orange-500" />
      </div>

      <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">Inventory KPIs</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <KPICard title="Total Products" value={inventory ? inventory.total_products : '...'} color="border-blue-500" />
        <KPICard title="Low Stock Items" value={inventory ? inventory.low_stock_items : '...'} color="border-yellow-500" />
        <KPICard title="Out of Stock" value={inventory ? inventory.out_of_stock_items : '...'} color="border-red-500" />
      </div>

      <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">Logistics KPIs</h3>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard title="Total Shipments" value={logistics ? logistics.total_shipments.toLocaleString() : '...'} color="border-blue-500" />
        <KPICard title="Delivered" value={logistics ? logistics.delivered.toLocaleString() : '...'} color="border-green-500" />
        <KPICard title="Pending" value={logistics ? logistics.pending.toLocaleString() : '...'} color="border-yellow-500" />
        <KPICard title="Shipped" value={logistics ? logistics.shipped.toLocaleString() : '...'} color="border-purple-500" />
      </div>
    </div>
  )
}

export default Dashboard