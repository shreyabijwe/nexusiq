import axios from 'axios'

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export const getSalesSummary = () => API.get('/api/sales/summary')
export const getSalesByStatus = () => API.get('/api/sales/by-status')
export const getMonthlyRevenue = () => API.get('/api/sales/monthly-revenue')
export const getTopProducts = () => API.get('/api/sales/top-products')
export const getInventorySummary = () => API.get('/api/inventory/summary')
export const getAllInventory = () => API.get('/api/inventory/all')
export const getInventoryByWarehouse = () => API.get('/api/inventory/by-warehouse')
export const getLogisticsSummary = () => API.get('/api/logistics/summary')
export const getByCarrier = () => API.get('/api/logistics/by-carrier')
export const getRecentShipments = () => API.get('/api/logistics/recent')
export const login = (data) => API.post('/api/auth/login', data)
export const getDemandForecast = () => API.get('/api/analytics/demand-forecast')
export const getAnomalyDetection = () => API.get('/api/analytics/anomaly-detection')
export const getExecutiveSummary = () => API.get('/api/analytics/executive-summary')
