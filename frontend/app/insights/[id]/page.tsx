'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { analysis } from '@/lib/api';
import { ArrowLeft, TrendingUp, AlertTriangle, FileText, BarChart3, PieChart } from 'lucide-react';
import { PieChart as RechartsPie, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function InsightsPage() {
    const router = useRouter();
    const params = useParams();
    const clusterId = params.id as string;

    const [insights, setInsights] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadInsights();
    }, [clusterId]);

    const loadInsights = async () => {
        try {
            const res = await analysis.insights(clusterId);
            setInsights(res.data.insights);
        } catch (error) {
            console.error('Failed to load insights:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading insights...</p>
                </div>
            </div>
        );
    }

    if (!insights) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">No insights available. Run analysis first.</p>
                    <button
                        onClick={() => router.push(`/cluster/${clusterId}`)}
                        className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                    >
                        Go to Cluster
                    </button>
                </div>
            </div>
        );
    }

    // Prepare chart data
    const sentimentData = [
        { name: 'Positive', value: insights.sentiment_distribution.positive, color: '#10b981' },
        { name: 'Negative', value: insights.sentiment_distribution.negative, color: '#ef4444' },
        { name: 'Neutral', value: insights.sentiment_distribution.neutral, color: '#6b7280' }
    ];

    const priorityData = [
        { name: 'Critical', value: insights.priority_distribution.critical, color: '#dc2626' },
        { name: 'High', value: insights.priority_distribution.high, color: '#f59e0b' },
        { name: 'Medium', value: insights.priority_distribution.medium, color: '#3b82f6' },
        { name: 'Low', value: insights.priority_distribution.low, color: '#10b981' }
    ];

    const eventData = Object.entries(insights.event_distribution).map(([name, value]) => ({
        name: name.replace(/_/g, ' '),
        count: value
    }));

    const issueData = Object.entries(insights.top_issues).map(([name, value]) => ({
        name: name.replace(/_/g, ' '),
        count: value
    }));

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
                    <button
                        onClick={() => router.push(`/cluster/${clusterId}`)}
                        className="p-2 hover:bg-gray-100 rounded-lg"
                    >
                        <ArrowLeft size={20} />
                    </button>
                    <div className="flex items-center gap-3">
                        <BarChart3 className="w-6 h-6 text-indigo-600" />
                        <h1 className="text-2xl font-bold">Cluster Insights</h1>
                    </div>
                    <span className="text-gray-500">• {insights.cluster_name}</span>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-7xl mx-auto px-6 py-8">
                {/* Key Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="bg-white rounded-xl shadow p-6"
                    >
                        <div className="flex items-center gap-3 mb-2">
                            <FileText className="w-5 h-5 text-blue-600" />
                            <p className="text-sm text-gray-600">Total Files</p>
                        </div>
                        <p className="text-3xl font-bold text-blue-600">{insights.metrics.total_files}</p>
                        <p className="text-xs text-gray-500 mt-1">{insights.metrics.total_segments} segments</p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="bg-white rounded-xl shadow p-6"
                    >
                        <div className="flex items-center gap-3 mb-2">
                            <AlertTriangle className="w-5 h-5 text-red-600" />
                            <p className="text-sm text-gray-600">Complaints</p>
                        </div>
                        <p className="text-3xl font-bold text-red-600">{insights.metrics.complaint_percentage}%</p>
                        <p className="text-xs text-gray-500 mt-1">of all segments</p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="bg-white rounded-xl shadow p-6"
                    >
                        <div className="flex items-center gap-3 mb-2">
                            <TrendingUp className="w-5 h-5 text-orange-600" />
                            <p className="text-sm text-gray-600">Urgent</p>
                        </div>
                        <p className="text-3xl font-bold text-orange-600">{insights.metrics.urgency_percentage}%</p>
                        <p className="text-xs text-gray-500 mt-1">require immediate action</p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                        className="bg-white rounded-xl shadow p-6"
                    >
                        <div className="flex items-center gap-3 mb-2">
                            <PieChart className="w-5 h-5 text-purple-600" />
                            <p className="text-sm text-gray-600">High Priority</p>
                        </div>
                        <p className="text-3xl font-bold text-purple-600">{insights.metrics.high_priority_percentage}%</p>
                        <p className="text-xs text-gray-500 mt-1">critical or high</p>
                    </motion.div>
                </div>

                {/* Charts Row */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Sentiment Distribution */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 }}
                        className="bg-white rounded-xl shadow p-6"
                    >
                        <h3 className="text-lg font-semibold mb-4">Sentiment Distribution</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <RechartsPie>
                                <Pie
                                    data={sentimentData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {sentimentData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </RechartsPie>
                        </ResponsiveContainer>
                    </motion.div>

                    {/* Priority Distribution */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.5 }}
                        className="bg-white rounded-xl shadow p-6"
                    >
                        <h3 className="text-lg font-semibold mb-4">Priority Distribution</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <RechartsPie>
                                <Pie
                                    data={priorityData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {priorityData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </RechartsPie>
                        </ResponsiveContainer>
                    </motion.div>
                </div>

                {/* Event Distribution Bar Chart */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="bg-white rounded-xl shadow p-6 mb-8"
                >
                    <h3 className="text-lg font-semibold mb-4">Event Distribution</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={eventData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="count" fill="#6366f1" />
                        </BarChart>
                    </ResponsiveContainer>
                </motion.div>

                {/* Top Issues Bar Chart */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.7 }}
                    className="bg-white rounded-xl shadow p-6 mb-8"
                >
                    <h3 className="text-lg font-semibold mb-4">Top Issues</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={issueData} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis type="number" />
                            <YAxis dataKey="name" type="category" width={150} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#f59e0b" />
                        </BarChart>
                    </ResponsiveContainer>
                </motion.div>

                {/* File Rankings */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 }}
                    className="bg-white rounded-xl shadow p-6"
                >
                    <h3 className="text-lg font-semibold mb-4">File Rankings (by Importance Score)</h3>
                    <div className="space-y-3">
                        {insights.top_files.map((file: any, index: number) => (
                            <div
                                key={file.file_id}
                                onClick={() => router.push(`/results/${clusterId}`)}
                                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition"
                            >
                                <div className="flex items-center gap-4 flex-1">
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white ${index === 0 ? 'bg-yellow-500' :
                                            index === 1 ? 'bg-gray-400' :
                                                index === 2 ? 'bg-orange-600' :
                                                    'bg-gray-300'
                                        }`}>
                                        {index + 1}
                                    </div>
                                    <div className="flex-1">
                                        <p className="font-medium">{file.file_name}</p>
                                        <div className="flex gap-4 text-xs text-gray-600 mt-1">
                                            <span>{file.segments} segments</span>
                                            {file.complaint_count > 0 && <span className="text-red-600">{file.complaint_count} complaints</span>}
                                            {file.urgency_count > 0 && <span className="text-orange-600">{file.urgency_count} urgent</span>}
                                            {file.risk_count > 0 && <span className="text-red-700 font-semibold">{file.risk_count} risks</span>}
                                        </div>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="text-2xl font-bold text-indigo-600">{file.score}</p>
                                    <p className="text-xs text-gray-500">importance</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Additional Stats */}
                {insights.risk_signals && Object.keys(insights.risk_signals).length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.9 }}
                        className="bg-red-50 border-2 border-red-200 rounded-xl shadow p-6 mt-6"
                    >
                        <h3 className="text-lg font-semibold text-red-800 mb-4 flex items-center gap-2">
                            <AlertTriangle className="w-5 h-5" />
                            Risk Signals Detected
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                            {Object.entries(insights.risk_signals).map(([risk, count]: any) => (
                                <div key={risk} className="bg-white rounded-lg p-3">
                                    <p className="text-sm text-gray-600">{risk.replace(/_/g, ' ')}</p>
                                    <p className="text-2xl font-bold text-red-600">{count}</p>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                )}
            </div>
        </div>
    );
}
