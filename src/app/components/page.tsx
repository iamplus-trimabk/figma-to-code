"use client"

import * as React from "react"
import { useState } from "react"
import { Button } from "@/components/button-demo"
import { Input } from "@/components/input-demo"
import { Card } from "@/components/card-demo"
import { Alert } from "@/components/alert-demo"

// Tab interface
interface Tab {
  id: string
  label: string
  component: React.ReactNode
}

export default function ComponentsPage() {
  const [activeTab, setActiveTab] = useState("buttons")

  // Define tabs for each component category
  const tabs: Tab[] = [
    {
      id: "buttons",
      label: "Buttons",
      component: <Button />
    },
    {
      id: "inputs",
      label: "Inputs",
      component: <Input />
    },
    {
      id: "cards",
      label: "Cards",
      component: <Card />
    },
    {
      id: "alerts",
      label: "Alerts",
      component: <Alert />
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">
                Component Library
              </h1>
              <span className="ml-3 px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full">
                Phase 1 + Phase 2
              </span>
            </div>
            <div className="text-sm text-gray-500">
              Stage 3 Component Generator
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8" aria-label="Tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap
                  ${activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                  transition-colors duration-200
                `}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Info */}
        <div className="mb-8">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">
                  Currently Viewing: {tabs.find(t => t.id === activeTab)?.label}
                </h3>
                <div className="mt-2 text-sm text-blue-700">
                  <p>Component Source:
                    {activeTab === "buttons" && " Phase 1 (Manual) + Phase 2 (Template)"}
                    {activeTab === "inputs" && " Phase 1 (Manual) + Phase 2 (Template)"}
                    {activeTab === "cards" && " Phase 1 (Manual) + Phase 2 (Template)"}
                    {activeTab === "alerts" && " Phase 1 (Manual)"}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Component Display */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="border-b border-gray-200 pb-4 mb-6">
            <h2 className="text-lg font-semibold text-gray-900">
              {tabs.find(t => t.id === activeTab)?.label} Components
            </h2>
            <p className="mt-1 text-sm text-gray-600">
              Interactive component demonstrations with various states and configurations.
            </p>
          </div>

          <div className="min-h-[400px]">
            {tabs.find(t => t.id === activeTab)?.component}
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Component Status</h3>
            <div className="space-y-2 text-xs text-gray-600">
              <div className="flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Button: Phase 1 + Phase 2
              </div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Input: Phase 1 + Phase 2
              </div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Card: Phase 1 + Phase 2
              </div>
              <div className="flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Alert: Phase 1 Only
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Template System</h3>
            <div className="text-xs text-gray-600">
              <p className="mb-2">✅ Jinja2 templates working</p>
              <p className="mb-2">✅ Component generation active</p>
              <p className="mb-2">✅ Design tokens integrated</p>
              <p>⚠️ Formatting refinement needed</p>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Quick Links</h3>
            <div className="space-y-1 text-xs">
              <a href="/button-test" className="block text-blue-600 hover:text-blue-800">Button Test Page</a>
              <a href="/input-test" className="block text-blue-600 hover:text-blue-800">Input Test Page</a>
              <a href="/card-test" className="block text-blue-600 hover:text-blue-800">Card Test Page</a>
              <a href="/alert-test" className="block text-blue-600 hover:text-blue-800">Alert Test Page</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}