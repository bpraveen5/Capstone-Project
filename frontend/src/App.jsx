import React, { useState } from 'react';
import UploadZone from './components/UploadZone';
import Dashboard from './components/Dashboard';

function App() {
    const [currentJobId, setCurrentJobId] = useState(null);

    return (
        <div className="min-h-screen flex flex-col">
            <header className="bg-slate-800 border-b border-slate-700 p-4">
                <div className="container mx-auto flex justify-between items-center">
                    <h1 className="text-2xl font-bold text-blue-400">UDA-Q Agent</h1>
                    <span className="text-sm text-slate-400">Universal AI Data Quality Evaluator</span>
                </div>
            </header>

            <main className="flex-grow container mx-auto p-6">
                {!currentJobId ? (
                    <div className="max-w-2xl mx-auto mt-10">
                        <h2 className="text-3xl font-bold mb-6 text-center">Upload your dataset to begin</h2>
                        <UploadZone onJobStarted={setCurrentJobId} />
                    </div>
                ) : (
                    <Dashboard jobId={currentJobId} onReset={() => setCurrentJobId(null)} />
                )}
            </main>
        </div>
    );
}

export default App;
