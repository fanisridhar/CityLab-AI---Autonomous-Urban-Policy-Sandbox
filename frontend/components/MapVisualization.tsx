'use client'

import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { DeckGL } from '@deck.gl/react'
import { Map } from 'react-map-gl/mapbox'
import { ScatterplotLayer, PathLayer } from '@deck.gl/layers'

interface MapVisualizationProps {
  scenarioId: number | null
  currentTick: number
}

export default function MapVisualization({ scenarioId, currentTick }: MapVisualizationProps) {
  const mapContainer = useRef<HTMLDivElement>(null)
  const [viewState, setViewState] = useState({
    longitude: -122.4194,
    latitude: 37.7749,
    zoom: 12,
    pitch: 0,
    bearing: 0,
  })
  const [agentData, setAgentData] = useState<any[]>([])
  const [routeData, setRouteData] = useState<any[]>([])

  useEffect(() => {
    if (!scenarioId) return

    // Fetch simulation state for current tick
    const fetchState = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/v1/simulations/runs/${scenarioId}/states/${currentTick}`)
        if (response.ok) {
          const data = await response.json()
          
          // Transform agent states to deck.gl format
          const agents = Object.entries(data.agent_states || {}).map(([id, state]: [string, any]) => ({
            position: [state.location?.lon || 0, state.location?.lat || 0],
            id,
            ...state,
          }))
          setAgentData(agents)

          // Transform route data
          const routes = data.city_state?.transit_routes || []
          setRouteData(routes)
        }
      } catch (error) {
        console.error('Failed to fetch simulation state:', error)
      }
    }

    fetchState()
  }, [scenarioId, currentTick])

  const layers = [
    new ScatterplotLayer({
      id: 'agents',
      data: agentData,
      getPosition: (d: any) => d.position,
      getRadius: 50,
      getFillColor: [0, 100, 255, 200],
      radiusMinPixels: 3,
      radiusMaxPixels: 10,
    }),
    new PathLayer({
      id: 'transit-routes',
      data: routeData,
      getPath: (d: any) => d.path || [],
      getColor: [255, 0, 0, 200],
      widthMinPixels: 2,
    }),
  ]

  const mapboxToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || ''

  return (
    <div ref={mapContainer} className="w-full h-full">
      <DeckGL
        viewState={viewState}
        onViewStateChange={({ viewState }) => setViewState(viewState)}
        controller={true}
        layers={layers}
      >
        <Map
          mapboxAccessToken={mapboxToken}
          mapStyle="mapbox://styles/mapbox/light-v11"
          reuseMaps
        />
      </DeckGL>
    </div>
  )
}
