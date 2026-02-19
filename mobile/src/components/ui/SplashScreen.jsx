import { motion } from 'framer-motion';
import { ShoppingBag } from 'lucide-react';
import { useEffect } from 'react';

export default function SplashScreen({ onComplete }) {
    useEffect(() => {
        // Automatically hide splash screen after 2.5 seconds
        const timer = setTimeout(() => {
            onComplete();
        }, 2500);
        return () => clearTimeout(timer);
    }, [onComplete]);

    return (
        <div className="fixed inset-0 bg-indigo-600 flex flex-col items-center justify-center z-[100]">
            <motion.div
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="bg-white p-6 rounded-3xl mb-6 shadow-2xl"
            >
                <ShoppingBag size={48} className="text-indigo-600" />
            </motion.div>

            <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.8 }}
                className="text-center"
            >
                <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">StyleStore</h1>
                <p className="text-indigo-200 text-sm font-medium tracking-wide">MODA & YAŞAM</p>
            </motion.div>

            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.5, duration: 0.5 }}
                className="absolute bottom-10 flex gap-1"
            >
                {[0, 1, 2].map((i) => (
                    <motion.div
                        key={i}
                        animate={{ y: [0, -6, 0] }}
                        transition={{
                            duration: 0.6,
                            repeat: Infinity,
                            delay: i * 0.1
                        }}
                        className="w-2 h-2 bg-white rounded-full opacity-80"
                    />
                ))}
            </motion.div>
        </div>
    );
}
