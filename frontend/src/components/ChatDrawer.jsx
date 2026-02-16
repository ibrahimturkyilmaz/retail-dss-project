import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, X, Send, User } from 'lucide-react';
import { supabase } from '../lib/supabase';
import { useAuth } from '../context/AuthContext';

const ChatDrawer = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const { user } = useAuth();

    useEffect(() => {
        if (!isOpen) return;

        // Mevcut mesajları yükle
        fetchMessages();

        // Realtime abonelik
        const channel = supabase
            .channel('public:messages')
            .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, (payload) => {
                // Yeni mesaj geldiğinde listeye ekle
                // Profil bilgisini de almak için normalde join gerekir ama basitlik için şimdilik sadece payload
                // Gerçek uygulamada kullanıcı bilgisini de fetch etmek gerekebilir
                setMessages((prev) => [...prev, payload.new]);
            })
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
    }, [isOpen]);

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const fetchMessages = async () => {
        setLoading(true);
        const { data, error } = await supabase
            .from('messages')
            .select('*')
            .order('created_at', { ascending: true })
            .limit(50);

        if (error) {
            console.error('Mesajlar yüklenemedi:', error);
        } else {
            setMessages(data || []);
        }
        setLoading(false);
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!newMessage.trim() || !user) return;

        const { error } = await supabase
            .from('messages')
            .insert([
                {
                    content: newMessage,
                    user_id: user.id,
                    user_email: user.email // Basitlik için email'i de kaydediyoruz
                }
            ]);

        if (error) {
            console.error('Mesaj gönderilemedi:', error);
        } else {
            setNewMessage('');
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    if (!user) return null; // Giriş yapmamışsa gösterme

    return (
        <>
            {/* Yüzen Buton */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="fixed bottom-6 right-6 p-4 bg-emerald-600 text-white rounded-full shadow-lg hover:bg-emerald-700 transition-all z-50 flex items-center justify-center animate-bounce-slow"
                >
                    <MessageSquare size={24} />
                </button>
            )}

            {/* Chat Paneli (Drawer) */}
            <div className={`fixed inset-y-0 right-0 w-96 bg-gray-900/95 backdrop-blur-md shadow-2xl transform transition-transform duration-300 ease-in-out z-50 border-l border-gray-700 flex flex-col ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>

                {/* Header */}
                <div className="p-4 border-b border-gray-700 flex justify-between items-center bg-gray-800/50">
                    <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                        Canlı Destek & Ekip
                    </h3>
                    <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white transition-colors">
                        <X size={20} />
                    </button>
                </div>

                {/* Mesaj Listesi */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
                    {loading ? (
                        <div className="text-center text-gray-400 mt-10">Yükleniyor...</div>
                    ) : messages.length === 0 ? (
                        <div className="text-center text-gray-500 mt-10 text-sm">
                            Henüz mesaj yok. İlk mesajı sen yaz!
                        </div>
                    ) : (
                        messages.map((msg) => (
                            <div key={msg.id} className={`flex flex-col ${msg.user_id === user.id ? 'items-end' : 'items-start'}`}>
                                <div className={`max-w-[80%] rounded-2xl px-4 py-2 shadow-sm ${msg.user_id === user.id
                                        ? 'bg-emerald-600 text-white rounded-tr-none'
                                        : 'bg-gray-700 text-gray-200 rounded-tl-none'
                                    }`}>
                                    <p className="text-sm">{msg.content}</p>
                                </div>
                                <span className="text-[10px] text-gray-500 mt-1 px-1">
                                    {msg.user_email?.split('@')[0] || 'Anonim'} • {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                            </div>
                        ))
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Alanı */}
                <form onSubmit={sendMessage} className="p-4 border-t border-gray-700 bg-gray-800/50">
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={newMessage}
                            onChange={(e) => setNewMessage(e.target.value)}
                            placeholder="Bir mesaj yaz..."
                            className="flex-1 bg-gray-700/50 border border-gray-600 text-white rounded-lg px-4 py-2 focus:outline-none focus:border-emerald-500 transition-colors placeholder-gray-500 text-sm"
                        />
                        <button
                            type="submit"
                            disabled={!newMessage.trim()}
                            className="p-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send size={18} />
                        </button>
                    </div>
                </form>
            </div>

            {/* Backdrop (Mobilde kapatmak için) */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 lg:hidden"
                    onClick={() => setIsOpen(false)}
                />
            )}
        </>
    );
};

export default ChatDrawer;
