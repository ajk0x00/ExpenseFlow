import React, { useState, useEffect } from 'react';
import type { BankAccount, BankAccountCreate, BankAccountUpdate } from '../api/accounts';

interface AccountFormProps {
    initialData?: BankAccount;
    onSubmit: (data: BankAccountCreate | BankAccountUpdate) => void;
    onCancel: () => void;
}

const AccountForm: React.FC<AccountFormProps> = ({ initialData, onSubmit, onCancel }) => {
    const [formData, setFormData] = useState<BankAccountCreate>({
        account_name: '',
        bank_name: '',
        description: '',
        account_type: 'debit',
        metadata_: {},
    });

    const [metadataEntries, setMetadataEntries] = useState<{ key: string; value: string }[]>([]);

    useEffect(() => {
        if (initialData) {
            setFormData({
                account_name: initialData.account_name,
                bank_name: initialData.bank_name,
                description: initialData.description || '',
                account_type: initialData.account_type,
                metadata_: initialData.metadata_ || {},
            });
            if (initialData.metadata_) {
                setMetadataEntries(
                    Object.entries(initialData.metadata_).map(([key, value]) => ({ key, value: String(value) }))
                );
            }
        }
    }, [initialData]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleMetadataChange = (index: number, field: 'key' | 'value', value: string) => {
        const newEntries = [...metadataEntries];
        newEntries[index][field] = value;
        setMetadataEntries(newEntries);
    };

    const addMetadataEntry = () => {
        setMetadataEntries([...metadataEntries, { key: '', value: '' }]);
    };

    const removeMetadataEntry = (index: number) => {
        const newEntries = metadataEntries.filter((_, i) => i !== index);
        setMetadataEntries(newEntries);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const metadataObject = metadataEntries.reduce((acc, entry) => {
            if (entry.key) {
                acc[entry.key] = entry.value;
            }
            return acc;
        }, {} as Record<string, any>);

        onSubmit({ ...formData, metadata_: metadataObject });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label className="block text-sm font-medium text-gray-700">Account Name</label>
                <input
                    type="text"
                    name="account_name"
                    value={formData.account_name}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700">Bank Name</label>
                <input
                    type="text"
                    name="bank_name"
                    value={formData.bank_name}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700">Type</label>
                <select
                    name="account_type"
                    value={formData.account_type}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                >
                    <option value="debit">Debit</option>
                    <option value="credit">Credit</option>
                </select>
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    rows={3}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Metadata</label>
                {metadataEntries.map((entry, index) => (
                    <div key={index} className="flex items-center space-x-2 mb-2">
                        <input
                            type="text"
                            placeholder="Key"
                            value={entry.key}
                            onChange={(e) => handleMetadataChange(index, 'key', e.target.value)}
                            className="flex-1 min-w-0 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                        />
                        <input
                            type="text"
                            placeholder="Value"
                            value={entry.value}
                            onChange={(e) => handleMetadataChange(index, 'value', e.target.value)}
                            className="flex-1 min-w-0 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                        />
                        <button
                            type="button"
                            onClick={() => removeMetadataEntry(index)}
                            className="px-2 py-1 text-red-600 hover:bg-red-50 rounded"
                        >
                            X
                        </button>
                    </div>
                ))}
                <button
                    type="button"
                    onClick={addMetadataEntry}
                    className="text-sm text-blue-600 hover:text-blue-800"
                >
                    + Add Metadata
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
                    {initialData ? 'Update Account' : 'Create Account'}
                </button>
            </div>
        </form>
    );
};

export default AccountForm;
