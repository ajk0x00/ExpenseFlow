import React, { useState, useEffect } from 'react';
import type { StatementFormat, StatementFormatCreate, StatementFormatUpdate } from '../api/statement-formats';

interface StatementFormatFormProps {
    initialData?: StatementFormat;
    onSubmit: (data: StatementFormatCreate | StatementFormatUpdate) => void;
    onCancel: () => void;
}

const StatementFormatForm: React.FC<StatementFormatFormProps> = ({ initialData, onSubmit, onCancel }) => {
    const [formData, setFormData] = useState<StatementFormatCreate>({
        format_name: '',
        bank_name: '',
        data_start_row: 1,
        date_column: '',
        narration_column: '',
        withdrawal_column: '',
        deposit_column: '',
    });

    useEffect(() => {
        if (initialData) {
            setFormData({
                format_name: initialData.format_name,
                bank_name: initialData.bank_name || '',
                data_start_row: initialData.data_start_row,
                date_column: initialData.date_column,
                narration_column: initialData.narration_column,
                withdrawal_column: initialData.withdrawal_column,
                deposit_column: initialData.deposit_column,
            });
        }
    }, [initialData]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'data_start_row' ? parseInt(value) || 1 : value
        }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label className="block text-sm font-medium text-gray-700">Format Name *</label>
                <input
                    type="text"
                    name="format_name"
                    value={formData.format_name}
                    onChange={handleChange}
                    required
                    placeholder="e.g., ICICI Savings Account Format"
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
                    placeholder="e.g., ICICI Bank"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Data Start Row *</label>
                <input
                    type="number"
                    name="data_start_row"
                    value={formData.data_start_row}
                    onChange={handleChange}
                    required
                    min="1"
                    placeholder="e.g., 15"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                />
                <p className="mt-1 text-xs text-gray-500">Row number where transaction data begins (1-indexed)</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Date Column *</label>
                    <input
                        type="text"
                        name="date_column"
                        value={formData.date_column}
                        onChange={handleChange}
                        required
                        placeholder="e.g., A, Date, or 0"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                    />
                    <p className="mt-1 text-xs text-gray-500">Column letter, name, or index</p>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Narration Column *</label>
                    <input
                        type="text"
                        name="narration_column"
                        value={formData.narration_column}
                        onChange={handleChange}
                        required
                        placeholder="e.g., B, Narration, or 1"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                    />
                    <p className="mt-1 text-xs text-gray-500">Column letter, name, or index</p>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Withdrawal Column *</label>
                    <input
                        type="text"
                        name="withdrawal_column"
                        value={formData.withdrawal_column}
                        onChange={handleChange}
                        required
                        placeholder="e.g., C, Withdrawal, or 2"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                    />
                    <p className="mt-1 text-xs text-gray-500">Column letter, name, or index</p>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Deposit Column *</label>
                    <input
                        type="text"
                        name="deposit_column"
                        value={formData.deposit_column}
                        onChange={handleChange}
                        required
                        placeholder="e.g., D, Deposit, or 3"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                    />
                    <p className="mt-1 text-xs text-gray-500">Column letter, name, or index</p>
                </div>
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
                    {initialData ? 'Update Format' : 'Create Format'}
                </button>
            </div>
        </form>
    );
};

export default StatementFormatForm;
