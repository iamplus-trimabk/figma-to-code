import { AppSidebar } from "@/shadcn/components/app-sidebar"
import { SiteHeader } from "@/shadcn/components/site-header"
import { SidebarProvider, SidebarInset } from "@/shadcn/components/ui/sidebar"

export default function App() {
  return (
    <SidebarProvider>
      <div className="flex h-screen w-full">
        <AppSidebar />
        <SidebarInset className="flex-1">
          <SiteHeader />
          <main className="flex-1 overflow-auto p-6">
            <div className="space-y-6">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                <p className="text-muted-foreground">
                  Welcome to your ShadCN Dashboard-01 setup
                </p>
              </div>

              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                <div className="rounded-xl border bg-card text-card-foreground shadow">
                  <div className="p-6">
                    <h3 className="font-semibold">Total Revenue</h3>
                    <p className="text-2xl font-bold">$45,231.89</p>
                    <p className="text-xs text-muted-foreground">+20.1% from last month</p>
                  </div>
                </div>

                <div className="rounded-xl border bg-card text-card-foreground shadow">
                  <div className="p-6">
                    <h3 className="font-semibold">Subscriptions</h3>
                    <p className="text-2xl font-bold">+2350</p>
                    <p className="text-xs text-muted-foreground">+180.1% from last month</p>
                  </div>
                </div>

                <div className="rounded-xl border bg-card text-card-foreground shadow">
                  <div className="p-6">
                    <h3 className="font-semibold">Sales</h3>
                    <p className="text-2xl font-bold">+12,234</p>
                    <p className="text-xs text-muted-foreground">+19% from last month</p>
                  </div>
                </div>

                <div className="rounded-xl border bg-card text-card-foreground shadow">
                  <div className="p-6">
                    <h3 className="font-semibold">Active Now</h3>
                    <p className="text-2xl font-bold">+573</p>
                    <p className="text-xs text-muted-foreground">+201 since last hour</p>
                  </div>
                </div>
              </div>

              <div className="rounded-xl border bg-card text-card-foreground shadow">
                <div className="p-6">
                  <h3 className="font-semibold mb-4">Recent Activity</h3>
                  <p className="text-muted-foreground">
                    Your dashboard is now running with ShadCN components!
                  </p>
                </div>
              </div>
            </div>
          </main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  )
}