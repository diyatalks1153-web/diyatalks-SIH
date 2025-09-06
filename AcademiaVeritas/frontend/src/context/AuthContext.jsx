import React, { createContext, useState, useContext, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState({ token: null, userType: null, userId: null });

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        if (token) {
            try {
                const decoded = jwtDecode(token);
                // Check if token is expired
                if (decoded.exp * 1000 > Date.now()) {
                    setAuth({ token, userType: decoded.user_type, userId: decoded.user_id });
                } else {
                    localStorage.removeItem('authToken');
                }
            } catch (error) {
                localStorage.removeItem('authToken');
            }
        }
    }, []);

    const login = (token) => {
        const decoded = jwtDecode(token);
        localStorage.setItem('authToken', token);
        setAuth({ token, userType: decoded.user_type, userId: decoded.user_id });
    };

    const logout = () => {
        localStorage.removeItem('authToken');
        setAuth({ token: null, userType: null, userId: null });
        // Optionally redirect to home page
        window.location.href = '/';
    };

    return (
        <AuthContext.Provider value={{ auth, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};
