import { LucideIcon } from 'lucide-react'

export interface NavItem {
  name: string
  href: string
  icon: LucideIcon
  badge?: string
  items?: NavItem[]
}

export interface NavigationConfig {
  main: NavItem[]
  admin: NavItem[]
  footer?: NavItem[]
}

export const defaultNavigationConfig: NavigationConfig = {
  main: [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: require('lucide-react').LayoutDashboard,
    },
    {
      name: 'Analytics',
      href: '/analytics',
      icon: require('lucide-react').BarChart3,
    },
    {
      name: 'Projects',
      href: '/projects',
      icon: require('lucide-react').FolderKanban,
    },
    {
      name: 'Team',
      href: '/team',
      icon: require('lucide-react').Users,
    },
    {
      name: 'Settings',
      href: '/settings',
      icon: require('lucide-react').Settings,
    },
  ],
  admin: [
    {
      name: 'User Management',
      href: '/admin/users',
      icon: require('lucide-react').Users,
    },
    {
      name: 'System Settings',
      href: '/admin/system',
      icon: require('lucide-react').Settings,
    },
    {
      name: 'Audit Logs',
      href: '/admin/audit',
      icon: require('lucide-react').FileText,
    },
  ],
  footer: [
    {
      name: 'Documentation',
      href: '/docs',
      icon: require('lucide-react').BookOpen,
    },
    {
      name: 'Support',
      href: '/support',
      icon: require('lucide-react').HelpCircle,
    },
  ],
}