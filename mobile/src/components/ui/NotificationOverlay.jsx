import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MapPin, X } from 'lucide-react';

export default function NotificationOverlay({ notification, onClose }) {
    return (
        <AnimatePresence>
            {notification && (
                <motion.div
                    initial={{ y: -100, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    exit={{ y: -100, opacity: 0 }}
                    className="fixed top-4 left-4 right-4 z-50 pointer-events-none"
                >
                    <div className="bg-white/90 backdrop-blur-md shadow-2xl rounded-2xl p-4 border-l-4 border-indigo-600 pointer-events-auto flex items-start gap-4">
                        <div className="bg-indigo-100 p-2 rounded-full text-indigo-600 shrink-0">
                            <MapPin size={24} />
                        </div>
                        <div className="flex-1">
                            <h3 className="font-bold text-gray-900">{notification.title}</h3>
                            <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
                            {notification.action && (
                                <button
                                    onClick={notification.action.onClick}
                                    className="mt-3 text-xs font-bold text-indigo-600 uppercase tracking-wider hover:text-indigo-800 transition-colors"
                                >
                                    {notification.action.label}
                                </button>
                            )}
                        </div>
                        <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
                            <X size={18} />
                        </button>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
