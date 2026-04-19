'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { clusters, files, analysis } from '@/lib/api';
import { Upload, Play, ArrowLeft, FileAudio, BarChart3, Eye } from 'lucide-react';

export default function ClusterPage() {
    const router = useRouter();
    const params = useParams();
    const clusterId = params.id as string;

    const [cluster, setCluster] = useState<any>(null);
    const [fileList, setFileList] = useState<any[]>([]);
    const [uploading, setUploading] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);

    useEffect(() => {
        loadData();
    }, [clusterId]);

    const loadData = async () => {
        try {
            const [clusterRes, filesRes] = await Promise.all([
                clusters.list(),
                clusters.files(clusterId),
            ]);

            const currentCluster = clusterRes.data.clusters.find((c: any) => c.id === clusterId);
            setCluster(currentCluster);
            setFileList(filesRes.data.files);
        } catch (error) {
            console.error('Failed to load data:', error);
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files || e.target.files.length === 0) return;

        setUploading(true);
        try {
            await files.upload(clusterId, e.target.files);
            await loadData();
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Upload failed');
        } finally {
            setUploading(false);
        }
    };

    const handleAnalyze = async () => {
        if (!confirm('Start analysis? This may take a few minutes.')) return;

        setAnalyzing(true);
        try {
            await analysis.start(clusterId);
            alert('Analysis completed!');
            router.push(`/results/${clusterId}`);
        } catch (error: any) {
            console.error('Analysis failed:', error);
            alert(error.response?.data?.detail || 'Analysis failed');
        } finally {
            setAnalyzing(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
                    <button
                        onClick={() => router.push('/dashboard')}
                        className="p-2 hover:bg-gray-100 rounded-lg"
                    >
                        <ArrowLeft size={20} />
                    </button>
                    <div className="flex-1">
                        <h1 className="text-2xl font-bold">{cluster?.name}</h1>
                        <p className="text-gray-600">{fileList.length} files</p>
                    </div>
                    <div className="flex gap-3">
                        {cluster?.status === 'completed' && (
                            <>
                                <button
                                    onClick={() => router.push(`/insights/${clusterId}`)}
                                    className="flex items-center gap-2 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
                                >
                                    <BarChart3 size={20} />
                                    View Insights
                                </button>
                                <button
                                    onClick={() => router.push(`/results/${clusterId}`)}
                                    className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                                >
                                    <Eye size={20} />
                                    View Results
                                </button>
                            </>
                        )}
                        {fileList.length > 0 && (
                            <button
                                onClick={handleAnalyze}
                                disabled={analyzing}
                                className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
                            >
                                <Play size={20} />
                                {analyzing ? 'Analyzing...' : 'Run Analysis'}
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-7xl mx-auto px-6 py-8">
                {/* Upload Area */}
                <div className="bg-white p-8 rounded-xl shadow mb-6">
                    <label className="block cursor-pointer">
                        <input
                            type="file"
                            multiple
                            accept=".wav,.mp3,.m4a"
                            onChange={handleFileUpload}
                            className="hidden"
                            disabled={uploading}
                        />
                        <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-indigo-500 transition">
                            <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                            <p className="text-lg font-semibold mb-2">
                                {uploading ? 'Uploading...' : 'Upload Audio Files'}
                            </p>
                            <p className="text-gray-600">
                                Click to browse or drag & drop • .wav, .mp3, .m4a
                            </p>
                        </div>
                    </label>
                </div>

                {/* Files List */}
                <div className="bg-white rounded-xl shadow p-6">
                    <h2 className="text-xl font-semibold mb-4">Files</h2>
                    {fileList.length === 0 ? (
                        <p className="text-center text-gray-500 py-8">No files uploaded yet</p>
                    ) : (
                        <div className="space-y-3">
                            {fileList.map((file) => (
                                <motion.div
                                    key={file.id}
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="flex items-center gap-4 p-4 border rounded-lg hover:border-indigo-500 transition"
                                >
                                    <FileAudio className="w-8 h-8 text-indigo-600" />
                                    <div className="flex-1">
                                        <p className="font-medium">{file.file_name}</p>
                                        <p className="text-sm text-gray-600">
                                            {file.status} • {new Date(file.uploaded_at).toLocaleString()}
                                        </p>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
