'use client'

import { useState } from 'react'
import MapVisualization from '@/components/MapVisualization'
import ScenarioPanel from '@/components/ScenarioPanel'
import MetricsDashboard from '@/components/MetricsDashboard'
import TimeSlider from '@/components/TimeSlider'

export default function Home() {
  const [selectedScenario, setSelectedScenario] = useState<number | null>(null)
  const [currentTick, setCurrentTick] = useState<number>(0)
  const [isPlaying, setIsPlaying] = useState<boolean>(false)

  return (
    <main className="flex h-screen flex-col">
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">CityLab AI</h1>
            <p className="text-sm text-gray-600">Autonomous Urban Policy Sandbox</p>
          </div>
          <nav className="flex gap-4">
            <button className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900">
              Scenarios
            </button>
            <button className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900">
              Data
            </button>
            <button className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900">
              Docs
            </button>
          </nav>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel - Scenarios */}
        <aside className="w-80 bg-gray-50 border-r border-gray-200 overflow-y-auto">
          <ScenarioPanel
            selectedScenario={selectedScenario}
            onSelectScenario={setSelectedScenario}
          />
        </aside>

        {/* Main Content - Map */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 relative">
            <MapVisualization
              scenarioId={selectedScenario}
              currentTick={currentTick}
            />
          </div>

          {/* Bottom Panel - Metrics and Controls */}
          <div className="bg-white border-t border-gray-200">
            <TimeSlider
              currentTick={currentTick}
              onTickChange={setCurrentTick}
              isPlaying={isPlaying}
              onPlayPause={setIsPlaying}
            />
            <MetricsDashboard scenarioId={selectedScenario} />
          </div>
        </div>
      </div>
    </main>
  )
}
