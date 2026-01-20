'use client'

import { useEffect, useRef } from 'react'

interface TimeSliderProps {
  currentTick: number
  onTickChange: (tick: number) => void
  isPlaying: boolean
  onPlayPause: (playing: boolean) => void
}

export default function TimeSlider({ currentTick, onTickChange, isPlaying, onPlayPause }: TimeSliderProps) {
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        onTickChange(currentTick + 1)
      }, 100) // Update every 100ms
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [isPlaying, currentTick, onTickChange])

  const formatTime = (ticks: number) => {
    const days = Math.floor(ticks / (24 * 60))
    const hours = Math.floor((ticks % (24 * 60)) / 60)
    const minutes = ticks % 60
    return `Day ${days + 1}, ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
  }

  return (
    <div className="px-6 py-4 border-b border-gray-200">
      <div className="flex items-center gap-4">
        <button
          onClick={() => onPlayPause(!isPlaying)}
          className="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700"
        >
          {isPlaying ? '⏸ Pause' : '▶ Play'}
        </button>

        <button
          onClick={() => onTickChange(0)}
          className="px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
        >
          ⏮ Reset
        </button>

        <div className="flex-1">
          <input
            type="range"
            min="0"
            max="10080" // 7 days * 24 hours * 60 minutes
            value={currentTick}
            onChange={(e) => onTickChange(parseInt(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        <div className="text-sm font-medium text-gray-700 min-w-[150px] text-right">
          {formatTime(currentTick)}
        </div>
      </div>
    </div>
  )
}
