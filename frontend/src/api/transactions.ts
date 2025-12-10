import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export interface Transaction {
    id: number;
    account_id: number;
    date: string;
    narration: string;
    withdrawal_amount: number;
    deposit_amount: number;
    metadata_?: Record<string, any>;
}

export interface TransactionCreate {
    account_id: number;
    date: string;
    narration: string;
    withdrawal_amount?: number;
    deposit_amount?: number;
    metadata_?: Record<string, any>;
}

export interface TransactionUpdate {
    account_id?: number;
    date?: string;
    narration?: string;
    withdrawal_amount?: number;
    deposit_amount?: number;
    metadata_?: Record<string, any>;
}

export interface UploadResult {
    success: boolean;
    count: number;
    total_withdrawals: number;
    total_deposits: number;
    net: number;
}

export const getTransactions = async (skip = 0, limit = 100): Promise<Transaction[]> => {
    const response = await axios.get(`${API_URL}/transactions/`, {
        params: { skip, limit }
    });
    return response.data;
};

export const createTransaction = async (data: TransactionCreate): Promise<Transaction> => {
    const response = await axios.post(`${API_URL}/transactions/`, data);
    return response.data;
};

export const updateTransaction = async (id: number, data: TransactionUpdate): Promise<Transaction> => {
    const response = await axios.put(`${API_URL}/transactions/${id}`, data);
    return response.data;
};

export const deleteTransaction = async (id: number): Promise<Transaction> => {
    const response = await axios.delete(`${API_URL}/transactions/${id}`);
    return response.data;
};

export const uploadTransactions = async (
    file: File,
    statementFormatId: number,
    accountId: number
): Promise<UploadResult> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('statement_format_id', statementFormatId.toString());
    formData.append('account_id', accountId.toString());

    const response = await axios.post(`${API_URL}/transactions/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

