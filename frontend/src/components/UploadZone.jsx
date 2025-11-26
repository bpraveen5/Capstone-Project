import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileUp, AlertCircle } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

export default function UploadZone({ onJobStarted }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
            setError(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('name', file.name);

        try {
            // 1. Upload Dataset
            const uploadRes = await axios.post(`${API_BASE}/datasets/`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const datasetId = uploadRes.data.id;

            // 2. Start Job
            const jobRes = await axios.post(`${API_BASE}/jobs/start_job/`, {
                dataset_id: datasetId
            });

            onJobStarted(jobRes.data.id);

        } catch (err) {
            console.error(err);
            const serverError = err.response?.data?.error || err.message;
            setError(`Upload Failed: ${serverError}`);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-lg">
            <div className="border-2 border-dashed border-slate-600 rounded-lg p-10 text-center hover:border-blue-500 transition-colors">
                <input
                    type="file"
                    accept=".csv,.xlsx"
                    onChange={handleFileChange}
                    className="hidden"
                    id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
                    <FileUp className="w-16 h-16 text-blue-400 mb-4" />
                    <span className="text-xl font-medium text-slate-200">
                        {file ? file.name : "Click to upload CSV or Excel"}
                    </span>
                    <span className="text-sm text-slate-500 mt-2">
                        Supported formats: .csv, .xlsx
                    </span>
                </label>
            </div>

            {error && (
                <div className="mt-4 p-3 bg-red-900/50 text-red-200 rounded flex items-center gap-2">
                    <AlertCircle size={18} />
                    {error}
                </div>
            )}

            <button
                onClick={handleUpload}
                disabled={!file || uploading}
                className={`mt-6 w-full py-3 rounded-lg font-bold text-white transition-all
          ${!file || uploading
                        ? 'bg-slate-600 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-900/20'
                    }`}
            >
                {uploading ? 'Uploading & Starting Agent...' : 'Start Analysis'}
            </button>
        </div>
    );
}
