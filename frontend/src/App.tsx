import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import AccountList from './components/AccountList';
import TransactionList from './components/TransactionList';
import StatementFormatList from './components/StatementFormatList';
import CategoryList from './components/CategoryList';
import Dashboard from './components/Dashboard';
import LoginPage from './pages/LoginPage';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/accounts" element={<AccountList />} />
          <Route path="/transactions" element={<TransactionList />} />
          <Route path="/categories" element={<CategoryList />} />
          <Route path="/statement-formats" element={<StatementFormatList />} />
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
