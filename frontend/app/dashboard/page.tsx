'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { clusters } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { Plus, Folder, LogOut, Trash2 } from 'lucide-react';

export default function Dashboard() {
    const router = useRouter();
    const { user, logout, isLoading } = useAuth();
    const [clusterList, setClusterList] = useState<any[]>([]);
    const [showCreate, setShowCreate] = useState(false);
    const [newClusterName, setNewClusterName] = useState('');

    useEffect(() => {
        if (isLoading) {
            return; // Wait for auth to initialize
        }

        if (!user) {
            router.push('/login');
            return;
        }

        // Only load clusters if we have a user
        loadClusters();
    }, [user, isLoading, router]);

    const loadClusters = async () => {
        try {
            const response = await clusters.list();
            setClusterList(response.data.clusters);
        } catch (error: any) {
            console.error('Failed to load clusters:', error);
            if (error.response?.status === 401) {
                logout();
            }
        }
    };

    const handleCreate = async () => {
        if (!newClusterName.trim()) return;

        try {
            await clusters.create(newClusterName);
            setNewClusterName('');
            setShowCreate(false);
            loadClusters();
        } catch (error: any) {
            console.error('Failed to create cluster:', error);
            if (error.response?.status === 401) {
                logout();
            } else {
                alert('Failed to create cluster');
            }
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Delete this cluster?')) return;

        try {
            await clusters.delete(id);
            loadClusters();
        } catch (error: any) {
            console.error('Failed to delete cluster:', error);
            if (error.response?.status === 401) {
                logout();
            }
        }
    };

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading...</p>
                </div>
            </div>
        );
    }

    if (!user) {
        return null;
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                    <h1 className="text-2xl font-bold text-gray-900">SARCIS Dashboard</h1>
                    <div className="flex items-center gap-4">
                        <span className="text-gray-600">Welcome, {user.name}</span>
                        <button
                            onClick={logout}
                            className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                        >
                            <LogOut size={18} />
                            Logout
                        </button>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-7xl mx-auto px-6 py-8">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-xl font-semibold">My Clusters</h2>
                    <button
                        onClick={() => setShowCreate(true)}
                        className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
                    >
                        <Plus size={20} />
                        New Cluster
                    </button>
                </div>

                {/* Create Modal */}
                {showCreate && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
                        onClick={() => setShowCreate(false)}
                    >
                        <motion.div
                            initial={{ scale: 0.9 }}
                            animate={{ scale: 1 }}
                            className="bg-white p-6 rounded-xl shadow-xl w-full max-w-md"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <h3 className="text-xl font-bold mb-4">Create New Cluster</h3>
                            <input
                                type="text"
                                value={newClusterName}
                                onChange={(e) => setNewClusterName(e.target.value)}
                                placeholder="Cluster name"
                                className="w-full px-4 py-2 border rounded-lg mb-4 focus:ring-2 focus:ring-indigo-500"
                                autoFocus
                                onKeyPress={(e) => e.key === 'Enter' && handleCreate()}
                            />
                            <div className="flex gap-3">
                                <button
                                    onClick={handleCreate}
                                    className="flex-1 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                                >
                                    Create
                                </button>
                                <button
                                    onClick={() => setShowCreate(false)}
                                    className="flex-1 py-2 bg-gray-200 rounded-lg hover:bg-gray-300"
                                >
                                    Cancel
                                </button>
                            </div>
                        </motion.div>
                    </motion.div>
                )}

                {/* Clusters Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {clusterList.map((cluster) => (
                        <motion.div
                            key={cluster.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            whileHover={{ scale: 1.02 }}
                            className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition cursor-pointer relative group"
                            onClick={() => router.push(`/cluster/${cluster.id}`)}
                        >
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleDelete(cluster.id);
                                }}
                                className="absolute top-4 right-4 p-2 text-red-500 hover:bg-red-50 rounded-lg opacity-0 group-hover:opacity-100 transition"
                            >
                                <Trash2 size={18} />
                            </button>

                            <Folder className="w-12 h-12 text-indigo-600 mb-4" />
                            <h3 className="text-lg font-semibold mb-2">{cluster.name}</h3>
                            <p className="text-gray-600 text-sm">
                                {cluster.file_count} files • {cluster.status}
                            </p>
                            <p className="text-gray-400 text-xs mt-2">
                                {new Date(cluster.created_at).toLocaleDateString()}
                            </p>
                        </motion.div>
                    ))}
                </div>

                {clusterList.length === 0 && (
                    <div className="text-center py-12 text-gray-500">
                        <Folder className="w-16 h-16 mx-auto mb-4 opacity-50" />
                        <p>No clusters yet. Create one to get started!</p>
                    </div>
                )}
            </div>
        </div>
    );
}
