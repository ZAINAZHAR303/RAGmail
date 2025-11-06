'use client';

import { useState } from 'react';

export default function EmailPreview({ email, loading }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (email?.email) {
      navigator.clipboard.writeText(email.email);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    if (!email?.email) return;

    const blob = new Blob([email.email], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `email_${email.selected_project}_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 flex items-center justify-center min-h-[500px]">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600 dark:text-gray-300 text-lg">
            🤖 AI is generating your email...
          </p>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-2">
            This may take a few seconds
          </p>
        </div>
      </div>
    );
  }

  if (!email) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 flex items-center justify-center min-h-[500px]">
        <div className="text-center">
          <div className="text-6xl mb-4">📧</div>
          <p className="text-gray-600 dark:text-gray-300 text-lg font-medium mb-2">
            Email Preview
          </p>
          <p className="text-gray-500 dark:text-gray-400 text-sm">
            Fill out the form and click "Generate Email" to see your personalized email here
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
      {/* Header with Actions */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">Generated Email</h2>
          <div className="flex gap-2">
            <button
              onClick={handleCopy}
              className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-colors text-sm font-medium"
            >
              {copied ? '✓ Copied!' : '📋 Copy'}
            </button>
            <button
              onClick={handleDownload}
              className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-colors text-sm font-medium"
            >
              💾 Download
            </button>
          </div>
        </div>
      </div>

      {/* Metadata */}
      <div className="bg-blue-50 dark:bg-gray-700 px-6 py-4 border-b border-blue-100 dark:border-gray-600">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-4">
            <span className="font-medium text-gray-700 dark:text-gray-300">
              📊 Selected Project:
            </span>
            <span className="text-blue-600 dark:text-blue-400 font-semibold">
              {email.selected_project}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="font-medium text-gray-700 dark:text-gray-300">
              📈 Relevance:
            </span>
            <span className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full font-bold">
              {email.relevance_score}/10
            </span>
          </div>
        </div>
      </div>

      {/* Email Content */}
      <div className="p-6 max-h-[600px] overflow-y-auto">
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6 font-mono text-sm">
          <pre className="whitespace-pre-wrap text-gray-800 dark:text-gray-200 leading-relaxed">
            {email.email}
          </pre>
        </div>
      </div>

      {/* Success Message */}
      {email.success && (
        <div className="bg-green-50 dark:bg-green-900/20 border-t border-green-100 dark:border-green-800 px-6 py-4">
          <p className="text-green-700 dark:text-green-400 text-sm font-medium">
            ✓ {email.message}
          </p>
        </div>
      )}
    </div>
  );
}
