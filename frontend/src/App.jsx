import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { UIProvider } from './context/UIContext';
import ProtectedRoute from './components/ProtectedRoute';
import DashboardLayout from './layouts/DashboardLayout';

// Lazy Load Pages for Performance
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Login = lazy(() => import('./pages/Login'));
const Stores = lazy(() => import('./pages/Stores'));
const Transfers = lazy(() => import('./pages/Transfers'));
const Simulations = lazy(() => import('./pages/Simulations'));
const Analytics = lazy(() => import('./pages/Analytics'));
const Settings = lazy(() => import('./pages/Settings'));
const SqlPlayground = lazy(() => import('./components/SqlPlayground'));
const VideoMeeting = lazy(() => import('./components/VideoMeeting'));

// Loading Component
const PageLoader = () => (
  <div className="flex items-center justify-center min-h-[400px] w-full">
    <div className="relative">
      <div className="w-12 h-12 rounded-full absolute border-4 border-gray-100"></div>
      <div className="w-12 h-12 rounded-full animate-spin absolute border-4 border-indigo-600 border-t-transparent"></div>
    </div>
  </div>
);

function App() {
  return (
    <AuthProvider>
      <UIProvider>
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/login" element={<Login />} />

            <Route path="/" element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }>
              <Route index element={<Dashboard />} />
              <Route path="simulations" element={<Simulations />} />
              <Route path="stores" element={<Stores />} />
              <Route path="transfers" element={<Transfers />} />
              <Route path="analytics" element={<Analytics />} />
              <Route path="playground" element={<SqlPlayground />} />
              <Route path="settings" element={<Settings />} />
              <Route path="meeting" element={<VideoMeeting />} />

              {/* 404 - Redirect to Dashboard */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </Suspense>
      </UIProvider>
    </AuthProvider>
  );
}

export default App;
