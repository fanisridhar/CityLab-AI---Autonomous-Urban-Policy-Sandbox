'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface MetricsDashboardProps {
  scenarioId: number | null
}

interface Metrics {
  avg_commute_time: number | null
  commute_time_change_pct: number | null
  transit_modal_share: number | null
  transit_ridership: number | null
  emissions_proxy: number | null
  service_coverage: number | null
  equity_index: number | null
}

export default function MetricsDashboard({ scenarioId }: MetricsDashboardProps) {
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [timeSeries, setTimeSeries] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!scenarioId) return
    fetchMetrics()
    fetchTimeSeries()
  }, [scenarioId])

  const fetchMetrics = async () => {
    if (!scenarioId) return
    setLoading(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      // Get latest run for scenario
      const runsResponse = await axios.get(`${apiUrl}/api/v1/scenarios/${scenarioId}/runs`)
      if (runsResponse.data.length > 0) {
        const latestRun = runsResponse.data[0]
        const metricsResponse = await axios.get(`${apiUrl}/api/v1/simulations/runs/${latestRun.id}/metrics`)
        setMetrics(metricsResponse.data)
      }
    } catch (error) {
      console.error('Failed to fetch metrics:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTimeSeries = async () => {
    if (!scenarioId) return
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const runsResponse = await axios.get(`${apiUrl}/api/v1/scenarios/${scenarioId}/runs`)
      if (runsResponse.data.length > 0) {
        const latestRun = runsResponse.data[0]
        const statesResponse = await axios.get(`${apiUrl}/api/v1/simulations/runs/${latestRun.id}/states`)
        
        // Transform to time series
        const series = statesResponse.data.map((state: any) => ({
          tick: state.tick,
          commute_time: state.city_state?.metrics?.avg_commute_time || 0,
          transit_ridership: state.city_state?.transit_ridership || 0,
          equity_index: state.city_state?.metrics?.equity_index || 0,
        }))
        setTimeSeries(series)
      }
    } catch (error) {
      console.error('Failed to fetch time series:', error)
    }
  }

  if (!scenarioId) {
    return (
      <div className="p-4 text-center text-gray-500">
        Select a scenario to view metrics
      </div>
    )
  }

  if (loading) {
    return (
      <div className="p-4">
        <div className="animate-pulse">Loading metrics...</div>
      </div>
    )
  }

  return (
    <div className="p-4">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Metrics</h3>
      
      {/* Key Metrics Grid */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-50 rounded-lg p-3">
          <div className="text-sm text-gray-600">Avg Commute Time</div>
          <div className="text-2xl font-bold text-gray-900">
            {metrics?.avg_commute_time?.toFixed(1) || 'N/A'} min
          </div>
          {metrics?.commute_time_change_pct && (
            <div className={`text-xs mt-1 ${
              metrics.commute_time_change_pct < 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {metrics.commute_time_change_pct > 0 ? '+' : ''}
              {metrics.commute_time_change_pct.toFixed(1)}%
            </div>
          )}
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="text-sm text-gray-600">Transit Modal Share</div>
          <div className="text-2xl font-bold text-gray-900">
            {metrics?.transit_modal_share ? (metrics.transit_modal_share * 100).toFixed(1) : 'N/A'}%
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="text-sm text-gray-600">Transit Ridership</div>
          <div className="text-2xl font-bold text-gray-900">
            {metrics?.transit_ridership?.toLocaleString() || 'N/A'}
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="text-sm text-gray-600">Equity Index</div>
          <div className="text-2xl font-bold text-gray-900">
            {metrics?.equity_index?.toFixed(2) || 'N/A'}
          </div>
        </div>
      </div>

      {/* Time Series Chart */}
      {timeSeries.length > 0 && (
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={timeSeries}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="tick" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="commute_time" stroke="#0ea5e9" name="Commute Time (min)" />
              <Line type="monotone" dataKey="transit_ridership" stroke="#10b981" name="Transit Ridership" />
              <Line type="monotone" dataKey="equity_index" stroke="#f59e0b" name="Equity Index" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
