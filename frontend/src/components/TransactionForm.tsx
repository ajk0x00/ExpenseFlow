import React, { useState, useEffect, useRef } from 'react';
import { ChevronDown, Check, X, Plus } from 'lucide-react';
import type { BankAccount } from '../api/accounts';
import { getAccounts } from '../api/accounts';
import type { TransactionCreate, TransactionUpdate, Transaction } from '../api/transactions';
import { getCategories } from '../api/categories';
import type { Category } from '../api/categories';

interface TransactionFormProps {
    initialData?: Transaction;
    onSubmit: (data: TransactionCreate | TransactionUpdate) => void;
    onCancel: () => void;
}

const TransactionForm: React.FC<TransactionFormProps> = ({ initialData, onSubmit, onCancel }) => {
    const [accounts, setAccounts] = useState<BankAccount[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    const [formData, setFormData] = useState<TransactionCreate>({
        account_id: initialData?.account_id || 0,
        date: initialData?.date ? new Date(initialData.date).toISOString().slice(0, 16) : new Date().toISOString().slice(0, 16),
        narration: initialData?.narration || '',
        withdrawal_amount: initialData?.withdrawal_amount || 0,
        deposit_amount: initialData?.deposit_amount || 0,
        category_ids: initialData?.categories?.map(c => c.id) || [],
        metadata_: initialData?.metadata_ || {},
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [accountsData, categoriesData] = await Promise.all([
                    getAccounts(),
                    getCategories()
                ]);
                setAccounts(accountsData);
                setCategories(categoriesData);

                if (!initialData && accountsData.length > 0) {
                    setFormData(prev => ({ ...prev, account_id: accountsData[0].id }));
                }
            } catch (err) {
                console.error('Failed to fetch data', err);
            }
        };
        fetchData();
    }, [initialData]);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsDropdownOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log('Submitting transaction data:', formData);
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

    const toggleCategory = (categoryId: number) => {
        setFormData(prev => {
            const currentIds = prev.category_ids || [];
            const newIds = currentIds.includes(categoryId)
                ? currentIds.filter(id => id !== categoryId)
                : [...currentIds, categoryId];
            return { ...prev, category_ids: newIds };
        });
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

    const selectedCategoryNames = categories
        .filter(c => formData.category_ids?.includes(c.id))
        .map(c => c.name)
        .join(', ');

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
                    <option value={0} disabled>Select an account</option>
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

            <div className="relative" ref={dropdownRef}>
                <label className="block text-sm font-medium text-gray-700">Categories</label>
                <div
                    onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border bg-white cursor-pointer flex justify-between items-center min-h-[42px]"
                >
                    <span className="truncate text-sm text-gray-700">
                        {selectedCategoryNames || 'Select categories'}
                    </span>
                    <ChevronDown size={18} className={`text-gray-400 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} />
                </div>

                {isDropdownOpen && (
                    <div className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
                        {categories.map((category) => (
                            <div
                                key={category.id}
                                onClick={() => toggleCategory(category.id)}
                                className="cursor-pointer select-none relative py-2 pl-10 pr-4 hover:bg-blue-50 flex items-center"
                            >
                                <div className="absolute inset-y-0 left-0 flex items-center pl-3">
                                    {formData.category_ids?.includes(category.id) ? (
                                        <Check size={18} className="text-blue-600" />
                                    ) : (
                                        <div className="w-[18px] h-[18px] border border-gray-300 rounded" />
                                    )}
                                </div>
                                <span className={`block truncate ${formData.category_ids?.includes(category.id) ? 'font-medium text-blue-700' : 'font-normal text-gray-900'}`}>
                                    {category.name}
                                </span>
                            </div>
                        ))}
                        {categories.length === 0 && (
                            <div className="py-2 px-4 text-gray-500 italic">No categories available</div>
                        )}
                    </div>
                )}
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
                            <X size={18} />
                        </button>
                    </div>
                ))}
                <button
                    type="button"
                    onClick={addMetadataField}
                    className="text-sm text-blue-600 hover:text-blue-800 flex items-center"
                >
                    <Plus size={16} className="mr-1" /> Add Metadata Field
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
