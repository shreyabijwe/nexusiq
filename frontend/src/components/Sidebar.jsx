import { Link, useLocation } from 'react-router-dom'

const links = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/sales', label: 'Sales', icon: '💰' },
  { path: '/inventory', label: 'Inventory', icon: '📦' },
  { path: '/logistics', label: 'Logistics', icon: '🚚' },
  { path: '/analytics', label: 'AI Analytics', icon: '🤖' },
]

const Sidebar = () => {
  const location = useLocation()

  return (
    <div className="w-64 bg-gray-900 min-h-screen p-6 flex flex-col">
      <div className="mb-8">
        <h1 className="text-white text-xl font-bold">NexusIQ</h1>
        <p className="text-gray-400 text-xs mt-1">Decision Intelligence</p>
      </div>
      <nav className="flex flex-col gap-2">
        {links.map(link => (
          <Link
            key={link.path}
            to={link.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all
              ${location.pathname === link.path
                ? 'bg-blue-600 text-white'
                : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`}
          >
            <span>{link.icon}</span>
            {link.label}
          </Link>
        ))}
      </nav>
    </div>
  )
}

export default Sidebar