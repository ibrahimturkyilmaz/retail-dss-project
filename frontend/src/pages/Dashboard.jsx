import React from 'react';
import { useDashboardStats, useRecentSales } from '../hooks/useDashboard';
import { ArrowTrendingUpIcon, CurrencyDollarIcon, ShoppingBagIcon } from '@heroicons/react/24/outline';

const StatCard = ({ title, value, icon: Icon, colorClass }) => (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
        <div className="flex items-center justify-between">
            <div>
                <p className="text-slate-500 text-sm font-medium">{title}</p>
                <p className="text-2xl font-bold text-slate-800 mt-2">{value}</p>
            </div>
            <div className={`p-3 rounded-xl ${colorClass}`}>
                <Icon className="w-6 h-6 text-white" />
            </div>
        </div>
        <div className="mt-4 flex items-center text-sm text-green-500">
            <ArrowTrendingUpIcon className="w-4 h-4 mr-1" />
            <span>Artış Trendi</span>
        </div>
    </div>
);

const Dashboard = () => {
    const { data: stats, isLoading: statsLoading } = useDashboardStats();
    const { data: recentSales, isLoading: salesLoading } = useRecentSales();

    if (statsLoading || salesLoading) {
        return <div className="p-8 text-center text-slate-500 animate-pulse">Panel verileri yükleniyor...</div>;
    }

    return (
        <div className="space-y-6">
            {/* Header Area */}
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-xl font-bold text-slate-800">Genel Bakış</h2>
                    <p className="text-sm text-slate-500">Mağaza performans özetiniz.</p>
                </div>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors shadow-sm shadow-blue-200">
                    Rapor İndir
                </button>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatCard
                    title="Toplam Ciro"
                    value={`₺${stats?.total_revenue?.toLocaleString('tr-TR', { maximumFractionDigits: 0 })}`}
                    icon={CurrencyDollarIcon}
                    colorClass="bg-gradient-to-br from-green-400 to-green-600"
                />
                <StatCard
                    title="Toplam İşlem"
                    value={stats?.total_transactions?.toLocaleString('tr-TR')}
                    icon={ShoppingBagIcon}
                    colorClass="bg-gradient-to-br from-blue-400 to-blue-600"
                />
                <StatCard
                    title="En Çok Satan"
                    value={stats?.top_selling_product}
                    icon={ArrowTrendingUpIcon}
                    colorClass="bg-gradient-to-br from-purple-400 to-purple-600"
                />
            </div>

            {/* Recent Sales Table */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                <div className="p-6 border-b border-slate-50 flex justify-between items-center">
                    <h3 className="font-bold text-slate-800">Son Satışlar</h3>
                    <button className="text-sm text-blue-500 hover:text-blue-700 font-medium">Tümünü Gör</button>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead className="bg-slate-50 text-slate-500 text-xs uppercase font-semibold">
                            <tr>
                                <th className="px-6 py-4">Ürün</th>
                                <th className="px-6 py-4">Mağaza</th>
                                <th className="px-6 py-4">Müşteri</th>
                                <th className="px-6 py-4">Tutar</th>
                                <th className="px-6 py-4">Tarih</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {recentSales?.map((sale) => (
                                <tr key={sale.id} className="hover:bg-slate-50/50 transition-colors">
                                    <td className="px-6 py-4 text-sm font-medium text-slate-700">{sale.product_name}</td>
                                    <td className="px-6 py-4 text-xs text-slate-500">{sale.store_name}</td>
                                    <td className="px-6 py-4 text-xs text-slate-500">{sale.customer_name}</td>
                                    <td className="px-6 py-4 text-sm font-bold text-slate-800">
                                        ₺{sale.total_price.toLocaleString('tr-TR')}
                                    </td>
                                    <td className="px-6 py-4 text-xs text-slate-400">
                                        {new Date(sale.date).toLocaleDateString('tr-TR')}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
