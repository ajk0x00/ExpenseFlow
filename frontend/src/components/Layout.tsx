import React from 'react';
import { LayoutDashboard, Wallet, Menu, X, ArrowRightLeft, FileSpreadsheet, Tags } from 'lucide-react';

interface LayoutProps {
    children: React.ReactNode;
    activeTab: 'dashboard' | 'accounts' | 'transactions' | 'categories' | 'statement-formats';
    onTabChange: (tab: 'dashboard' | 'accounts' | 'transactions' | 'categories' | 'statement-formats') => void;
}

const Layout: React.FC<LayoutProps> = ({ children, activeTab, onTabChange }) => {
    const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);

    const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

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
                <nav className="p-4 space-y-2">
                    <button
                        onClick={() => {
                            onTabChange('dashboard');
                            setIsSidebarOpen(false);
                        }}
                        className={`flex items-center w-full p-3 rounded-lg transition-colors ${activeTab === 'dashboard'
                            ? 'bg-blue-50 text-blue-600'
                            : 'text-gray-600 hover:bg-gray-50'
                            }`}
                    >
                        <LayoutDashboard size={20} className="mr-3" />
                        Dashboard
                    </button>
                    <button
                        onClick={() => {
                            onTabChange('accounts');
                            setIsSidebarOpen(false);
                        }}
                        className={`flex items-center w-full p-3 rounded-lg transition-colors ${activeTab === 'accounts'
                            ? 'bg-blue-50 text-blue-600'
                            : 'text-gray-600 hover:bg-gray-50'
                            }`}
                    >
                        <Wallet size={20} className="mr-3" />
                        Accounts
                    </button>
                    <button
                        onClick={() => {
                            onTabChange('transactions');
                            setIsSidebarOpen(false);
                        }}
                        className={`flex items-center w-full p-3 rounded-lg transition-colors ${activeTab === 'transactions'
                            ? 'bg-blue-50 text-blue-600'
                            : 'text-gray-600 hover:bg-gray-50'
                            }`}
                    >
                        <ArrowRightLeft size={20} className="mr-3" />
                        Transactions
                    </button>
                    <button
                        onClick={() => {
                            onTabChange('categories');
                            setIsSidebarOpen(false);
                        }}
                        className={`flex items-center w-full p-3 rounded-lg transition-colors ${activeTab === 'categories'
                            ? 'bg-blue-50 text-blue-600'
                            : 'text-gray-600 hover:bg-gray-50'
                            }`}
                    >
                        <Tags size={20} className="mr-3" />
                        Categories
                    </button>
                    <button
                        onClick={() => {
                            onTabChange('statement-formats');
                            setIsSidebarOpen(false);
                        }}
                        className={`flex items-center w-full p-3 rounded-lg transition-colors ${activeTab === 'statement-formats'
                            ? 'bg-blue-50 text-blue-600'
                            : 'text-gray-600 hover:bg-gray-50'
                            }`}
                    >
                        <FileSpreadsheet size={20} className="mr-3" />
                        Statement Formats
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
                    {children}
                </main>
            </div>
        </div>
    );
};

export default Layout;
