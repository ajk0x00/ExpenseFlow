import React, { useEffect, useState } from 'react';
import { Plus, Edit2, Trash2, Upload } from 'lucide-react';
import { getTransactions, createTransaction, updateTransaction, deleteTransaction } from '../api/transactions';
import type { Transaction, TransactionCreate, TransactionUpdate } from '../api/transactions';
import TransactionForm from './TransactionForm';
import TransactionUpload from './TransactionUpload';
import ConfirmationModal from './ConfirmationModal';

const TransactionList: React.FC = () => {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [isUploadOpen, setIsUploadOpen] = useState(false);
    const [editingTransaction, setEditingTransaction] = useState<Transaction | undefined>(undefined);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [deleteId, setDeleteId] = useState<number | null>(null);

    const fetchTransactions = async () => {
        try {
            const data = await getTransactions();
            setTransactions(data);
        } catch (err) {
            setError('Failed to fetch transactions');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTransactions();
    }, []);

    const handleCreate = async (data: TransactionCreate) => {
        try {
            await createTransaction(data);
            setIsFormOpen(false);
            fetchTransactions();
        } catch (err) {
            console.error('Failed to create transaction', err);
            alert('Failed to create transaction');
        }
    };

    const handleUpdate = async (data: TransactionUpdate) => {
        if (!editingTransaction) return;
        try {
            await updateTransaction(editingTransaction.id, data);
            setIsFormOpen(false);
            setEditingTransaction(undefined);
            fetchTransactions();
        } catch (err) {
            console.error('Failed to update transaction', err);
            alert('Failed to update transaction');
        }
    };

    const confirmDelete = (id: number) => {
        setDeleteId(id);
    };

    const handleDelete = async () => {
        if (deleteId === null) return;
        try {
            await deleteTransaction(deleteId);
            setDeleteId(null);
            fetchTransactions();
        } catch (err) {
            console.error('Failed to delete transaction', err);
            alert('Failed to delete transaction');
        }
    };

    const openCreateForm = () => {
        setEditingTransaction(undefined);
        setIsFormOpen(true);
    };

    const openEditForm = (transaction: Transaction) => {
        setEditingTransaction(transaction);
        setIsFormOpen(true);
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="text-red-500">{error}</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-800">Transactions</h2>
                <div className="flex space-x-3">
                    <button
                        onClick={() => setIsUploadOpen(true)}
                        className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                        <Upload size={20} className="mr-2" />
                        Upload Statement
                    </button>
                    <button
                        onClick={openCreateForm}
                        className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        <Plus size={20} className="mr-2" />
                        Add Transaction
                    </button>
                </div>
            </div>

            {isFormOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
                        <h3 className="text-xl font-bold mb-4">
                            {editingTransaction ? 'Edit Transaction' : 'New Transaction'}
                        </h3>
                        <TransactionForm
                            initialData={editingTransaction}
                            onSubmit={(data) => editingTransaction ? handleUpdate(data as TransactionUpdate) : handleCreate(data as TransactionCreate)}
                            onCancel={() => setIsFormOpen(false)}
                        />
                    </div>
                </div>
            )}

            {isUploadOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                        <TransactionUpload
                            onSuccess={() => {
                                setIsUploadOpen(false);
                                fetchTransactions();
                            }}
                            onCancel={() => setIsUploadOpen(false)}
                        />
                    </div>
                </div>
            )}

            <ConfirmationModal
                isOpen={deleteId !== null}
                title="Delete Transaction"
                message="Are you sure you want to delete this transaction? This action cannot be undone."
                onConfirm={handleDelete}
                onCancel={() => setDeleteId(null)}
            />

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Narration</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Withdrawal</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Deposit</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {transactions.map((transaction) => (
                            <tr key={transaction.id}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {new Date(transaction.date).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    {transaction.narration}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">
                                    {transaction.withdrawal_amount > 0 ? transaction.withdrawal_amount : '-'}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">
                                    {transaction.deposit_amount > 0 ? transaction.deposit_amount : '-'}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button
                                        onClick={() => openEditForm(transaction)}
                                        className="text-blue-600 hover:text-blue-900 mr-4"
                                    >
                                        <Edit2 size={18} />
                                    </button>
                                    <button
                                        onClick={() => confirmDelete(transaction.id)}
                                        className="text-red-600 hover:text-red-900"
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TransactionList;
