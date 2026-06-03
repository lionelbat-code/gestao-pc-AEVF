import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// TODO: Importar páginas e componentes quando existirem

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar autenticação ao carregar
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Carregando...</div>;
  }

  return (
    <Router>
      <Routes>
        {/* Rotas públicas */}
        <Route path="/login" element={<div>Login - Em Desenvolvimento</div>} />
        
        {/* Rotas protegidas */}
        {isAuthenticated ? (
          <>
            <Route path="/dashboard" element={<div>Dashboard - Em Desenvolvimento</div>} />
            <Route path="/alunos" element={<div>Alunos - Em Desenvolvimento</div>} />
            <Route path="/computadores" element={<div>Computadores - Em Desenvolvimento</div>} />
            <Route path="/emprestimos" element={<div>Empréstimos - Em Desenvolvimento</div>} />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </>
        ) : (
          <Route path="*" element={<Navigate to="/login" />} />
        )}
      </Routes>
    </Router>
  );
}

export default App;