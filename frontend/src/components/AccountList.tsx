import React, { useEffect, useState } from 'react';
import { Plus, Edit2, Trash2 } from 'lucide-react';
import { getAccounts, createAccount, updateAccount, deleteAccount } from '../api/accounts';
import type { BankAccount, BankAccountCreate, BankAccountUpdate } from '../api/accounts';
import AccountForm from './AccountForm';
import ConfirmationModal from './ConfirmationModal';

const AccountList: React.FC = () => {
    const [accounts, setAccounts] = useState<BankAccount[]>([]);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [editingAccount, setEditingAccount] = useState<BankAccount | undefined>(undefined);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [deleteId, setDeleteId] = useState<number | null>(null);

    const fetchAccounts = async () => {
        try {
            const data = await getAccounts();
            setAccounts(data);
        } catch (err) {
            setError('Failed to fetch accounts');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAccounts();
    }, []);

    const handleCreate = async (data: BankAccountCreate) => {
        try {
            await createAccount(data);
            setIsFormOpen(false);
            fetchAccounts();
        } catch (err) {
            console.error('Failed to create account', err);
            alert('Failed to create account');
        }
    };

    const handleUpdate = async (data: BankAccountUpdate) => {
        if (!editingAccount) return;
        try {
            await updateAccount(editingAccount.id, data);
            setIsFormOpen(false);
            setEditingAccount(undefined);
            fetchAccounts();
        } catch (err) {
            console.error('Failed to update account', err);
            alert('Failed to update account');
        }
    };

    const confirmDelete = (id: number) => {
        setDeleteId(id);
    };

    const handleDelete = async () => {
        if (deleteId === null) return;
        try {
            await deleteAccount(deleteId);
            setDeleteId(null);
            fetchAccounts();
        } catch (err) {
            console.error('Failed to delete account', err);
            alert('Failed to delete account');
        }
    };

    const openCreateForm = () => {
        setEditingAccount(undefined);
        setIsFormOpen(true);
    };

    const openEditForm = (account: BankAccount) => {
        setEditingAccount(account);
        setIsFormOpen(true);
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="text-red-500">{error}</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-800">Accounts</h2>
                <button
                    onClick={openCreateForm}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <Plus size={20} className="mr-2" />
                    Add Account
                </button>
            </div>

            {isFormOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
                        <h3 className="text-xl font-bold mb-4">
                            {editingAccount ? 'Edit Account' : 'New Account'}
                        </h3>
                        <AccountForm
                            initialData={editingAccount}
                            onSubmit={(data) => editingAccount ? handleUpdate(data as BankAccountUpdate) : handleCreate(data as BankAccountCreate)}
                            onCancel={() => setIsFormOpen(false)}
                        />
                    </div>
                </div>
            )}

            <ConfirmationModal
                isOpen={deleteId !== null}
                title="Delete Account"
                message="Are you sure you want to delete this account? This action cannot be undone."
                onConfirm={handleDelete}
                onCancel={() => setDeleteId(null)}
            />

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {accounts.map((account) => (
                    <div key={account.id} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900">{account.account_name}</h3>
                                <p className="text-sm text-gray-500">{account.bank_name}</p>
                            </div>
                            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${account.account_type === 'credit' ? 'bg-purple-100 text-purple-800' : 'bg-green-100 text-green-800'
                                }`}>
                                {account.account_type.toUpperCase()}
                            </span>
                        </div>
                        {account.description && (
                            <p className="text-gray-600 text-sm mb-4">{account.description}</p>
                        )}
                        <div className="flex justify-end space-x-2 pt-4 border-t">
                            <button
                                onClick={() => openEditForm(account)}
                                className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
                            >
                                <Edit2 size={18} />
                            </button>
                            <button
                                onClick={() => confirmDelete(account.id)}
                                className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                            >
                                <Trash2 size={18} />
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AccountList;
