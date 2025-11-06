'use client';

import { useState } from 'react';
import EmailForm from './components/EmailForm';
import EmailPreview from './components/EmailPreview';

export default function Home() {
  const [generatedEmail, setGeneratedEmail] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            🎓 RAGmail
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            AI-Powered Professor Outreach Email Generator
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Generate personalized emails using RAG & LLM technology
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left: Form */}
          <EmailForm 
            onEmailGenerated={setGeneratedEmail}
            loading={loading}
            setLoading={setLoading}
          />

          {/* Right: Preview */}
          <EmailPreview 
            email={generatedEmail}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
}
