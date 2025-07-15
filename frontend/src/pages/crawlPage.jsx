import React, { useState, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function CrawlPage() {
    const urlRef = useRef();
    const statusRef = useRef();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    async function crawl() {
        statusRef.current.innerText = "⏳ Crawling started...";
        setLoading(true);
        const url = urlRef.current.value;
        try {
            const response = await axios.post('http://localhost:8000/crawl', { url });
            console.log(response.data);
            statusRef.current.innerText = "✅ " + response.data.status;
            setTimeout(() => {
                navigate('/chat');
            }, 3000);
        } catch (err) {
            console.error(err);
            statusRef.current.innerText = "❌ Crawl failed. Check console.";
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="flex items-center justify-center h-screen bg-black font-sans">
            <div className="bg-white/5 backdrop-blur-md border border-white/20 shadow-lg rounded-3xl p-10 w-[90%] max-w-md text-center transition-all duration-300">
                <h1 className="text-4xl font-extrabold text-white mb-4">🌐 Crawl a Website</h1>
                <p className="text-gray-300 mb-6 text-sm">Enter the URL of the site you'd like to crawl:</p>

                <input
                    type="text"
                    placeholder="https://example.com"
                    ref={urlRef}
                    className="w-full px-4 py-2 mb-4 bg-white/10 text-white border border-white/20 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />

                <button
                    onClick={crawl}
                    disabled={loading}
                    className={`w-full py-2 rounded-lg text-white font-semibold transition duration-300 ${
                        loading
                            ? 'bg-purple-400 cursor-not-allowed'
                            : 'bg-purple-600 hover:bg-purple-700'
                    }`}
                >
                    {loading ? 'Crawling...' : 'Submit'}
                </button>

                {loading && (
                    <div className="flex justify-center mt-4">
                        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-400"></div>
                    </div>
                )}

                <div
                    className="mt-4 text-sm font-medium text-white min-h-[1.5rem]"
                    ref={statusRef}
                    id="status"
                ></div>
            </div>
        </div>
    );
}

export default CrawlPage;
