import React from 'react';
import { LayoutDashboard, Wallet, Menu, X, ArrowRightLeft, FileSpreadsheet, Tags, LogOut } from 'lucide-react';
import { useNavigate, useLocation, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Layout = () => {
    const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);
    const navigate = useNavigate();
    const location = useLocation();
    const { logout } = useAuth();

    const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

    const isActive = (path: string) => {
        if (path === '/' && location.pathname === '/') return true;
        if (path !== '/' && location.pathname.startsWith(path)) return true;
        return false;
    };

    const navItems = [
        { path: '/', label: 'Dashboard', icon: LayoutDashboard },
        { path: '/accounts', label: 'Accounts', icon: Wallet },
        { path: '/transactions', label: 'Transactions', icon: ArrowRightLeft },
        { path: '/categories', label: 'Categories', icon: Tags },
        { path: '/statement-formats', label: 'Statement Formats', icon: FileSpreadsheet },
    ];

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <div
                className={`fixed inset-y-0 left-0 z-30 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
                    } md:relative md:translate-x-0`}
            >
                <div className="flex items-center justify-between p-4 border-b">
                    <h1 className="text-xl font-bold text-blue-600">Expense Tracker</h1>
                    <button onClick={toggleSidebar} className="md:hidden">
                        <X size={24} />
                    </button>
                </div>
                <nav className="p-4 space-y-2 flex flex-col h-[calc(100%-64px)]">
                    <div className="flex-1 space-y-2">
                        {navItems.map((item) => (
                            <button
                                key={item.path}
                                onClick={() => {
                                    navigate(item.path);
                                    setIsSidebarOpen(false);
                                }}
                                className={`flex items-center w-full p-3 rounded-lg transition-colors ${isActive(item.path)
                                    ? 'bg-blue-50 text-blue-600'
                                    : 'text-gray-600 hover:bg-gray-50'
                                    }`}
                            >
                                <item.icon size={20} className="mr-3" />
                                {item.label}
                            </button>
                        ))}
                    </div>
                    <button
                        onClick={handleLogout}
                        className="flex items-center w-full p-3 rounded-lg transition-colors text-red-600 hover:bg-red-50 mt-auto"
                    >
                        <LogOut size={20} className="mr-3" />
                        Logout
                    </button>
                </nav>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                <header className="bg-white shadow-sm p-4 flex items-center md:hidden">
                    <button onClick={toggleSidebar} className="text-gray-600">
                        <Menu size={24} />
                    </button>
                    <h1 className="ml-4 text-xl font-bold text-blue-600">Expense Tracker</h1>
                </header>
                <main className="flex-1 overflow-y-auto p-6">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default Layout;
