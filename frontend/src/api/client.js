import axios from 'axios';

export const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});

apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('roboPulseToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default apiClient;
