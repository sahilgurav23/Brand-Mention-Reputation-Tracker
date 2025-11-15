"use client";

// Dashboard is a client component because it fetches data from the backend
// at runtime and reacts to user interactions (time range, refresh).
import { useState, useEffect } from "react";
import {
  TrendingUp,
  AlertCircle,
  MessageSquare,
  BarChart3,
  Zap,
  Filter,
  RefreshCw,
} from "lucide-react";
import {
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

// High-level metric values shown in the top cards.
interface MetricState {
  totalMentions: number;
  sentimentScore: number;
}

// One point in the mentions-over-time chart.
interface TimelinePoint {
  date: string;
  positive: number;
  negative: number;
  neutral: number;
}

// Single slice in the sentiment pie chart.
interface SentimentSlice {
  name: string;
  value: number;
  color: string;
}

// Bar data for the "Top Topics" chart.
interface TopicBar {
  name: string;
  mentions: number;
}

// Bar data for the "Top Sources" list.
interface SourceBar {
  name: string;
  mentions: number;
}

// Row in the "Recent Mentions" list.
interface MentionItem {
  id: number;
  author: string;
  content: string;
  source: string;
  sentiment: string;
  time: string;
}

// Backend base URL. You can override this via NEXT_PUBLIC_API_BASE_URL
// when deploying, otherwise it defaults to local FastAPI dev server.
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function Dashboard() {
  // (Reserved for future) could control different dashboard tabs.
  const [activeTab, setActiveTab] = useState("overview");
  const [timeRange, setTimeRange] = useState("7d");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [brandName, setBrandName] = useState<string | null>(null);

  const [metrics, setMetrics] = useState<MetricState | null>(null);
  const [timelineData, setTimelineData] = useState<TimelinePoint[]>([]);
  const [sentimentData, setSentimentData] = useState<SentimentSlice[]>([]);
  const [topics, setTopics] = useState<TopicBar[]>([]);
  const [sources, setSources] = useState<SourceBar[]>([]);
  const [mentions, setMentions] = useState<MentionItem[]>([]);

  const getDaysFromRange = (range: string) => {
    if (range === "24h") return 1;
    if (range === "30d") return 30;
    return 7;
  };

  // Main data loader: calls all backend analytics + mentions endpoints
  // in parallel for the selected time range.
  const fetchData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const days = getDaysFromRange(timeRange);

      const [summaryRes, timelineRes, sentimentRes, topicsRes, sourcesRes, mentionsRes] =
        await Promise.all([
          fetch(`${API_BASE_URL}/api/analytics/summary?days=${days}`),
          fetch(`${API_BASE_URL}/api/analytics/timeline?days=${days}`),
          fetch(`${API_BASE_URL}/api/analytics/sentiment?days=${days}`),
          fetch(`${API_BASE_URL}/api/analytics/topics?days=${days}&limit=5`),
          fetch(`${API_BASE_URL}/api/analytics/sources?days=${days}`),
          fetch(`${API_BASE_URL}/api/mentions?days=${days}&limit=10`),
        ]);

      if (!summaryRes.ok) throw new Error("Failed to load summary");

      const summary = await summaryRes.json();
      const timelineJson = timelineRes.ok ? await timelineRes.json() : { timeline: {} };
      const sentimentJson = sentimentRes.ok
        ? await sentimentRes.json()
        : { positive: 0, negative: 0, neutral: 0, total: 0 };
      const topicsJson = topicsRes.ok ? await topicsRes.json() : { topics: [] };
      const sourcesJson = sourcesRes.ok ? await sourcesRes.json() : { sources: [] };
      const mentionsJson = mentionsRes.ok ? await mentionsRes.json() : [];

      // Metrics
      const total = typeof summary.total_mentions === "number" ? summary.total_mentions : 0;
      const positive = sentimentJson.positive ?? 0;
      const negative = sentimentJson.negative ?? 0;
      const neutral = sentimentJson.neutral ?? 0;
      const sentimentTotal = positive + negative + neutral;
      const sentimentScore =
        sentimentTotal > 0 ? Math.round(((positive - negative) / sentimentTotal + 1) * 50) : 0;

      setMetrics({ totalMentions: total, sentimentScore });

      // Timeline -> array for recharts
      const timelineArray: TimelinePoint[] = Object.entries(
        timelineJson.timeline ?? {}
      ).map(([date, values]: [string, any]) => ({
        date,
        positive: values.positive ?? 0,
        negative: values.negative ?? 0,
        neutral: values.neutral ?? 0,
      }));
      setTimelineData(timelineArray);

      // Sentiment pie chart
      const sentimentSlices: SentimentSlice[] = [
        { name: "Positive", value: positive, color: "#10b981" },
        { name: "Neutral", value: neutral, color: "#6b7280" },
        { name: "Negative", value: negative, color: "#ef4444" },
      ];
      setSentimentData(sentimentSlices);

      // Topics
      const topicBars: TopicBar[] = (topicsJson.topics ?? []).map((t: any) => ({
        name: t.topic ?? "Unknown",
        mentions: t.count ?? 0,
      }));
      setTopics(topicBars);

      // Sources
      const sourceBars: SourceBar[] = (sourcesJson.sources ?? []).map((s: any) => ({
        name: s.source ?? "Unknown",
        mentions: s.count ?? 0,
      }));
      setSources(sourceBars);

      // Recent mentions
      const mentionItems: MentionItem[] = (mentionsJson ?? []).map((m: any) => ({
        id: m.id,
        author: m.author || "Unknown",
        content: m.content || "",
        source: m.source || "Unknown",
        sentiment: m.sentiment || "neutral",
        time: m.created_at || "",
      }));
      setMentions(mentionItems);

      // Record when the dashboard was last refreshed successfully.
      setLastUpdated(new Date().toLocaleString());
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to load data");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeRange]);

  // Load brand settings once so we can show the current brand name
  // in the dashboard header.
  useEffect(() => {
    const loadSettings = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/settings`);
        if (!res.ok) return;
        const data = await res.json();
        if (data && typeof data.brand_name === "string") {
          setBrandName(data.brand_name || null);
        }
      } catch {
        // If settings fail to load, we simply keep the generic title.
      }
    };

    loadSettings();
  }, []);

  const handleRefresh = () => {
    fetchData();
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-slate-200 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                  {brandName || "Brand Tracker"}
                </h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  {brandName
                    ? `Real-time mention monitoring for ${brandName}`
                    : "Real-time Mention Monitoring"}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <button
                onClick={handleRefresh}
                disabled={isLoading}
                className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors disabled:opacity-50"
              >
                <RefreshCw
                  className={`w-5 h-5 text-slate-600 dark:text-slate-400 ${
                    isLoading ? "animate-spin" : ""
                  }`}
                />
              </button>
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm"
              >
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
              </select>
              {lastUpdated && (
                <span className="hidden md:inline text-xs text-slate-500 dark:text-slate-400">
                  Last updated: {lastUpdated}
                </span>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Metrics Grid - high level KPIs for the selected time range */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard
            icon={MessageSquare}
            label="Total Mentions"
            value={metrics ? metrics.totalMentions : "-"}
            change={0}
            color="blue"
          />
          <MetricCard
            icon={TrendingUp}
            label="Sentiment Score"
            value={metrics ? `${metrics.sentimentScore}%` : "-"}
            change={0}
            color="green"
          />
          <MetricCard
            icon={AlertCircle}
            label="Active Alerts"
            value={"-"}
            change={0}
            color="red"
          />
          <MetricCard
            icon={Zap}
            label="Engagement Rate"
            value="-"
            change={0}
            color="purple"
          />
        </div>

        {/* Charts Section - timeline + sentiment overview */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Timeline Chart */}
          <div className="lg:col-span-2 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
              Mention Timeline
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1e293b",
                    border: "1px solid #475569",
                    borderRadius: "8px",
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="positive"
                  stroke="#10b981"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="negative"
                  stroke="#ef4444"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="neutral"
                  stroke="#6b7280"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Sentiment Distribution */}
          <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
              Sentiment Distribution
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sentimentData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }: { name: string; value: number }) => `${name} ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Topics and Sources */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Top Topics */}
          <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
              Top Topics
            </h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={topics}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" stroke="#94a3b8" angle={-45} textAnchor="end" height={100} />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1e293b",
                    border: "1px solid #475569",
                    borderRadius: "8px",
                  }}
                />
                <Bar dataKey="mentions" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top Sources */}
          <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
              Top Sources
            </h2>
            <div className="space-y-4">
              {sources.map((source) => (
                <div key={source.name} className="flex items-center justify-between">
                  <span className="text-slate-600 dark:text-slate-400">{source.name}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-purple-600"
                        style={{
                          width: `${(source.mentions / (sources[0]?.mentions || 1)) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="text-sm font-semibold text-slate-900 dark:text-white w-12 text-right">
                      {source.mentions}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Alerts and Recent Mentions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Alerts */}
          <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              Active Alerts
            </h2>
            <div className="text-sm text-slate-500 dark:text-slate-400">
              Alerts will appear here once alert rules are configured in the backend.
            </div>
          </div>

          {/* Recent Mentions */}
          <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              Recent Mentions
            </h2>
            {error && (
              <p className="text-sm text-red-600 dark:text-red-400 mb-3">
                Failed to load data from API. Please check that the backend is running
                on {API_BASE_URL}.
              </p>
            )}
            <div className="space-y-3">
              {mentions.length === 0 && !error && (
                <div className="text-sm text-slate-500 dark:text-slate-400">
                  <p>No mentions found for the selected time range.</p>
                  <p className="mt-1">
                    If this is a fresh setup, run <code>python news_ingest.py</code> in the
                    <code>backend</code> folder to pull live news mentions into the database.
                  </p>
                </div>
              )}
              {mentions.map((mention) => (
                <div
                  key={mention.id}
                  className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700"
                >
                  <div className="flex items-start justify-between mb-2">
                    <p className="font-semibold text-sm text-slate-900 dark:text-white">
                      {mention.author}
                    </p>
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        mention.sentiment === "positive"
                          ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                          : mention.sentiment === "negative"
                          ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
                          : "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200"
                      }`}
                    >
                      {mention.sentiment}
                    </span>
                  </div>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                    {mention.content}
                  </p>
                  <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-500">
                    <span>{mention.source}</span>
                    <span>{mention.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

interface MetricCardProps {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: string | number;
  change: number;
  color: "blue" | "green" | "red" | "purple";
}

function MetricCard({ icon: Icon, label, value, change, color }: MetricCardProps) {
  const colorClasses = {
    blue: "from-blue-500 to-blue-600",
    green: "from-green-500 to-green-600",
    red: "from-red-500 to-red-600",
    purple: "from-purple-500 to-purple-600",
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${colorClasses[color as keyof typeof colorClasses]} flex items-center justify-center`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <span
          className={`text-sm font-semibold ${
            change >= 0
              ? "text-green-600 dark:text-green-400"
              : "text-red-600 dark:text-red-400"
          }`}
        >
          {change >= 0 ? "+" : ""}{change}%
        </span>
      </div>
      <p className="text-slate-600 dark:text-slate-400 text-sm mb-1">{label}</p>
      <p className="text-3xl font-bold text-slate-900 dark:text-white">{value}</p>
    </div>
  );
}
