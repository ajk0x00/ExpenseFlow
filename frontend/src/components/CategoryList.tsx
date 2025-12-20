import React, { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, X } from 'lucide-react';
import { getCategories, createCategory, updateCategory, deleteCategory } from '../api/categories';
import type { Category } from '../api/categories';
import CategoryForm from './CategoryForm';
import ConfirmationModal from './ConfirmationModal';

const CategoryList: React.FC = () => {
    const [categories, setCategories] = useState<Category[]>([]);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [editingCategory, setEditingCategory] = useState<Category | undefined>(undefined);
    const [deleteConfirmation, setDeleteConfirmation] = useState<{ isOpen: boolean; categoryId: number | null }>({
        isOpen: false,
        categoryId: null
    });
    const [error, setError] = useState<string | null>(null);

    const fetchCategories = async () => {
        try {
            const data = await getCategories();
            setCategories(data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch categories');
            console.error(err);
        }
    };

    useEffect(() => {
        fetchCategories();
    }, []);

    const handleCreate = async (data: any) => {
        try {
            await createCategory(data);
            setIsFormOpen(false);
            fetchCategories();
        } catch (err) {
            setError('Failed to create category');
            console.error(err);
        }
    };

    const handleUpdate = async (data: any) => {
        if (!editingCategory) return;
        try {
            await updateCategory(editingCategory.id, data);
            setEditingCategory(undefined);
            setIsFormOpen(false);
            fetchCategories();
        } catch (err) {
            setError('Failed to update category');
            console.error(err);
        }
    };

    const handleDelete = async () => {
        if (deleteConfirmation.categoryId) {
            try {
                await deleteCategory(deleteConfirmation.categoryId);
                setDeleteConfirmation({ isOpen: false, categoryId: null });
                fetchCategories();
            } catch (err) {
                setError('Failed to delete category');
                console.error(err);
            }
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-800">Categories</h2>
                <button
                    onClick={() => {
                        setEditingCategory(undefined);
                        setIsFormOpen(true);
                    }}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <Plus size={20} className="mr-2" />
                    Add Category
                </button>
            </div>

            {error && (
                <div className="bg-red-50 border-l-4 border-red-500 p-4">
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <X className="h-5 w-5 text-red-400" aria-hidden="true" />
                        </div>
                        <div className="ml-3">
                            <p className="text-sm text-red-700">{error}</p>
                        </div>
                    </div>
                </div>
            )}

            {isFormOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg p-6 w-full max-w-md">
                        <h3 className="text-lg font-medium text-gray-900 mb-4">
                            {editingCategory ? 'Edit Category' : 'New Category'}
                        </h3>
                        <CategoryForm
                            initialData={editingCategory}
                            onSubmit={editingCategory ? handleUpdate : handleCreate}
                            onCancel={() => {
                                setIsFormOpen(false);
                                setEditingCategory(undefined);
                            }}
                        />
                    </div>
                </div>
            )}

            <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {categories.map((category) => (
                            <tr key={category.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                    {category.name}
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-500">
                                    {category.description}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button
                                        onClick={() => {
                                            setEditingCategory(category);
                                            setIsFormOpen(true);
                                        }}
                                        className="text-blue-600 hover:text-blue-900 mr-4"
                                    >
                                        <Edit2 size={18} />
                                    </button>
                                    <button
                                        onClick={() => setDeleteConfirmation({ isOpen: true, categoryId: category.id })}
                                        className="text-red-600 hover:text-red-900"
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {categories.length === 0 && (
                            <tr>
                                <td colSpan={3} className="px-6 py-4 text-center text-sm text-gray-500">
                                    No categories found. Create one to get started.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            <ConfirmationModal
                isOpen={deleteConfirmation.isOpen}
                onCancel={() => setDeleteConfirmation({ isOpen: false, categoryId: null })}
                onConfirm={handleDelete}
                title="Delete Category"
                message="Are you sure you want to delete this category? This action cannot be undone."
            />
        </div>
    );
};

export default CategoryList;
