'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'

interface Scenario {
  id: number
  name: string
  description: string | null
  policy_type: string | null
  created_at: string
}

interface ScenarioPanelProps {
  selectedScenario: number | null
  onSelectScenario: (id: number | null) => void
}

export default function ScenarioPanel({ selectedScenario, onSelectScenario }: ScenarioPanelProps) {
  const [scenarios, setScenarios] = useState<Scenario[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchScenarios()
  }, [])

  const fetchScenarios = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await axios.get(`${apiUrl}/api/v1/scenarios`)
      setScenarios(response.data)
    } catch (error) {
      console.error('Failed to fetch scenarios:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateScenario = () => {
    // TODO: Open create scenario modal
    console.log('Create scenario')
  }

  if (loading) {
    return (
      <div className="p-4">
        <div className="animate-pulse">Loading scenarios...</div>
      </div>
    )
  }

  return (
    <div className="p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Scenarios</h2>
        <button
          onClick={handleCreateScenario}
          className="px-3 py-1.5 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700"
        >
          + New
        </button>
      </div>

      <div className="space-y-2">
        {scenarios.map((scenario) => (
          <div
            key={scenario.id}
            onClick={() => onSelectScenario(scenario.id)}
            className={`p-3 rounded-lg border cursor-pointer transition-colors ${
              selectedScenario === scenario.id
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-200 hover:border-gray-300 bg-white'
            }`}
          >
            <h3 className="font-medium text-gray-900">{scenario.name}</h3>
            {scenario.description && (
              <p className="text-sm text-gray-600 mt-1 line-clamp-2">{scenario.description}</p>
            )}
            {scenario.policy_type && (
              <span className="inline-block mt-2 px-2 py-0.5 text-xs font-medium text-gray-700 bg-gray-100 rounded">
                {scenario.policy_type}
              </span>
            )}
          </div>
        ))}

        {scenarios.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <p>No scenarios yet</p>
            <button
              onClick={handleCreateScenario}
              className="mt-2 text-sm text-primary-600 hover:text-primary-700"
            >
              Create your first scenario
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
