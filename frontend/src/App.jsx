import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import Dashboard from './pages/Dashboard';
import Stores from './pages/Stores';
import Transfers from './pages/Transfers';
import Simulations from './pages/Simulations';

// Placeholder Pages
const Analytics = () => <div className="p-4 bg-white rounded-lg shadow">Analizler (Yapım Aşamasında)</div>;
const Settings = () => <div className="p-4 bg-white rounded-lg shadow">Ayarlar (Yapım Aşamasında)</div>;

function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardLayout />}>
        {/* Ana sayfa dashboard'a yönlensin (veya direkt dashboard component render edilsin) */}
        <Route index element={<Dashboard />} />

        <Route path="simulations" element={<Simulations />} />
        <Route path="stores" element={<Stores />} />
        <Route path="transfers" element={<Transfers />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="settings" element={<Settings />} />

        {/* 404 - Redirect to Dashboard */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

export default App;
