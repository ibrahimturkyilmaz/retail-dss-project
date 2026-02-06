import React, { useState } from 'react';
import axiosClient from '../api/axios';
import {
    ArrowTrendingUpIcon,
    ArrowTrendingDownIcon,
    ExclamationTriangleIcon,
    ArrowPathIcon,
    BoltIcon
} from '@heroicons/react/24/outline';

const SimulationCard = ({ title, description, icon: Icon, colorClass, onClick, isLoading }) => (
    <div
        onClick={!isLoading ? onClick : undefined}
        className={`bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-lg transition-all cursor-pointer group relative overflow-hidden ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
        <div className={`absolute top-0 right-0 w-24 h-24 transform translate-x-8 -translate-y-8 rounded-full opacity-10 ${colorClass}`}></div>

        <div className="relative z-10">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${colorClass} text-white`}>
                <Icon className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">{title}</h3>
            <p className="text-sm text-slate-500">{description}</p>
        </div>
    </div>
);

const LogItem = ({ log }) => (
    <div className="flex items-start space-x-3 p-3 bg-slate-50 rounded-lg border border-slate-100 text-sm animate-in slide-in-from-left-2 duration-300">
        <div className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 
            ${log.type === 'BOOM' ? 'bg-green-500' :
                log.type === 'RECESSION' ? 'bg-orange-500' :
                    log.type === 'SHOCK' ? 'bg-red-500' : 'bg-blue-500'}`}
        />
        <div>
            <span className="text-slate-400 text-xs mr-2">{log.time}</span>
            <span className="text-slate-700 font-medium">{log.message}</span>
        </div>
    </div>
);

const Simulations = () => {
    const [loading, setLoading] = useState(false);
    const [logs, setLogs] = useState([]);
    const [stats, setStats] = useState({ total_revenue: 0, total_stock: 0, critical_stores: 0 });

    const fetchStats = async () => {
        try {
            const { data } = await axiosClient.get('/api/simulate/stats');
            setStats(data);
        } catch (error) {
            console.error("Stats fetch error:", error);
        }
    };

    // İlk açılışta verileri çek
    React.useEffect(() => {
        fetchStats();
    }, []);

    const addLog = (message, type) => {
        const time = new Date().toLocaleTimeString('tr-TR');
        setLogs(prev => [{ message, type, time }, ...prev]);
    };

    const triggerSimulation = async (endpoint, title, type) => {
        if (loading) return;
        setLoading(true);
        addLog(`${title} senaryosu başlatılıyor...`, 'INFO');

        try {
            const { data } = await axiosClient.post(`/api/simulate/${endpoint}`);
            addLog(data.message, type);
            // Simülasyon bitince istatistikleri güncelle
            await fetchStats();
        } catch (error) {
            addLog(`Hata oluştu: ${error.message}`, 'ERROR');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto">
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-800 flex items-center">
                    <BoltIcon className="w-8 h-8 mr-3 text-yellow-500" />
                    Senaryo Simülasyon Merkezi
                </h1>
                <p className="text-slate-500 mt-2">
                    Sistemi zorlu koşullar altında test etmek için "What-If" (Ya olursa?) senaryolarını çalıştırın.
                </p>
            </div>

            {/* Live Indicators */}
            <div className="grid grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
                    <div>
                        <p className="text-xs text-slate-500 uppercase font-bold">Anlık Ciro</p>
                        <p className="text-2xl font-bold text-slate-800">
                            {new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(stats.total_revenue)}
                        </p>
                    </div>
                    <div className="bg-green-100 p-2 rounded-lg text-green-600">
                        <ArrowTrendingUpIcon className="w-6 h-6" />
                    </div>
                </div>
                <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
                    <div>
                        <p className="text-xs text-slate-500 uppercase font-bold">Toplam Stok</p>
                        <p className="text-2xl font-bold text-slate-800">{stats.total_stock.toLocaleString()}</p>
                    </div>
                    <div className="bg-blue-100 p-2 rounded-lg text-blue-600">
                        <ArrowPathIcon className="w-6 h-6" />
                    </div>
                </div>
                <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
                    <div>
                        <p className="text-xs text-slate-500 uppercase font-bold">Kritik Mağaza (Stockout)</p>
                        <p className="text-2xl font-bold text-red-600">{stats.critical_stores}</p>
                    </div>
                    <div className="bg-red-100 p-2 rounded-lg text-red-600">
                        <ExclamationTriangleIcon className="w-6 h-6" />
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <SimulationCard
                    title="Talep Patlaması"
                    description="Satışları %50 artır, stokları erit."
                    icon={ArrowTrendingUpIcon}
                    colorClass="bg-green-500"
                    onClick={() => triggerSimulation('sales-boom', 'Talep Patlaması', 'BOOM')}
                    isLoading={loading}
                />
                <SimulationCard
                    title="Ekonomik Durgunluk"
                    description="Satışlar durur, stoklar şişer."
                    icon={ArrowTrendingDownIcon}
                    colorClass="bg-orange-500"
                    onClick={() => triggerSimulation('recession', 'Ekonomik Durgunluk', 'RECESSION')}
                    isLoading={loading}
                />
                <SimulationCard
                    title="Tedarik Krizi"
                    description="Tüm stok kaynakları %50 kesilir."
                    icon={ExclamationTriangleIcon}
                    colorClass="bg-red-600"
                    onClick={() => triggerSimulation('supply-shock', 'Tedarik Krizi', 'SHOCK')}
                    isLoading={loading}
                />
                <SimulationCard
                    title="Sistemi Sıfırla"
                    description="Fabrika ayarlarına dön (Reset)."
                    icon={ArrowPathIcon}
                    colorClass="bg-slate-600"
                    onClick={() => triggerSimulation('reset', 'Sistem Sıfırlama', 'RESET')}
                    isLoading={loading}
                />
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="p-4 border-b border-slate-100 bg-slate-50/50">
                    <h3 className="font-bold text-slate-700">Simülasyon Logları</h3>
                </div>
                <div className="p-4 h-64 overflow-y-auto space-y-2 font-mono">
                    {logs.length === 0 ? (
                        <div className="text-center text-slate-400 py-10">
                            Henüz bir senaryo çalıştırılmadı.
                        </div>
                    ) : (
                        logs.map((log, index) => <LogItem key={index} log={log} />)
                    )}
                </div>
            </div>
        </div>
    );
};

export default Simulations;
