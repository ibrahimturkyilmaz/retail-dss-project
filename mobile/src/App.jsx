import { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import BottomNav from './components/layout/BottomNav';
import HomeScreen from './components/screens/HomeScreen';
import ShopScreen from './components/screens/ShopScreen';
import ProfileScreen from './components/screens/ProfileScreen';
import NotificationOverlay from './components/ui/NotificationOverlay';
import StatusBar from './components/ui/StatusBar';
import SplashScreen from './components/ui/SplashScreen';
import LoginScreen from './components/screens/LoginScreen';
import FavoritesScreen from './components/screens/FavoritesScreen';
import CartScreen from './components/screens/CartScreen';
// import { api } from './services/api'; // Legacy API removed
import { mockProducts, mockStores } from './data/mockData';
import { useGeofencing } from './hooks/useGeofencing';
import { LocationProvider } from './context/LocationContext';
import { UserProvider, useUser } from './context/UserContext';
import { CartProvider } from './context/CartContext';
import { FavoritesProvider } from './context/FavoritesContext';

function MainLayout() {
  const { user, login, loading } = useUser();
  const [activeTab, setActiveTab] = useState('home');
  const [products, setProducts] = useState([]);
  const [stores, setStores] = useState([]);
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);

  // App Flow State
  const [showSplash, setShowSplash] = useState(false);
  const [showLogin, setShowLogin] = useState(true);

  const { notification, dismissNotification, simulateEnterRegion, simulateInStore } = useGeofencing(stores);

  // Restore Session Logic
  useEffect(() => {
    if (!loading && user) {
      setShowLogin(false);
    }
  }, [user, loading]);

  useEffect(() => {
    // Load local mock data
    const initData = () => {
      setProducts(mockProducts);
      setStores(mockStores);
    };

    initData();
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen bg-gray-50">Yükleniyor...</div>;
  }

  const handleLogin = (user) => {
    login(user);
    setShowLogin(false);
    setShowSplash(true);
  };

  const handleSplashComplete = () => {
    setShowSplash(false);
  };

  const renderScreen = () => {
    switch (activeTab) {
      case 'home':
        return (
          <HomeScreen
            user={user}
            onSimulateEnter={() => simulateEnterRegion('store_001')}
            onSimulateInStore={simulateInStore}
            onNavigateToShop={() => setActiveTab('shop')}
            onNavigateToProfile={() => setActiveTab('profile')}
          />
        );
      case 'shop':
        return <ShopScreen products={products} />;
      case 'favorites':
        return <FavoritesScreen />;
      case 'cart':
        return <CartScreen />;
      case 'profile':
        return (
          <ProfileScreen
            notificationsEnabled={notificationsEnabled}
            setNotificationsEnabled={setNotificationsEnabled}
          />
        );
      default:
        return <HomeScreen user={user} />;
    }
  };

  if (showLogin) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  if (showSplash) {
    return <SplashScreen onComplete={handleSplashComplete} />;
  }

  const statusBarTheme = activeTab === 'profile' ? 'dark' : 'light';

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900 pb-20">
      <NotificationOverlay notification={notification} onClose={dismissNotification} />
      <main className="max-w-md mx-auto min-h-screen bg-white shadow-2xl overflow-hidden relative">
        <StatusBar theme={statusBarTheme} />
        <AnimatePresence mode="wait">
          {renderScreen()}
        </AnimatePresence>
      </main>
      <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
  );
}

export default function App() {
  return (
    <UserProvider>
      <LocationProvider>
        <CartProvider>
          <FavoritesProvider>
            <MainLayout />
          </FavoritesProvider>
        </CartProvider>
      </LocationProvider>
    </UserProvider>
  );
}
