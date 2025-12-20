import { useState } from 'react';
import Layout from './components/Layout';
import AccountList from './components/AccountList';
import TransactionList from './components/TransactionList';
import StatementFormatList from './components/StatementFormatList';
import CategoryList from './components/CategoryList';

function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'accounts' | 'transactions' | 'categories' | 'statement-formats'>('dashboard');

  return (
    <Layout activeTab={activeTab} onTabChange={setActiveTab}>
      {activeTab === 'dashboard' && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-800">Dashboard</h2>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <p className="text-gray-600">Welcome to your Expense Tracker Dashboard!</p>
          </div>
        </div>
      )}
      {activeTab === 'accounts' && <AccountList />}
      {activeTab === 'transactions' && <TransactionList />}
      {activeTab === 'categories' && <CategoryList />}
      {activeTab === 'statement-formats' && <StatementFormatList />}
    </Layout>
  );
}

export default App;
