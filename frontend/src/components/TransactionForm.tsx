import React, { useState, useEffect } from 'react';
import type { BankAccount } from '../api/accounts';
import { getAccounts } from '../api/accounts';
import type { TransactionCreate, TransactionUpdate, Transaction } from '../api/transactions';

interface TransactionFormProps {
    initialData?: Transaction;
    onSubmit: (data: TransactionCreate | TransactionUpdate) => void;
    onCancel: () => void;
}

const TransactionForm: React.FC<TransactionFormProps> = ({ initialData, onSubmit, onCancel }) => {
    const [accounts, setAccounts] = useState<BankAccount[]>([]);
    const [formData, setFormData] = useState<TransactionCreate>({
        account_id: initialData?.account_id || 0,
        date: initialData?.date ? new Date(initialData.date).toISOString().slice(0, 16) : new Date().toISOString().slice(0, 16),
        narration: initialData?.narration || '',
        withdrawal_amount: initialData?.withdrawal_amount || 0,
        deposit_amount: initialData?.deposit_amount || 0,
        metadata_: initialData?.metadata_ || {},
    });

    useEffect(() => {
        const fetchAccounts = async () => {
            try {
                const data = await getAccounts();
                setAccounts(data);
                if (!initialData && data.length > 0) {
                    setFormData(prev => ({ ...prev, account_id: data[0].id }));
                }
            } catch (err) {
                console.error('Failed to fetch accounts', err);
            }
        };
        fetchAccounts();
    }, [initialData]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'account_id' ? parseInt(value) :
                name === 'withdrawal_amount' || name === 'deposit_amount' ? parseFloat(value) : value
        }));
    };

    const handleMetadataChange = (key: string, value: string) => {
        setFormData(prev => ({
            ...prev,
            metadata_: { ...prev.metadata_, [key]: value }
        }));
    };

    const addMetadataField = () => {
        setFormData(prev => ({
            ...prev,
            metadata_: { ...prev.metadata_, '': '' }
        }));
    };

    const removeMetadataField = (key: string) => {
        const newMetadata = { ...formData.metadata_ };
        delete newMetadata[key];
        setFormData(prev => ({ ...prev, metadata_: newMetadata }));
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label className="block text-sm font-medium text-gray-700">Account</label>
                <select
                    name="account_id"
                    value={formData.account_id}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                    required
                >
                    {accounts.map(account => (
                        <option key={account.id} value={account.id}>
                            {account.account_name} ({account.bank_name})
                        </option>
                    ))}
                </select>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Date</label>
                <input
                    type="datetime-local"
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                    required
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Narration</label>
                <input
                    type="text"
                    name="narration"
                    value={formData.narration}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                    required
                />
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Withdrawal Amount</label>
                    <input
                        type="number"
                        step="0.01"
                        name="withdrawal_amount"
                        value={formData.withdrawal_amount}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Deposit Amount</label>
                    <input
                        type="number"
                        step="0.01"
                        name="deposit_amount"
                        value={formData.deposit_amount}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Metadata</label>
                {Object.entries(formData.metadata_ || {}).map(([key, value], index) => (
                    <div key={index} className="flex gap-2 mb-2">
                        <input
                            type="text"
                            placeholder="Key"
                            value={key}
                            onChange={(e) => {
                                const newKey = e.target.value;
                                const newMetadata = { ...formData.metadata_ };
                                delete newMetadata[key];
                                newMetadata[newKey] = value;
                                setFormData(prev => ({ ...prev, metadata_: newMetadata }));
                            }}
                            className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                        />
                        <input
                            type="text"
                            placeholder="Value"
                            value={value}
                            onChange={(e) => handleMetadataChange(key, e.target.value)}
                            className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                        />
                        <button
                            type="button"
                            onClick={() => removeMetadataField(key)}
                            className="text-red-600 hover:text-red-800"
                        >
                            Remove
                        </button>
                    </div>
                ))}
                <button
                    type="button"
                    onClick={addMetadataField}
                    className="text-sm text-blue-600 hover:text-blue-800"
                >
                    + Add Metadata Field
                </button>
            </div>

            <div className="flex justify-end space-x-3 pt-4">
                <button
                    type="button"
                    onClick={onCancel}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                >
                    Cancel
                </button>
                <button
                    type="submit"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
                >
                    {initialData ? 'Update Transaction' : 'Create Transaction'}
                </button>
            </div>
        </form>
    );
};

export default TransactionForm;
