'use client';

import { useState } from 'react';

export default function EmailForm({ onEmailGenerated, loading, setLoading }) {
  const [formData, setFormData] = useState({
    professor_name: '',
    university_name: '',
    research_domain: '',
    paper_title: '',
    paper_summary: '',
    force_project: ''
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/generate-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate email');
      }

      const data = await response.json();
      onEmailGenerated(data);
    } catch (err) {
      setError(err.message);
      console.error('Error generating email:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFormData({
      professor_name: '',
      university_name: '',
      research_domain: '',
      paper_title: '',
      paper_summary: '',
      force_project: ''
    });
    setError('');
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Professor Details
      </h2>

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Professor Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Professor Name *
          </label>
          <input
            type="text"
            name="professor_name"
            value={formData.professor_name}
            onChange={handleChange}
            required
            placeholder="Dr. Michael Chen"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
        </div>

        {/* University Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            University Name *
          </label>
          <input
            type="text"
            name="university_name"
            value={formData.university_name}
            onChange={handleChange}
            required
            placeholder="MIT"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
        </div>

        {/* Research Domain */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Research Domain *
          </label>
          <input
            type="text"
            name="research_domain"
            value={formData.research_domain}
            onChange={handleChange}
            required
            placeholder="multi-agent systems, natural language processing"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
        </div>

        {/* Paper Title (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Recent Paper Title (Optional)
          </label>
          <input
            type="text"
            name="paper_title"
            value={formData.paper_title}
            onChange={handleChange}
            placeholder="Coordinated Multi-Agent Planning for Complex Tasks"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
        </div>

        {/* Paper Summary (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Paper Summary (Optional)
          </label>
          <textarea
            name="paper_summary"
            value={formData.paper_summary}
            onChange={handleChange}
            rows="3"
            placeholder="Brief summary of the paper's main contributions..."
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
        </div>

        {/* Force Project (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Force Specific Project (Optional)
          </label>
          <input
            type="text"
            name="force_project"
            value={formData.force_project}
            onChange={handleChange}
            placeholder="HireFlow"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Leave blank to let AI choose the best project
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Buttons */}
        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Generating...
              </span>
            ) : (
              '🚀 Generate Email'
            )}
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-semibold rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            Clear
          </button>
        </div>
      </form>
    </div>
  );
}
