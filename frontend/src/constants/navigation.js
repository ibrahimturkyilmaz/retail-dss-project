import {
    HomeIcon,
    ShoppingBagIcon,
    TruckIcon,
    ChartBarIcon,
    Cog6ToothIcon,
    BoltIcon
} from '@heroicons/react/24/outline';

// Menü yapısını buradan kolayca değiştirebilirsiniz.
export const NAVIGATION_ITEMS = [
    {
        name: 'Genel Bakış',
        path: '/',
        icon: HomeIcon,
    },
    {
        name: 'Simülasyon',
        path: '/simulations',
        icon: BoltIcon,
    },
    {
        name: 'Mağazalar',
        path: '/stores',
        icon: ShoppingBagIcon,
    },
    {
        name: 'Transferler',
        path: '/transfers',
        icon: TruckIcon,
    },
    {
        name: 'Analizler',
        path: '/analytics',
        icon: ChartBarIcon,
    },
];

export const BOTTOM_NAVIGATION_ITEMS = [
    {
        name: 'Ayarlar',
        path: '/settings',
        icon: Cog6ToothIcon,
    },
];
