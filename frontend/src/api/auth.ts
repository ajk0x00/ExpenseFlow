import client from './client';

export const login = async (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await client.post('/auth/jwt/login', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });
    return response.data;
};

export const getMe = async () => {
    // There isn't a dedicated /users/me in the default fastapi-users setup unless configured, 
    // but usually /users/{id} or similar. 
    // Wait, fastapi-users has /users/me if configured. 
    // Let's assume we might need it later, but for now strict login is enough.
    // Actually, checking if token is valid often involves calling a protected endpoint.
    // Let's use /users/me if available or just rely on local storage for now.
    // The previous implementation plan didn't strictly require getMe, but it helps for "isAuthenticated" check.
    // Let's check api.py... Use /users/me
    const response = await client.get('/users/me');
    return response.data;
};
