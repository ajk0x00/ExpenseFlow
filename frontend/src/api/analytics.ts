import axios from 'axios';
import { API_URL } from './client';

export interface ExpenseByCategory {
    category_name: string;
    amount: number;
    percentage: number;
}

export interface ExpensesByCategoryResponse {
    items: ExpenseByCategory[];
    total_amount: number;
}

export interface ExpenseOverTime {
    date: string;
    amount: number;
}

export const getExpensesByCategory = async (startDate?: string, endDate?: string): Promise<ExpensesByCategoryResponse> => {
    const response = await axios.get<ExpensesByCategoryResponse>(`${API_URL}/analytics/expenses-by-category`, {
        params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
};

export const getExpensesOverTime = async (startDate?: string, endDate?: string): Promise<ExpenseOverTime[]> => {
    const response = await axios.get<ExpenseOverTime[]>(`${API_URL}/analytics/expenses-over-time`, {
        params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
};
