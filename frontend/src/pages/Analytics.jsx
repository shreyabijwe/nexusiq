import { useEffect, useState } from 'react'
import { getDemandForecast, getAnomalyDetection, getExecutiveSummary } from '../api/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const Analytics = () => {
  const [forecast, setForecast] = useState(null)
  const [anomalies, setAnomalies] = useState(null)
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    getDemandForecast().then(r => setForecast(r.data))
    getAnomalyDetection().then(r => setAnomalies(r.data))
    getExecutiveSummary().then(r => setSummary(r.data))
  }, [])

  const forecastData = forecast ? [
    ...forecast.historical.map(h => ({ month: h.month, actual: h.revenue, forecast: null })),
    ...forecast.forecast.map(f => ({ month: f.month, actual: null, forecast: f.predicted_revenue }))
  ] : []

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-1">AI Analytics</h2>
      <p className="text-gray-400 text-sm mb-6">Forecasting, anomaly detection and executive insights</p>

      {summary && (
        <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
          <h3 className="text-sm font-semibold text-gray-600 mb-4">Executive Summary</h3>
          <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans leading-relaxed">
            {summary.summary}
          </pre>
        </div>
      )}

      <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
        <h3 className="text-sm font-semibold text-gray-600 mb-4">Demand Forecast — Next 3 Months</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="month" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} tickFormatter={v => `$${(v/1000).toFixed(0)}k`} />
            <Tooltip formatter={v => [`$${v?.toLocaleString()}`, '']} />
            <Legend />
            <Line type="monotone" dataKey="actual" stroke="#3b82f6" strokeWidth={2} dot={false} name="Actual Revenue" />
            <Line type="monotone" dataKey="forecast" stroke="#f59e0b" strokeWidth={2} strokeDasharray="5 5" dot={false} name="Forecast" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-600 mb-4">Anomaly Detection</h3>
        {anomalies?.anomalies.length > 0 ? (
          <div className="mb-4">
            <p className="text-sm text-red-500 font-medium mb-2">⚠ {anomalies.anomalies.length} anomalies detected</p>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left py-2 px-4 text-gray-500">Date</th>
                  <th className="text-left py-2 px-4 text-gray-500">Revenue</th>
                  <th className="text-left py-2 px-4 text-gray-500">Orders</th>
                  <th className="text-left py-2 px-4 text-gray-500">Z-Score</th>
                  <th className="text-left py-2 px-4 text-gray-500">Type</th>
                </tr>
              </thead>
              <tbody>
                {anomalies.anomalies.map((a, i) => (
                  <tr key={i} className="border-b border-gray-50 bg-red-50">
                    <td className="py-2 px-4 text-gray-800">{a.day}</td>
                    <td className="py-2 px-4 text-gray-800">${a.revenue.toLocaleString()}</td>
                    <td className="py-2 px-4 text-gray-800">{a.order_count}</td>
                    <td className="py-2 px-4 text-gray-800">{a.z_score}</td>
                    <td className="py-2 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${a.z_score > 0 ? 'bg-orange-100 text-orange-600' : 'bg-red-100 text-red-600'}`}>
                        {a.z_score > 0 ? 'Spike' : 'Drop'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-green-500 text-sm">No anomalies detected</p>
        )}
      </div>
    </div>
  )
}

export default Analytics