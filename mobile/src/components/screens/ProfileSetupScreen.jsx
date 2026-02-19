import { useState } from 'react';
import { motion } from 'framer-motion';
import { User, Phone, Mail, CheckCircle, ArrowRight, Sparkles } from 'lucide-react';
import { useUser } from '../../context/UserContext';

export default function ProfileSetupScreen({ onComplete }) {
    const { user, updateProfile } = useUser();
    const [name, setName] = useState(user?.name || '');
    const [surname, setSurname] = useState(user?.surname || '');
    const [phone, setPhone] = useState(user?.phone || '');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/customers/${user.id}/profile`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: name,
                    surname: surname,
                    phone: phone || null,
                }),
            });

            if (!response.ok) throw new Error('Profil güncellenemedi');

            const updatedData = await response.json();
            updateProfile(updatedData);
            onComplete();
        } catch (error) {
            console.error('Profile setup error:', error);
            alert('Profil güncellenirken bir hata oluştu.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-white relative overflow-hidden flex flex-col">
            {/* Background */}
            <div className="absolute top-0 left-0 right-0 h-72 bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-700 rounded-b-[3rem]">
                <div className="absolute top-8 right-8 w-32 h-32 bg-white/10 rounded-full blur-2xl" />
                <div className="absolute bottom-4 left-4 w-48 h-48 bg-purple-400/10 rounded-full blur-3xl" />
            </div>

            <div className="relative z-10 px-8 pt-16 flex-1">
                {/* Header */}
                <div className="text-center mb-8">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", delay: 0.2 }}
                        className="w-20 h-20 bg-white/20 backdrop-blur-md rounded-3xl flex items-center justify-center mx-auto mb-5 border border-white/30"
                    >
                        <Sparkles size={36} className="text-white" />
                    </motion.div>
                    <h1 className="text-3xl font-bold text-white mb-2">Profilini Tamamla</h1>
                    <p className="text-indigo-100 text-sm">Seni daha iyi tanıyalım ✨</p>
                </div>

                {/* Email Badge */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="bg-white rounded-2xl p-4 shadow-lg shadow-indigo-100 flex items-center gap-3 mb-6 border border-indigo-50"
                >
                    <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
                        <CheckCircle size={22} />
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-xs font-bold text-emerald-600 uppercase tracking-wide">Doğrulanmış E-posta</p>
                        <p className="text-gray-800 font-medium truncate">{user?.email}</p>
                    </div>
                    <Mail size={18} className="text-gray-300" />
                </motion.div>

                {/* Form */}
                <motion.form
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    onSubmit={handleSubmit}
                    className="space-y-4"
                >
                    <div className="grid grid-cols-2 gap-3">
                        <div className="space-y-1.5">
                            <label className="text-sm font-semibold text-gray-700 ml-1">İsim</label>
                            <div className="relative">
                                <User size={18} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full bg-gray-50 border border-gray-100 rounded-2xl py-3.5 pl-11 pr-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium text-sm"
                                    required
                                />
                            </div>
                        </div>
                        <div className="space-y-1.5">
                            <label className="text-sm font-semibold text-gray-700 ml-1">Soyisim</label>
                            <input
                                type="text"
                                value={surname}
                                onChange={(e) => setSurname(e.target.value)}
                                className="w-full bg-gray-50 border border-gray-100 rounded-2xl py-3.5 px-4 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium text-sm"
                            />
                        </div>
                    </div>

                    <div className="space-y-1.5">
                        <label className="text-sm font-semibold text-gray-700 ml-1">Telefon <span className="text-gray-400 font-normal">(opsiyonel)</span></label>
                        <div className="relative">
                            <Phone size={18} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
                            <input
                                type="tel"
                                value={phone}
                                onChange={(e) => setPhone(e.target.value)}
                                className="w-full bg-gray-50 border border-gray-100 rounded-2xl py-3.5 pl-11 pr-4 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium"
                                placeholder="05XX XXX XX XX"
                            />
                        </div>
                    </div>

                    <motion.button
                        whileTap={{ scale: 0.98 }}
                        type="submit"
                        disabled={isLoading || !name}
                        className="w-full bg-indigo-600 text-white rounded-2xl py-4 font-bold text-lg shadow-lg shadow-indigo-200 flex items-center justify-center gap-2 hover:bg-indigo-700 transition-colors disabled:opacity-70 disabled:cursor-not-allowed mt-6"
                    >
                        {isLoading ? (
                            <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                Profili Tamamla
                                <ArrowRight size={20} />
                            </>
                        )}
                    </motion.button>

                    <button
                        type="button"
                        onClick={onComplete}
                        className="w-full text-gray-400 text-sm font-medium py-2 hover:text-gray-600 transition-colors"
                    >
                        Şimdilik Atla
                    </button>
                </motion.form>
            </div>
        </div>
    );
}
