import { API_URL } from './client';

export interface Category {
    id: number;
    name: string;
    description?: string;
}

export interface CategoryCreate {
    name: string;
    description?: string;
}

export interface CategoryUpdate {
    name?: string;
    description?: string;
}

export const getCategories = async (): Promise<Category[]> => {
    const response = await fetch(`${API_URL}/categories/`);
    if (!response.ok) {
        throw new Error('Failed to fetch categories');
    }
    return response.json();
};

export const createCategory = async (data: CategoryCreate): Promise<Category> => {
    const response = await fetch(`${API_URL}/categories/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error('Failed to create category');
    }
    return response.json();
};

export const updateCategory = async (id: number, data: CategoryUpdate): Promise<Category> => {
    const response = await fetch(`${API_URL}/categories/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error('Failed to update category');
    }
    return response.json();
};

export const deleteCategory = async (id: number): Promise<Category> => {
    const response = await fetch(`${API_URL}/categories/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Failed to delete category');
    }
    return response.json();
};
