import { useState } from 'react'
import { Button } from '@/shadcn/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shadcn/components/ui/card'
import { Input } from '@/shadcn/components/ui/input'
import { Label } from '@/shadcn/components/ui/label'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight">Welcome to Your App</h1>
          <p className="text-xl text-muted-foreground">
            Built with ShadCN components and Tailwind CSS
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Counter Demo</CardTitle>
              <CardDescription>
                Basic state management with ShadCN components
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center">
                <p className="text-2xl font-semibold">{count}</p>
                <div className="flex gap-2 justify-center mt-4">
                  <Button
                    onClick={() => setCount(c => c + 1)}
                    variant="default"
                  >
                    Increment
                  </Button>
                  <Button
                    onClick={() => setCount(c => Math.max(0, c - 1))}
                    variant="outline"
                  >
                    Decrement
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Form Demo</CardTitle>
              <CardDescription>
                Basic form with ShadCN input components
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Name</Label>
                <Input id="name" placeholder="Enter your name" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" placeholder="Enter your email" />
              </div>
              <Button className="w-full">Submit</Button>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Getting Started</CardTitle>
            <CardDescription>
              Your project is ready for development
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 text-sm">
              <div>
                <strong>✅ ShadCN Components:</strong> Button, Card, Input, Label, and more
              </div>
              <div>
                <strong>✅ Styling:</strong> Tailwind CSS with custom design tokens
              </div>
              <div>
                <strong>✅ Type Safety:</strong> Full TypeScript support
              </div>
              <div>
                <strong>✅ Development:</strong> Hot reload and fast refresh
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App
