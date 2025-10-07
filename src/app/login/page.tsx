/**
 * Login Page - Complete Page Assembly using Stage 4 Page Assembler
 *
 * This page demonstrates the complete Stage 4 implementation:
 * - Uses Page Assembler to render the Login screen from Figma layouts
 * - Components are positioned and sized exactly as in the original design
 * - Generated components from Stage 3 are used in the assembly
 */

import { PageAssemblerComponent } from '@/lib/page-assembler'

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Stage 4: Page Assembler Demo
          </h1>
          <p className="text-gray-600">
            Complete Login page assembled from Figma layouts using generated components
          </p>
        </div>

        {/* Container for the assembled login screen - Now Responsive! */}
        <div className="w-full max-w-md mx-auto">
          <div className="border border-gray-300 rounded-lg shadow-lg overflow-hidden">
            <PageAssemblerComponent
              screenName="Login"
              className="responsive-login-screen"
              responsive={true}
              style={{
                // No more scaling - use responsive layout!
                minHeight: '500px',
              }}
            />
          </div>
        </div>

        {/* Information panel */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Page Assembler Features Demonstrated:
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium text-gray-700 mb-2">✅ Layout Parsing</h3>
              <p className="text-sm text-gray-600">
                Parses Figma screen layouts to extract component hierarchy, positioning, and sizing data
              </p>
            </div>
            <div>
              <h3 className="font-medium text-gray-700 mb-2">✅ Component Registry</h3>
              <p className="text-sm text-gray-600">
                Maps Figma component names to generated React components from Stage 3
              </p>
            </div>
            <div>
              <h3 className="font-medium text-gray-700 mb-2">✅ Responsive Layout System</h3>
              <p className="text-sm text-gray-600">
                Components use modern flexbox layout instead of absolute positioning
              </p>
            </div>
            <div>
              <h3 className="font-medium text-gray-700 mb-2">✅ Mobile-Friendly Design</h3>
              <p className="text-sm text-gray-600">
                Components adapt to different screen sizes with responsive containers
              </p>
            </div>
          </div>
        </div>

        {/* Component mapping reference */}
        <div className="mt-6 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Component Mapping Reference:
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="border rounded p-2">
              <strong>bg</strong> → Bg component
            </div>
            <div className="border rounded p-2">
              <strong>Email</strong> → Email component
            </div>
            <div className="border rounded p-2">
              <strong>Password</strong> → Password component
            </div>
            <div className="border rounded p-2">
              <strong>button</strong> → Button component
            </div>
            <div className="border rounded p-2">
              <strong>Remember me</strong> → RememberMe component
            </div>
            <div className="border rounded p-2">
              <strong>Forgot Password?</strong> → ForgotPassword component
            </div>
            <div className="border rounded p-2">
              <strong>Illustration</strong> → Placeholder
            </div>
            <div className="border rounded p-2">
              <strong>Social buttons</strong> → Button variants
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}