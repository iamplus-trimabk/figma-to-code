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
    <div className="min-h-screen bg-gray-100">
      <div className="w-full h-full">
        {/* Direct page assembly - let the PageAssembler handle the layout */}
        <PageAssemblerComponent
          screenName="Login"
          className="responsive-login-screen"
          responsive={true}
        />
      </div>
    </div>
  )
}