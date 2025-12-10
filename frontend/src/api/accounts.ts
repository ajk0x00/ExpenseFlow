import axios from 'axios';

const API_URL = '/api/v1/accounts';

export interface BankAccount {
    id: number;
    account_name: string;
    bank_name: string;
    description?: string;
    account_type: 'credit' | 'debit';
    metadata_?: Record<string, any>;
}

// Type alias for convenience
export type Account = BankAccount;

export interface BankAccountCreate {
    account_name: string;
    bank_name: string;
    description?: string;
    account_type: 'credit' | 'debit';
    metadata_?: Record<string, any>;
}

export interface BankAccountUpdate {
    account_name?: string;
    bank_name?: string;
    description?: string;
    account_type?: 'credit' | 'debit';
    metadata_?: Record<string, any>;
}

export const getAccounts = async (): Promise<BankAccount[]> => {
    const response = await axios.get(API_URL + '/');
    return response.data;
};

export const createAccount = async (account: BankAccountCreate): Promise<BankAccount> => {
    const response = await axios.post(API_URL + '/', account);
    return response.data;
};

export const updateAccount = async (id: number, account: BankAccountUpdate): Promise<BankAccount> => {
    const response = await axios.put(`${API_URL}/${id}`, account);
    return response.data;
};

export const deleteAccount = async (id: number): Promise<BankAccount> => {
    const response = await axios.delete(`${API_URL}/${id}`);
    return response.data;
};
