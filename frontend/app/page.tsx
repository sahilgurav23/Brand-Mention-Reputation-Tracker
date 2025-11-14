"use client";

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

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const [timeRange, setTimeRange] = useState("7d");
  const [isLoading, setIsLoading] = useState(false);

  // Mock data - Replace with actual API calls
  const mockMetrics = {
    totalMentions: 2847,
    positiveChange: 12.5,
    sentimentScore: 68,
    alertsActive: 3,
  };

  const mockSentimentData = [
    { name: "Positive", value: 1250, color: "#10b981" },
    { name: "Neutral", value: 980, color: "#6b7280" },
    { name: "Negative", value: 617, color: "#ef4444" },
  ];

  const mockTimelineData = [
    { date: "Mon", positive: 120, negative: 45, neutral: 80 },
    { date: "Tue", positive: 145, negative: 52, neutral: 95 },
    { date: "Wed", positive: 165, negative: 38, neutral: 110 },
    { date: "Thu", positive: 190, negative: 55, neutral: 125 },
    { date: "Fri", positive: 210, negative: 48, neutral: 140 },
    { date: "Sat", positive: 185, negative: 62, neutral: 120 },
    { date: "Sun", positive: 235, negative: 41, neutral: 155 },
  ];

  const mockTopics = [
    { name: "Product Quality", mentions: 450 },
    { name: "Customer Service", mentions: 380 },
    { name: "Pricing", mentions: 290 },
    { name: "Shipping", mentions: 245 },
    { name: "Brand Values", mentions: 180 },
  ];

  const mockSources = [
    { name: "Twitter", mentions: 1200 },
    { name: "Reddit", mentions: 850 },
    { name: "News", mentions: 420 },
    { name: "Blogs", mentions: 377 },
  ];

  const mockAlerts = [
    {
      id: 1,
      type: "spike",
      title: "Mention Spike Detected",
      description: "245% increase in mentions in the last 2 hours",
      severity: "high",
      time: "2 hours ago",
    },
    {
      id: 2,
      type: "sentiment",
      title: "Negative Sentiment Shift",
      description: "Negative mentions increased to 35% of total",
      severity: "medium",
      time: "4 hours ago",
    },
    {
      id: 3,
      type: "trend",
      title: "Trending Topic",
      description: '"Product Quality" is trending with 450 mentions',
      severity: "low",
      time: "6 hours ago",
    },
  ];

  const mockMentions = [
    {
      id: 1,
      author: "Sarah Johnson",
      content: "Love the new product update! Great improvements.",
      source: "Twitter",
      sentiment: "positive",
      time: "2 hours ago",
    },
    {
      id: 2,
      author: "Tech Review Daily",
      content: "Comprehensive review of the latest features...",
      source: "Blog",
      sentiment: "neutral",
      time: "3 hours ago",
    },
    {
      id: 3,
      author: "Customer Support",
      content: "Disappointed with the recent changes",
      source: "Reddit",
      sentiment: "negative",
      time: "4 hours ago",
    },
  ];

  const handleRefresh = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 1000);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                  Brand Tracker
                </h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  Real-time Mention Monitoring
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
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            icon={MessageSquare}
            label="Total Mentions"
            value={mockMetrics.totalMentions}
            change={mockMetrics.positiveChange}
            color="blue"
          />
          <MetricCard
            icon={TrendingUp}
            label="Sentiment Score"
            value={`${mockMetrics.sentimentScore}%`}
            change={5.2}
            color="green"
          />
          <MetricCard
            icon={AlertCircle}
            label="Active Alerts"
            value={mockMetrics.alertsActive}
            change={-2}
            color="red"
          />
          <MetricCard
            icon={Zap}
            label="Engagement Rate"
            value="24.5%"
            change={8.1}
            color="purple"
          />
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Timeline Chart */}
          <div className="lg:col-span-2 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
              Mention Timeline
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockTimelineData}>
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
          <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
              Sentiment Distribution
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={mockSentimentData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }: { name: string; value: number }) => `${name} ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {mockSentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Topics and Sources */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Top Topics */}
          <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
              Top Topics
            </h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={mockTopics}>
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
              {mockSources.map((source) => (
                <div key={source.name} className="flex items-center justify-between">
                  <span className="text-slate-600 dark:text-slate-400">{source.name}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-purple-600"
                        style={{
                          width: `${(source.mentions / 1200) * 100}%`,
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
            <div className="space-y-3">
              {mockAlerts.map((alert) => (
                <div
                  key={alert.id}
                  className={`p-3 rounded-lg border-l-4 ${
                    alert.severity === "high"
                      ? "border-l-red-500 bg-red-50 dark:bg-red-950"
                      : alert.severity === "medium"
                      ? "border-l-yellow-500 bg-yellow-50 dark:bg-yellow-950"
                      : "border-l-blue-500 bg-blue-50 dark:bg-blue-950"
                  }`}
                >
                  <p className="font-semibold text-sm text-slate-900 dark:text-white">
                    {alert.title}
                  </p>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                    {alert.description}
                  </p>
                  <p className="text-xs text-slate-500 dark:text-slate-500 mt-2">
                    {alert.time}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Mentions */}
          <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              Recent Mentions
            </h2>
            <div className="space-y-3">
              {mockMentions.map((mention) => (
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
