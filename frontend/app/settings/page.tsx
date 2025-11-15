"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

// Shape of settings as returned by the backend /api/settings endpoint.
interface SettingsPayload {
  news_api_key: string | null;
  twitter_api_key: string | null;
  twitter_api_secret: string | null;
  reddit_client_id: string | null;
  reddit_client_secret: string | null;
  brand_name: string | null;
  brand_keywords: string | null;
  search_query: string | null;
}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function SettingsPage() {
  const router = useRouter();
  const [settings, setSettings] = useState<SettingsPayload | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showNewsKey, setShowNewsKey] = useState(false);
  const [showTwitterKey, setShowTwitterKey] = useState(false);
  const [showTwitterSecret, setShowTwitterSecret] = useState(false);
  const [showRedditId, setShowRedditId] = useState(false);
  const [showRedditSecret, setShowRedditSecret] = useState(false);

  // Simple client-side guard: if not "logged in", redirect to /login.
  useEffect(() => {
    if (typeof window === "undefined") return;
    const authed = localStorage.getItem("brandTrackerAuthed");
    if (!authed) {
      router.push("/login");
    }
  }, [router]);

  // Load current settings from backend.
  useEffect(() => {
    const load = async () => {
      try {
        setError(null);
        const res = await fetch(`${API_BASE_URL}/api/settings`);
        if (!res.ok) throw new Error("Failed to load settings");
        const data = await res.json();
        setSettings(data);
      } catch (err: any) {
        setError(err.message || "Failed to load settings");
      }
    };
    load();
  }, []);

  const handleChange = (field: keyof SettingsPayload, value: string) => {
    setSettings((prev) =>
      prev
        ? { ...prev, [field]: value }
        : {
            news_api_key: "",
            twitter_api_key: "",
            twitter_api_secret: "",
            reddit_client_id: "",
            reddit_client_secret: "",
            brand_name: "",
            brand_keywords: "",
            search_query: "",
            [field]: value,
          }
    );
  };

  const handleSave = async () => {
    if (!settings) return;
    try {
      setIsSaving(true);
      setError(null);
      setSuccess(null);

      const res = await fetch(`${API_BASE_URL}/api/settings`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(settings),
      });

      if (!res.ok) throw new Error("Failed to save settings");

      const data = await res.json();
      setSettings(data);
      setSuccess("Settings saved successfully.");
    } catch (err: any) {
      setError(err.message || "Failed to save settings");
    } finally {
      setIsSaving(false);
    }
  };

  if (!settings) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <p className="text-sm text-slate-500 dark:text-slate-400">Loading settings...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      <header className="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-slate-900 dark:text-white">Settings</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Manage API keys and brand configuration used by the backend.
            </p>
          </div>
          <button
            onClick={() => router.push("/")}
            className="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            Back to Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {error && (
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        )}
        {success && !error && (
          <p className="text-sm text-green-600 dark:text-green-400">{success}</p>
        )}

        {/* API Keys section */}
        <section className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-900 dark:text-white mb-1">API Keys</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-4">
            These values are used by the backend when calling external services.
          </p>

          <div className="space-y-4">
            {/* NewsAPI */}
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                NewsAPI Key
              </label>
              <div className="flex gap-2">
                <input
                  type={showNewsKey ? "text" : "password"}
                  className="flex-1 px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={settings.news_api_key ?? ""}
                  onChange={(e) => handleChange("news_api_key", e.target.value)}
                />
                <button
                  type="button"
                  onClick={() => setShowNewsKey((v) => !v)}
                  className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-200 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700"
                >
                  {showNewsKey ? "Hide" : "View"}
                </button>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Stored in the database; used by the News ingestion script and services.
              </p>
            </div>

            {/* Twitter */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Twitter API Key
                </label>
                <div className="flex gap-2">
                  <input
                    type={showTwitterKey ? "text" : "password"}
                    className="flex-1 px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={settings.twitter_api_key ?? ""}
                    onChange={(e) => handleChange("twitter_api_key", e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={() => setShowTwitterKey((v) => !v)}
                    className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-200 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700"
                  >
                    {showTwitterKey ? "Hide" : "View"}
                  </button>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Twitter API Secret
                </label>
                <div className="flex gap-2">
                  <input
                    type={showTwitterSecret ? "text" : "password"}
                    className="flex-1 px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={settings.twitter_api_secret ?? ""}
                    onChange={(e) => handleChange("twitter_api_secret", e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={() => setShowTwitterSecret((v) => !v)}
                    className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-200 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700"
                  >
                    {showTwitterSecret ? "Hide" : "View"}
                  </button>
                </div>
              </div>
            </div>

            {/* Reddit */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Reddit Client ID
                </label>
                <div className="flex gap-2">
                  <input
                    type={showRedditId ? "text" : "password"}
                    className="flex-1 px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={settings.reddit_client_id ?? ""}
                    onChange={(e) => handleChange("reddit_client_id", e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={() => setShowRedditId((v) => !v)}
                    className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-200 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700"
                  >
                    {showRedditId ? "Hide" : "View"}
                  </button>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Reddit Client Secret
                </label>
                <div className="flex gap-2">
                  <input
                    type={showRedditSecret ? "text" : "password"}
                    className="flex-1 px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={settings.reddit_client_secret ?? ""}
                    onChange={(e) => handleChange("reddit_client_secret", e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={() => setShowRedditSecret((v) => !v)}
                    className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-200 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700"
                  >
                    {showRedditSecret ? "Hide" : "View"}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Brand configuration section */}
        <section className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-900 dark:text-white mb-1">Brand Configuration</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-4">
            Controls what keywords and queries are used when collecting mentions.
          </p>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                Brand Name
              </label>
              <input
                className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={settings.brand_name ?? ""}
                onChange={(e) => handleChange("brand_name", e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                Brand Keywords (comma-separated)
              </label>
              <input
                className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={settings.brand_keywords ?? ""}
                onChange={(e) => handleChange("brand_keywords", e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                Search Query
              </label>
              <input
                className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={settings.search_query ?? ""}
                onChange={(e) => handleChange("search_query", e.target.value)}
              />
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Used as the primary query when collecting mentions (e.g. NewsAPI).
              </p>
            </div>
          </div>
        </section>

        <div className="flex justify-end">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 text-white text-sm font-medium disabled:opacity-60"
          >
            {isSaving ? "Saving..." : "Save Settings"}
          </button>
        </div>
      </main>
    </div>
  );
}
