import React, { useEffect, useState } from 'react';
import { Plus, Edit2, Trash2, FileSpreadsheet } from 'lucide-react';
import { getStatementFormats, createStatementFormat, updateStatementFormat, deleteStatementFormat } from '../api/statement-formats';
import type { StatementFormat, StatementFormatCreate, StatementFormatUpdate } from '../api/statement-formats';
import StatementFormatForm from './StatementFormatForm';
import ConfirmationModal from './ConfirmationModal';

const StatementFormatList: React.FC = () => {
    const [formats, setFormats] = useState<StatementFormat[]>([]);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [editingFormat, setEditingFormat] = useState<StatementFormat | undefined>(undefined);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [deleteId, setDeleteId] = useState<number | null>(null);

    const fetchFormats = async () => {
        try {
            const data = await getStatementFormats();
            setFormats(data);
        } catch (err) {
            setError('Failed to fetch statement formats');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFormats();
    }, []);

    const handleCreate = async (data: StatementFormatCreate) => {
        try {
            await createStatementFormat(data);
            setIsFormOpen(false);
            fetchFormats();
        } catch (err) {
            console.error('Failed to create statement format', err);
            alert('Failed to create statement format');
        }
    };

    const handleUpdate = async (data: StatementFormatUpdate) => {
        if (!editingFormat) return;
        try {
            await updateStatementFormat(editingFormat.id, data);
            setIsFormOpen(false);
            setEditingFormat(undefined);
            fetchFormats();
        } catch (err) {
            console.error('Failed to update statement format', err);
            alert('Failed to update statement format');
        }
    };

    const confirmDelete = (id: number) => {
        setDeleteId(id);
    };

    const handleDelete = async () => {
        if (deleteId === null) return;
        try {
            await deleteStatementFormat(deleteId);
            setDeleteId(null);
            fetchFormats();
        } catch (err) {
            console.error('Failed to delete statement format', err);
            alert('Failed to delete statement format');
        }
    };

    const openCreateForm = () => {
        setEditingFormat(undefined);
        setIsFormOpen(true);
    };

    const openEditForm = (format: StatementFormat) => {
        setEditingFormat(format);
        setIsFormOpen(true);
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="text-red-500">{error}</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-800">Statement Formats</h2>
                <button
                    onClick={openCreateForm}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <Plus size={20} className="mr-2" />
                    Add Format
                </button>
            </div>

            {isFormOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                        <h3 className="text-xl font-bold mb-4">
                            {editingFormat ? 'Edit Statement Format' : 'New Statement Format'}
                        </h3>
                        <StatementFormatForm
                            initialData={editingFormat}
                            onSubmit={(data) => editingFormat ? handleUpdate(data as StatementFormatUpdate) : handleCreate(data as StatementFormatCreate)}
                            onCancel={() => setIsFormOpen(false)}
                        />
                    </div>
                </div>
            )}

            <ConfirmationModal
                isOpen={deleteId !== null}
                title="Delete Statement Format"
                message="Are you sure you want to delete this statement format? This action cannot be undone."
                onConfirm={handleDelete}
                onCancel={() => setDeleteId(null)}
            />

            {formats.length === 0 ? (
                <div className="bg-white p-12 rounded-lg shadow-sm border border-gray-200 text-center">
                    <FileSpreadsheet size={48} className="mx-auto text-gray-400 mb-4" />
                    <h3 className="text-lg font-semibold text-gray-700 mb-2">No Statement Formats</h3>
                    <p className="text-gray-500 mb-4">Get started by creating your first statement format configuration.</p>
                    <button
                        onClick={openCreateForm}
                        className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        <Plus size={20} className="mr-2" />
                        Add Format
                    </button>
                </div>
            ) : (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {formats.map((format) => (
                        <div key={format.id} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                            <div className="flex justify-between items-start mb-4">
                                <div className="flex-1">
                                    <h3 className="text-lg font-semibold text-gray-900">{format.format_name}</h3>
                                    {format.bank_name && (
                                        <p className="text-sm text-gray-500">{format.bank_name}</p>
                                    )}
                                </div>
                            </div>

                            <div className="space-y-2 mb-4 text-sm">
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Start Row:</span>
                                    <span className="font-medium text-gray-900">{format.data_start_row}</span>
                                </div>
                                <div className="grid grid-cols-2 gap-2 pt-2 border-t">
                                    <div>
                                        <span className="text-gray-600 block text-xs">Date:</span>
                                        <span className="font-mono text-xs bg-gray-100 px-1 py-0.5 rounded">{format.date_column}</span>
                                    </div>
                                    <div>
                                        <span className="text-gray-600 block text-xs">Narration:</span>
                                        <span className="font-mono text-xs bg-gray-100 px-1 py-0.5 rounded">{format.narration_column}</span>
                                    </div>
                                    <div>
                                        <span className="text-gray-600 block text-xs">Withdrawal:</span>
                                        <span className="font-mono text-xs bg-gray-100 px-1 py-0.5 rounded">{format.withdrawal_column}</span>
                                    </div>
                                    <div>
                                        <span className="text-gray-600 block text-xs">Deposit:</span>
                                        <span className="font-mono text-xs bg-gray-100 px-1 py-0.5 rounded">{format.deposit_column}</span>
                                    </div>
                                </div>
                            </div>

                            <div className="flex justify-end space-x-2 pt-4 border-t">
                                <button
                                    onClick={() => openEditForm(format)}
                                    className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
                                >
                                    <Edit2 size={18} />
                                </button>
                                <button
                                    onClick={() => confirmDelete(format.id)}
                                    className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                                >
                                    <Trash2 size={18} />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default StatementFormatList;
