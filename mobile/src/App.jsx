import { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import BottomNav from './components/layout/BottomNav';
import HomeScreen from './components/screens/HomeScreen';
import ShopScreen from './components/screens/ShopScreen';
import ProfileScreen from './components/screens/ProfileScreen';
import ProfileSetupScreen from './components/screens/ProfileSetupScreen';
import NotificationOverlay from './components/ui/NotificationOverlay';
import StatusBar from './components/ui/StatusBar';
import SplashScreen from './components/ui/SplashScreen';
import LoginScreen from './components/screens/LoginScreen';
import FavoritesScreen from './components/screens/FavoritesScreen';
import CartScreen from './components/screens/CartScreen';
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
  const [showProfileSetup, setShowProfileSetup] = useState(false);

  const { notification, dismissNotification, simulateEnterRegion, simulateInStore } = useGeofencing(stores);

  // Restore Session Logic — also handle Google OAuth redirect
  useEffect(() => {
    if (!loading && user) {
      setShowLogin(false);
      // If backend returned is_new_user (new Google customer), show profile setup
      if (user.is_new_user && !showProfileSetup) {
        setShowProfileSetup(true);
      }
    }
  }, [user, loading]);

  useEffect(() => {
    const initData = () => {
      setProducts(mockProducts);
      setStores(mockStores);
    };
    initData();
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen bg-gray-50">Yükleniyor...</div>;
  }

  const handleLogin = (userData) => {
    login(userData);
    setShowLogin(false);

    // If new user, show profile setup
    if (userData.is_new_user) {
      setShowProfileSetup(true);
    } else {
      setShowSplash(true);
    }
  };

  const handleProfileSetupComplete = () => {
    setShowProfileSetup(false);
    setShowSplash(true);
  };

  const handleSplashComplete = () => {
    setShowSplash(false);
  };

  const handleEditProfile = () => {
    setShowProfileSetup(true);
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
            onEditProfile={handleEditProfile}
          />
        );
      default:
        return <HomeScreen user={user} />;
    }
  };

  if (showLogin) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  if (showProfileSetup) {
    return <ProfileSetupScreen onComplete={handleProfileSetupComplete} />;
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
