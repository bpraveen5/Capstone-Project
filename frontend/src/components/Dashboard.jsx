import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { CheckCircle, AlertTriangle, Activity, Download, RefreshCw } from 'lucide-react';
import { QualityScoreChart, IssuesPieChart } from './Charts';

const API_BASE = 'http://localhost:8000/api';

export default function Dashboard({ jobId, onReset }) {
    const [job, setJob] = useState(null);
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        let interval;

        const fetchJob = async () => {
            try {
                const res = await axios.get(`${API_BASE}/jobs/${jobId}/`);
                setJob(res.data);
                if (res.data.logs) {
                    try {
                        setLogs(JSON.parse(res.data.logs));
                    } catch (e) {
                        setLogs([]);
                    }
                }

                if (res.data.status === 'COMPLETED' || res.data.status === 'FAILED') {
                    clearInterval(interval);
                }
            } catch (err) {
                console.error("Error polling job", err);
            }
        };

        fetchJob();
        interval = setInterval(fetchJob, 2000); // Poll every 2s

        return () => clearInterval(interval);
    }, [jobId]);

    const handleDownload = () => {
        if (job?.report?.cleaned_file_path) {
            const filename = job.report.cleaned_file_path.split('/').pop().split('\\').pop();
            const downloadUrl = `${API_BASE.replace('/api', '')}/media/cleaned/${filename}`;
            window.open(downloadUrl, '_blank');
        }
    };

    if (!job) return <div className="text-center p-10">Loading job details...</div>;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left: Status & Logs */}
            <div className="lg:col-span-1 space-y-6">
                <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                        <Activity className="text-blue-400" />
                        Agent Status
                    </h3>
                    <div className={`text-center p-4 rounded-lg font-bold text-xl mb-4
            ${job.status === 'RUNNING' ? 'bg-blue-900/30 text-blue-300 animate-pulse' : ''}
            ${job.status === 'COMPLETED' ? 'bg-green-900/30 text-green-300' : ''}
            ${job.status === 'FAILED' ? 'bg-red-900/30 text-red-300' : ''}
          `}>
                        {job.status}
                    </div>

                    <div className="h-64 overflow-y-auto bg-slate-900 p-4 rounded font-mono text-xs text-slate-300 space-y-1">
                        {logs.map((log, i) => (
                            <div key={i} className="border-l-2 border-slate-700 pl-2">
                                <span className="text-slate-500">[{i + 1}]</span> {log}
                            </div>
                        ))}
                    </div>
                </div>

                {job.status === 'COMPLETED' && (
                    <button onClick={onReset} className="w-full py-2 bg-slate-700 hover:bg-slate-600 rounded text-slate-200 flex items-center justify-center gap-2">
                        <RefreshCw size={16} /> Start New Analysis
                    </button>
                )}
            </div>

            {/* Right: Report & Results */}
            <div className="lg:col-span-2">
                {job.report ? (
                    <div className="space-y-6">
                        {/* Scores */}
                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center">
                                <div className="text-slate-400 text-sm uppercase tracking-wider">Initial Quality</div>
                                <div className="text-4xl font-bold text-yellow-500 mt-2">{job.report.initial_quality_score.toFixed(1)}</div>
                            </div>
                            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center">
                                <div className="text-slate-400 text-sm uppercase tracking-wider">Final Quality</div>
                                <div className="text-4xl font-bold text-green-500 mt-2">{job.report.final_quality_score.toFixed(1)}</div>
                            </div>
                        </div>

                        {/* Charts Row */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                                <h4 className="text-sm font-bold text-slate-400 mb-4 uppercase">Quality Improvement</h4>
                                <QualityScoreChart
                                    initial={job.report.initial_quality_score}
                                    final={job.report.final_quality_score}
                                />
                            </div>
                            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                                <h4 className="text-sm font-bold text-slate-400 mb-4 uppercase">Issues Distribution</h4>
                                <IssuesPieChart issues={job.report.issues_found} />
                            </div>
                        </div>

                        {/* Issues Found */}
                        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                <AlertTriangle className="text-yellow-500" />
                                Issues Detected & Fixed
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {Object.entries(job.report.issues_found).map(([issue, count]) => (
                                    <div key={issue} className="bg-slate-900 p-4 rounded flex justify-between items-center">
                                        <span className="capitalize text-slate-300">{issue.replace('_', ' ')}</span>
                                        <span className="bg-red-900/50 text-red-200 px-2 py-1 rounded text-sm font-bold">{count} found</span>
                                    </div>
                                ))}
                            </div>
                            <div className="mt-6">
                                <h4 className="text-sm font-bold text-slate-400 mb-2 uppercase">Actions Taken</h4>
                                <ul className="space-y-2">
                                    {job.report.actions_taken.map((action, i) => (
                                        <li key={i} className="flex items-center gap-2 text-green-300">
                                            <CheckCircle size={16} /> {action}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>

                        {/* Download */}
                        {job.report.cleaned_file_path && (
                            <div className="bg-green-900/20 border border-green-900/50 p-6 rounded-xl flex justify-between items-center">
                                <div>
                                    <h3 className="text-lg font-bold text-green-400">Dataset Cleaned Successfully!</h3>
                                    <p className="text-green-200/70 text-sm">Your data is ready for download.</p>
                                </div>
                                <button onClick={handleDownload} className="bg-green-600 hover:bg-green-500 text-white px-6 py-3 rounded-lg font-bold flex items-center gap-2 shadow-lg shadow-green-900/20">
                                    <Download size={20} /> Download Cleaned Data
                                </button>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="h-full flex items-center justify-center bg-slate-800/50 border border-slate-700/50 rounded-xl border-dashed">
                        <div className="text-center text-slate-500">
                            <Activity className="w-12 h-12 mx-auto mb-4 opacity-50 animate-spin" />
                            <p>Agent is analyzing your data...</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
