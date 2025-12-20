import { useState } from 'react';
import Layout from './components/Layout';
import AccountList from './components/AccountList';
import TransactionList from './components/TransactionList';
import StatementFormatList from './components/StatementFormatList';
import CategoryList from './components/CategoryList';

import Dashboard from './components/Dashboard';

function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'accounts' | 'transactions' | 'categories' | 'statement-formats'>('dashboard');

  return (
    <Layout activeTab={activeTab} onTabChange={setActiveTab}>
      {activeTab === 'dashboard' && <Dashboard />}
      {activeTab === 'accounts' && <AccountList />}
      {activeTab === 'transactions' && <TransactionList />}
      {activeTab === 'categories' && <CategoryList />}
      {activeTab === 'statement-formats' && <StatementFormatList />}
    </Layout>
  );
}

export default App;
