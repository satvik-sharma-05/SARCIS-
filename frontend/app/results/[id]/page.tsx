'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { analysis } from '@/lib/api';
import { ArrowLeft, Clock, AlertCircle, TrendingUp, BarChart3, Play, Pause } from 'lucide-react';

export default function ResultsPage() {
    const router = useRouter();
    const params = useParams();
    const clusterId = params.id as string;

    const [results, setResults] = useState<any[]>([]);
    const [insights, setInsights] = useState<any>(null);
    const [selectedFile, setSelectedFile] = useState<any>(null);
    const [selectedSegment, setSelectedSegment] = useState<any>(null);
    const [playing, setPlaying] = useState(false);

    const audioRef = useRef<HTMLAudioElement>(null);

    useEffect(() => {
        loadData();
    }, [clusterId]);

    const loadData = async () => {
        try {
            const [resultsRes, insightsRes] = await Promise.all([
                analysis.results(clusterId),
                analysis.insights(clusterId),
            ]);

            setResults(resultsRes.data.results);
            setInsights(insightsRes.data.insights);

            if (resultsRes.data.results.length > 0) {
                setSelectedFile(resultsRes.data.results[0]);
            }
        } catch (error) {
            console.error('Failed to load results:', error);
        }
    };

    // Get audio URL for the selected file
    const getAudioUrl = () => {
        if (!selectedFile) return '';

        const fileName = selectedFile.file_name;
        const token = localStorage.getItem('token');

        // We'll use the token in the Authorization header via fetch
        // For now, return the base URL
        return `http://localhost:8000/audio/${clusterId}/${encodeURIComponent(fileName)}`;
    };

    // Update audio source when file changes
    useEffect(() => {
        if (selectedFile && audioRef.current) {
            const token = localStorage.getItem('token');
            const fileName = selectedFile.file_name;
            const url = `http://localhost:8000/audio/${clusterId}/${encodeURIComponent(fileName)}`;

            // Fetch with auth and create blob URL
            fetch(url, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
                .then(res => res.blob())
                .then(blob => {
                    const blobUrl = URL.createObjectURL(blob);
                    if (audioRef.current) {
                        audioRef.current.src = blobUrl;
                    }
                })
                .catch(err => console.error('Failed to load audio:', err));
        }
    }, [selectedFile, clusterId]);

    const handleSegmentClick = (segment: any) => {
        setSelectedSegment(segment);
        if (audioRef.current) {
            audioRef.current.currentTime = segment.start;
            audioRef.current.play();
            setPlaying(true);
        }
    };

    const togglePlayPause = () => {
        if (audioRef.current) {
            if (playing) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setPlaying(!playing);
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'critical':
                return 'bg-red-600 text-white';
            case 'high':
                return 'bg-red-100 text-red-800';
            case 'medium':
                return 'bg-yellow-100 text-yellow-800';
            default:
                return 'bg-green-100 text-green-800';
        }
    };

    const getSentimentColor = (sentiment: string) => {
        switch (sentiment) {
            case 'positive':
                return 'text-green-600';
            case 'negative':
                return 'text-red-600';
            default:
                return 'text-gray-600';
        }
    };

    const getEventColor = (event: string) => {
        const colors: any = {
            complaint: 'bg-red-100 text-red-800',
            urgency: 'bg-orange-100 text-orange-800',
            request: 'bg-blue-100 text-blue-800',
            financial_issue: 'bg-purple-100 text-purple-800',
            technical_issue: 'bg-indigo-100 text-indigo-800',
            positive_feedback: 'bg-green-100 text-green-800',
            escalation: 'bg-red-200 text-red-900',
            negative_language: 'bg-gray-700 text-white',
        };
        return colors[event] || 'bg-gray-100 text-gray-800';
    };

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
                    <h1 className="text-2xl font-bold">Analysis Results</h1>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-7xl mx-auto px-6 py-8">
                {/* Cluster Insights Dashboard */}
                {insights && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="bg-white rounded-xl shadow p-6 mb-6"
                    >
                        <div className="flex items-center gap-3 mb-6">
                            <BarChart3 className="w-6 h-6 text-indigo-600" />
                            <h2 className="text-xl font-bold">Cluster Intelligence</h2>
                        </div>

                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                            <div className="bg-blue-50 p-4 rounded-lg">
                                <p className="text-sm text-gray-600 mb-1">Total Files</p>
                                <p className="text-3xl font-bold text-blue-600">{insights.metrics?.total_files || 0}</p>
                            </div>
                            <div className="bg-purple-50 p-4 rounded-lg">
                                <p className="text-sm text-gray-600 mb-1">Total Segments</p>
                                <p className="text-3xl font-bold text-purple-600">{insights.metrics?.total_segments || 0}</p>
                            </div>
                            <div className="bg-red-50 p-4 rounded-lg">
                                <p className="text-sm text-gray-600 mb-1">Complaints</p>
                                <p className="text-3xl font-bold text-red-600">{insights.metrics?.complaint_percentage || 0}%</p>
                            </div>
                            <div className="bg-orange-50 p-4 rounded-lg">
                                <p className="text-sm text-gray-600 mb-1">Urgent</p>
                                <p className="text-3xl font-bold text-orange-600">{insights.metrics?.urgency_percentage || 0}%</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <h3 className="font-semibold mb-3">Top Events</h3>
                                <div className="space-y-2">
                                    {Object.entries(insights.event_distribution || insights.top_events || {}).map(([event, count]: any) => (
                                        <div key={event} className="flex justify-between items-center">
                                            <span className={`px-3 py-1 rounded-full text-sm ${getEventColor(event)}`}>
                                                {event}
                                            </span>
                                            <span className="font-semibold">{count}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <h3 className="font-semibold mb-3">Priority Distribution</h3>
                                <div className="space-y-2">
                                    {Object.entries(insights.priority_distribution || {}).map(([priority, count]: any) => (
                                        <div key={priority} className="flex justify-between items-center">
                                            <span className={`px-3 py-1 rounded-full text-sm ${getPriorityColor(priority)}`}>
                                                {priority}
                                            </span>
                                            <span className="font-semibold">{count}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    {/* File List */}
                    <div className="lg:col-span-1">
                        <div className="bg-white rounded-xl shadow p-4">
                            <h3 className="font-semibold mb-4">Files</h3>
                            <div className="space-y-2">
                                {results.map((result) => (
                                    <button
                                        key={result.id}
                                        onClick={() => setSelectedFile(result)}
                                        className={`w-full text-left p-3 rounded-lg transition ${selectedFile?.id === result.id
                                            ? 'bg-indigo-100 border-2 border-indigo-500'
                                            : 'bg-gray-50 hover:bg-gray-100'
                                            }`}
                                    >
                                        <p className="font-medium text-sm truncate">{result.file_name}</p>
                                        <p className="text-xs text-gray-600">{result.segments.length} segments</p>
                                        {result.summary && (
                                            <div className="mt-2 space-y-1">
                                                <p className="text-xs text-red-600">
                                                    {result.summary.negative_percentage}% negative
                                                </p>
                                                <p className="text-xs text-orange-600">
                                                    {result.summary.high_priority_count} high priority
                                                </p>
                                            </div>
                                        )}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Segments */}
                    <div className="lg:col-span-3">
                        {selectedFile ? (
                            <div className="bg-white rounded-xl shadow p-6">
                                <div className="flex items-center justify-between mb-6">
                                    <h2 className="text-xl font-bold">{selectedFile.file_name}</h2>
                                    {selectedFile.summary && (
                                        <div className="flex gap-4 text-sm">
                                            <span className="text-gray-600">
                                                Overall: <span className={getSentimentColor(selectedFile.summary.overall_sentiment)}>
                                                    {selectedFile.summary.overall_sentiment}
                                                </span>
                                            </span>
                                            <span className="text-gray-600">
                                                Top Issue: <span className="font-semibold">{selectedFile.summary.top_issue}</span>
                                            </span>
                                        </div>
                                    )}
                                </div>

                                {/* Audio Player */}
                                <div className="bg-gray-100 p-4 rounded-lg mb-6">
                                    <div className="flex items-center gap-4 mb-2">
                                        <button
                                            onClick={togglePlayPause}
                                            className="p-3 bg-indigo-600 text-white rounded-full hover:bg-indigo-700"
                                        >
                                            {playing ? <Pause size={20} /> : <Play size={20} />}
                                        </button>
                                        <div className="flex-1">
                                            <audio
                                                ref={audioRef}
                                                onPlay={() => setPlaying(true)}
                                                onPause={() => setPlaying(false)}
                                                onEnded={() => setPlaying(false)}
                                                className="w-full"
                                                controls
                                            />
                                        </div>
                                    </div>
                                </div>

                                <div className="space-y-4">
                                    {selectedFile.segments.map((segment: any, index: number) => (
                                        <motion.div
                                            key={index}
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: index * 0.02 }}
                                            onClick={() => handleSegmentClick(segment)}
                                            className={`border rounded-lg p-4 hover:border-indigo-500 transition cursor-pointer ${selectedSegment === segment ? 'border-indigo-500 bg-indigo-50' : ''
                                                }`}
                                        >
                                            <div className="flex items-start justify-between mb-3">
                                                <div className="flex items-center gap-3">
                                                    <Clock size={16} className="text-gray-400" />
                                                    <span className="text-sm text-gray-600">
                                                        {segment.start.toFixed(1)}s - {segment.end.toFixed(1)}s
                                                    </span>
                                                </div>
                                                <span
                                                    className={`px-3 py-1 rounded-full text-xs font-semibold ${getPriorityColor(
                                                        segment.priority
                                                    )}`}
                                                >
                                                    {segment.priority}
                                                </span>
                                            </div>

                                            <p className="text-gray-900 mb-3">{segment.text}</p>

                                            <div className="flex flex-wrap gap-2 mb-2">
                                                {segment.events.map((event: string, i: number) => (
                                                    <span
                                                        key={i}
                                                        className={`px-2 py-1 rounded text-xs font-medium ${getEventColor(event)}`}
                                                    >
                                                        {event}
                                                    </span>
                                                ))}
                                            </div>

                                            <div className="flex items-center gap-4 text-sm">
                                                <span className={`font-medium ${getSentimentColor(segment.sentiment)}`}>
                                                    {segment.sentiment}
                                                </span>
                                                <span className="text-gray-600">Intent: {segment.intent}</span>
                                                {segment.entities && segment.entities.length > 0 && (
                                                    <span className="text-gray-600">
                                                        Entities: {segment.entities.join(', ')}
                                                    </span>
                                                )}
                                                {segment.risk_level && segment.risk_level !== 'low' && (
                                                    <span className={`font-semibold ${segment.risk_level === 'extreme' ? 'text-red-700' :
                                                        segment.risk_level === 'high' ? 'text-red-600' :
                                                            'text-orange-600'
                                                        }`}>
                                                        ⚠️ Risk: {segment.risk_level}
                                                    </span>
                                                )}
                                            </div>

                                            {segment.summary && (
                                                <div className="mt-2 text-sm text-gray-700 bg-gray-50 p-2 rounded">
                                                    {segment.summary}
                                                </div>
                                            )}

                                            <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
                                                <span>Confidence: {(segment.confidence * 100).toFixed(0)}%</span>
                                                {segment.sentiment_intensity && (
                                                    <span>Intensity: {(segment.sentiment_intensity * 100).toFixed(0)}%</span>
                                                )}
                                                {segment.analysis_source && (
                                                    <span className={segment.analysis_source === 'llm' ? 'text-green-600' : 'text-blue-600'}>
                                                        {segment.analysis_source === 'llm' ? '✨ LLM' : '📊 NLP'}
                                                    </span>
                                                )}
                                            </div>
                                        </motion.div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                            <div className="bg-white rounded-xl shadow p-12 text-center text-gray-500">
                                <AlertCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                                <p>Select a file to view results</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
