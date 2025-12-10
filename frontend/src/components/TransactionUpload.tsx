import React, { useState, useEffect } from 'react';
import { Upload, X, FileSpreadsheet, CheckCircle } from 'lucide-react';
import { uploadTransactions, type UploadResult } from '../api/transactions';
import { getStatementFormats, type StatementFormat } from '../api/statement-formats';
import { getAccounts, type Account } from '../api/accounts';

interface TransactionUploadProps {
    onSuccess: () => void;
    onCancel: () => void;
}

const TransactionUpload: React.FC<TransactionUploadProps> = ({ onSuccess, onCancel }) => {
    const [file, setFile] = useState<File | null>(null);
    const [statementFormats, setStatementFormats] = useState<StatementFormat[]>([]);
    const [accounts, setAccounts] = useState<Account[]>([]);
    const [selectedFormatId, setSelectedFormatId] = useState<number | ''>('');
    const [selectedAccountId, setSelectedAccountId] = useState<number | ''>('');
    const [uploading, setUploading] = useState(false);
    const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [formatsData, accountsData] = await Promise.all([
                getStatementFormats(),
                getAccounts()
            ]);
            setStatementFormats(formatsData);
            setAccounts(accountsData);
        } catch (err) {
            setError('Failed to load data');
            console.error(err);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {
            // Validate file type
            if (!selectedFile.name.endsWith('.xls') && !selectedFile.name.endsWith('.xlsx')) {
                setError('Please select a valid Excel file (.xls or .xlsx)');
                return;
            }
            setFile(selectedFile);
            setError('');
        }
    };

    const handleUpload = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!file) {
            setError('Please select a file');
            return;
        }

        if (!selectedFormatId) {
            setError('Please select a statement format');
            return;
        }

        if (!selectedAccountId) {
            setError('Please select an account');
            return;
        }

        setUploading(true);
        setError('');

        try {
            const result = await uploadTransactions(
                file,
                Number(selectedFormatId),
                Number(selectedAccountId)
            );
            setUploadResult(result);

            // Auto-close after successful upload
            setTimeout(() => {
                onSuccess();
            }, 3000);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to upload file');
            console.error(err);
        } finally {
            setUploading(false);
        }
    };

    const selectedFormat = statementFormats.find(f => f.id === selectedFormatId);

    return (
        <div className="bg-white rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold text-gray-800">Upload Bank Statement</h3>
                <button
                    onClick={onCancel}
                    className="text-gray-400 hover:text-gray-600"
                >
                    <X size={24} />
                </button>
            </div>

            {uploadResult ? (
                <div className="space-y-6">
                    <div className="flex items-center justify-center text-green-600 mb-4">
                        <CheckCircle size={64} />
                    </div>
                    <div className="text-center">
                        <h4 className="text-xl font-bold text-gray-800 mb-4">Upload Successful!</h4>
                        <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                            <div className="flex justify-between">
                                <span className="text-gray-600">Transactions Imported:</span>
                                <span className="font-bold">{uploadResult.count}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Total Withdrawals:</span>
                                <span className="font-bold text-red-600">₹{uploadResult.total_withdrawals.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Total Deposits:</span>
                                <span className="font-bold text-green-600">₹{uploadResult.total_deposits.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
                            </div>
                            <div className="flex justify-between border-t pt-2 mt-2">
                                <span className="text-gray-600">Net Amount:</span>
                                <span className={`font-bold ${uploadResult.net >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                    ₹{uploadResult.net.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            ) : (
                <form onSubmit={handleUpload} className="space-y-6">
                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                            {error}
                        </div>
                    )}

                    {/* Account Selection */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Bank Account <span className="text-red-500">*</span>
                        </label>
                        <select
                            value={selectedAccountId}
                            onChange={(e) => setSelectedAccountId(e.target.value ? Number(e.target.value) : '')}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            required
                        >
                            <option value="">Select an account</option>
                            {accounts.map((account) => (
                                <option key={account.id} value={account.id}>
                                    {account.account_name} - {account.bank_name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Statement Format Selection */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Statement Format <span className="text-red-500">*</span>
                        </label>
                        <select
                            value={selectedFormatId}
                            onChange={(e) => setSelectedFormatId(e.target.value ? Number(e.target.value) : '')}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            required
                        >
                            <option value="">Select a format</option>
                            {statementFormats.map((format) => (
                                <option key={format.id} value={format.id}>
                                    {format.format_name} {format.bank_name && `(${format.bank_name})`}
                                </option>
                            ))}
                        </select>
                        {selectedFormat && (
                            <div className="mt-2 p-3 bg-blue-50 rounded text-sm text-gray-600">
                                <div className="font-medium mb-1">Format Details:</div>
                                <div>Data starts at row: {selectedFormat.data_start_row}</div>
                                <div>Columns: Date={selectedFormat.date_column}, Narration={selectedFormat.narration_column}</div>
                            </div>
                        )}
                    </div>

                    {/* File Upload */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Statement File <span className="text-red-500">*</span>
                        </label>
                        <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-blue-400 transition-colors">
                            <div className="space-y-1 text-center">
                                {file ? (
                                    <div className="flex items-center justify-center space-x-2">
                                        <FileSpreadsheet className="text-green-600" size={40} />
                                        <div>
                                            <p className="text-sm font-medium text-gray-900">{file.name}</p>
                                            <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
                                        </div>
                                    </div>
                                ) : (
                                    <>
                                        <Upload className="mx-auto text-gray-400" size={40} />
                                        <div className="flex text-sm text-gray-600">
                                            <label
                                                htmlFor="file-upload"
                                                className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500"
                                            >
                                                <span>Upload a file</span>
                                                <input
                                                    id="file-upload"
                                                    name="file-upload"
                                                    type="file"
                                                    className="sr-only"
                                                    accept=".xls,.xlsx"
                                                    onChange={handleFileChange}
                                                />
                                            </label>
                                            <p className="pl-1">or drag and drop</p>
                                        </div>
                                        <p className="text-xs text-gray-500">Excel files only (.xls, .xlsx)</p>
                                    </>
                                )}
                            </div>
                        </div>
                        {file && (
                            <button
                                type="button"
                                onClick={() => setFile(null)}
                                className="mt-2 text-sm text-red-600 hover:text-red-800"
                            >
                                Remove file
                            </button>
                        )}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex justify-end space-x-3 pt-4">
                        <button
                            type="button"
                            onClick={onCancel}
                            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                            disabled={uploading}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
                            disabled={uploading || !file || !selectedFormatId || !selectedAccountId}
                        >
                            {uploading ? (
                                <>
                                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Uploading...
                                </>
                            ) : (
                                <>
                                    <Upload size={18} className="mr-2" />
                                    Upload & Import
                                </>
                            )}
                        </button>
                    </div>
                </form>
            )}
        </div>
    );
};

export default TransactionUpload;
