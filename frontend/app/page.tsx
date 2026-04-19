'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { AudioWaveform } from 'lucide-react';

export default function Home() {
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            router.push('/dashboard');
        }
    }, [router]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center"
            >
                <AudioWaveform className="w-20 h-20 mx-auto mb-6 text-indigo-600" />
                <h1 className="text-5xl font-bold mb-4 text-gray-900">SARCIS</h1>
                <p className="text-xl text-gray-600 mb-8">Smart Audio Risk & Context Intelligence</p>

                <div className="space-x-4">
                    <button
                        onClick={() => router.push('/login')}
                        className="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
                    >
                        Login
                    </button>
                    <button
                        onClick={() => router.push('/signup')}
                        className="px-8 py-3 bg-white text-indigo-600 border-2 border-indigo-600 rounded-lg hover:bg-indigo-50 transition"
                    >
                        Sign Up
                    </button>
                </div>
            </motion.div>
        </div>
    );
}
