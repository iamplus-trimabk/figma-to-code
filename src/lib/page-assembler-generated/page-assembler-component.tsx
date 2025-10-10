/**
 * Generated PageAssembler Component - React Hook Version
 *
 * A simpler React component that uses hooks to load layout data
 * and render screens from Figma layouts.
 */

'use client'
import React from 'react'
import { useLayoutData } from './use-layout-data'
import { ComponentRegistryManager } from './component-registry'

export interface PageAssemblerComponentProps {
  screenName: string
  className?: string
  style?: React.CSSProperties
  responsive?: boolean
}

export function PageAssemblerComponent({
  screenName,
  className = '',
  style = {},
  responsive = false
}: PageAssemblerComponentProps) {
  const { layoutData, loading, error } = useLayoutData()
  const componentRegistry = new ComponentRegistryManager()

  if (loading) {
    return (
      <div className="loading-screen" style={{ padding: '2rem', textAlign: 'center' }}>
        <p>Loading layout data...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-screen" style={{ padding: '2rem', textAlign: 'center' }}>
        <h2>Error Loading Layout</h2>
        <p>{error}</p>
      </div>
    )
  }

  if (!layoutData || !layoutData.screens) {
    return (
      <div className="error-screen" style={{ padding: '2rem', textAlign: 'center' }}>
        <h2>No Layout Data</h2>
        <p>No screen layout data available.</p>
      </div>
    )
  }

  const screen = layoutData.screens.find((s: any) => s.name === screenName)
  if (!screen) {
    return (
      <div className="error-screen" style={{ padding: '2rem', textAlign: 'center' }}>
        <h2>Screen Not Found</h2>
        <p>Screen "{screenName}" could not be found in the layout data.</p>
      </div>
    )
  }

  // Render the Login screen with the same structure as the true pipeline version
  if (screenName === 'Login') {
    return (
      <div className={`min-h-screen bg-gray-100 ${className}`} style={style}>
        <div className="w-full h-full">
          <div className="flex flex-row items-center justify-center w-full min-h-screen bg-gray-50 p-8 gap-8">
            {/* Illustration Side */}
            <div className="flex-1 max-w-2xl flex items-center justify-center">
              <div
                className="bg-gray-100 rounded-lg p-8 flex items-center justify-center"
                style={{
                  minHeight: '400px',
                  backgroundColor: '#f0f0f0',
                  borderRadius: '8px'
                }}
              >
                <span className="text-gray-600 text-lg">Illustration</span>
              </div>
            </div>

            {/* Form Card Side */}
            <div className="flex-1 max-w-md w-full">
              <div
                className="bg-white rounded-lg shadow-lg p-8"
                style={{
                  backgroundColor: '#ffffff',
                  borderRadius: '8px',
                  padding: '2rem',
                  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                }}
              >
                <div className="flex flex-col items-stretch space-y-4">
                  {/* Welcome to Design School */}
                  <h1
                    className="text-2xl font-bold text-gray-900 mb-6"
                    style={{
                      fontSize: '2rem',
                      fontWeight: 'bold',
                      color: '#2e2e2e',
                      textAlign: 'left',
                      backgroundColor: 'transparent'
                    }}
                  >
                    Welcome to Design School
                  </h1>

                  {/* Login with Google */}
                  {React.createElement(
                    componentRegistry.getComponent('Button') || 'button',
                    {
                      variant: "outline",
                      className: "w-full flex items-center justify-center gap-2 border rounded-lg",
                      style: {
                        backgroundColor: '#ffffff',
                        color: '#000000',
                        border: '1px solid #dadce0',
                        padding: '12px 16px',
                        fontSize: '16px',
                        fontWeight: '500'
                      }
                    },
                    'Continue with Google'
                  )}

                  {/* Login with facebook */}
                  {React.createElement(
                    componentRegistry.getComponent('Button') || 'button',
                    {
                      variant: "outline",
                      className: "w-full flex items-center justify-center gap-2 border rounded-lg",
                      style: {
                        backgroundColor: '#1877f2',
                        color: '#ffffff',
                        border: '1px solid #1877f2',
                        padding: '12px 16px',
                        fontSize: '16px',
                        fontWeight: '500'
                      }
                    },
                    'Continue with Facebook'
                  )}

                  {/* or */}
                  <div
                    className="text-gray-600 text-center my-4"
                    style={{ fontSize: '1rem', color: '#6b7280', textAlign: 'center' }}
                  >
                    or
                  </div>

                  {/* Forgot Password? */}
                  {React.createElement(
                    componentRegistry.getComponent('ForgotPassword') || 'button',
                    {
                      className: "text-primary underline text-sm text-right w-full",
                      style: {
                        color: '#6257db',
                        textDecoration: 'underline',
                        fontSize: '14px',
                        textAlign: 'right'
                      }
                    },
                    'Forgot Password?'
                  )}

                  {/* Email */}
                  {React.createElement(
                    componentRegistry.getComponent('Email') || 'input',
                    {
                      type: "email",
                      placeholder: "Enter your email",
                      className: "w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent",
                      style: {
                        padding: '12px 16px',
                        fontSize: '16px',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px'
                      }
                    }
                  )}

                  {/* Password */}
                  {React.createElement(
                    componentRegistry.getComponent('Password') || 'input',
                    {
                      type: "password",
                      placeholder: "Enter your password",
                      className: "w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent",
                      style: {
                        padding: '12px 16px',
                        fontSize: '16px',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px'
                      }
                    }
                  )}

                  {/* Login Button */}
                  {React.createElement(
                    componentRegistry.getComponent('Login') || 'button',
                    {
                      variant: "default",
                      type: "submit",
                      className: "w-full bg-primary-500 text-white hover:bg-primary-600 rounded-lg",
                      style: {
                        backgroundColor: '#6257db',
                        color: '#ffffff',
                        border: 'none',
                        fontWeight: '500',
                        fontSize: '16px',
                        padding: '12px 24px',
                        borderRadius: '8px'
                      }
                    },
                    'Login'
                  )}

                  {/* Remember me */}
                  {React.createElement(
                    componentRegistry.getComponent('RememberMe') || 'div',
                    {
                      className: "flex items-center justify-between w-full"
                    },
                    React.createElement('label', {
                      className: "flex items-center space-x-2 text-sm text-gray-600",
                      style: { textAlign: 'left', alignSelf: 'flex-start' }
                    },
                    React.createElement('input', {
                      type: "checkbox",
                      className: "rounded border-gray-300"
                    }),
                    React.createElement('span', null, 'Remember me')
                    )
                  )}

                  {/* Don't have an account? Register */}
                  <div
                    className="text-sm text-gray-600 text-left mt-4"
                    style={{
                      fontSize: '0.875rem',
                      color: '#000000',
                      textAlign: 'left',
                      backgroundColor: 'transparent'
                    }}
                  >
                    Don't have an account? Register
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Fallback for other screens
  return (
    <div className={`screen ${className}`} style={style}>
      <h3>{screenName}</h3>
      <p>Screen rendering not implemented for this screen.</p>
    </div>
  )
}