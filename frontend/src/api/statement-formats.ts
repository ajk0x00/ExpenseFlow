import axios from 'axios';

const API_URL = '/api/v1/statement-formats';

export interface StatementFormat {
    id: number;
    format_name: string;
    bank_name?: string;
    data_start_row: number;
    date_column: string;
    narration_column: string;
    withdrawal_column: string;
    deposit_column: string;
    created_at: string;
    updated_at: string;
}

export interface StatementFormatCreate {
    format_name: string;
    bank_name?: string;
    data_start_row: number;
    date_column: string;
    narration_column: string;
    withdrawal_column: string;
    deposit_column: string;
}

export interface StatementFormatUpdate {
    format_name?: string;
    bank_name?: string;
    data_start_row?: number;
    date_column?: string;
    narration_column?: string;
    withdrawal_column?: string;
    deposit_column?: string;
}

export const getStatementFormats = async (): Promise<StatementFormat[]> => {
    const response = await axios.get(API_URL + '/');
    return response.data;
};

export const getStatementFormat = async (id: number): Promise<StatementFormat> => {
    const response = await axios.get(`${API_URL}/${id}`);
    return response.data;
};

export const createStatementFormat = async (format: StatementFormatCreate): Promise<StatementFormat> => {
    const response = await axios.post(API_URL + '/', format);
    return response.data;
};

export const updateStatementFormat = async (id: number, format: StatementFormatUpdate): Promise<StatementFormat> => {
    const response = await axios.put(`${API_URL}/${id}`, format);
    return response.data;
};

export const deleteStatementFormat = async (id: number): Promise<StatementFormat> => {
    const response = await axios.delete(`${API_URL}/${id}`);
    return response.data;
};
