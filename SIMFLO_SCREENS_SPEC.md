# SimFlo Screens/Pages Specification V1.0

## 🎯 Purpose
Defines the structure and behavior of complete screens/pages in the SimFlo format.

## 📋 Screen Structure

### Basic Screen Definition
```json
{
  "screens": {
    "ScreenName": {
      "type": "screen",
      "platform": "mobile | desktop | responsive",
      "layout": {
        "type": "auto-layout | stack | grid",
        "direction": "column | row",
        "width": "100%",
        "height": "100vh",
        "padding": "token-reference",
        "margin": "token-reference",
        "gap": "token-reference",
        "justifyContent": "flex-start | center | flex-end | space-between",
        "alignItems": "flex-start | center | flex-end | stretch",
        "overflow": "visible | hidden | scroll | auto"
      },
      "styles": {
        "backgroundColor": "token-reference",
        "backgroundImage": "image-url",
        "backgroundSize": "cover | contain | auto",
        "backgroundPosition": "center | top | bottom | left | right",
        "opacity": "0-1"
      },
      "children": [
        {
          "type": "component | container | text | image",
          "name": "ComponentName",
          "variant": "variant-name",
          "layout": {
            "component-specific-layout"
          },
          "properties": {
            "component-properties"
          },
          "children": []
        }
      ],
      "responsive": {
        "mobile": {
          "layout": { /* mobile-specific layout */ },
          "styles": { /* mobile-specific styles */ }
        },
        "tablet": {
          "layout": { /* tablet-specific layout */ },
          "styles": { /* tablet-specific styles */ }
        },
        "desktop": {
          "layout": { /* desktop-specific layout */ },
          "styles": { /* desktop-specific styles */ }
        }
      }
    }
  }
}
```

## 🏗️ Layout Patterns

### 1. Full Screen Layout
```json
{
  "Login": {
    "type": "screen",
    "platform": "responsive",
    "layout": {
      "type": "auto-layout",
      "direction": "column",
      "width": "100%",
      "height": "100vh",
      "justifyContent": "center",
      "alignItems": "center",
      "padding": "spacing.6"
    },
    "styles": {
      "backgroundColor": "colors.background.secondary"
    },
    "children": [
      {
        "type": "component",
        "name": "Card",
        "variant": "elevated",
        "layout": {
          "width": "90%",
          "maxWidth": "400px"
        },
        "content": {
          "type": "container",
          "children": [
            {
              "type": "text",
              "properties": {
                "value": "Welcome Back",
                "fontSize": "fontSize.3xl",
                "fontWeight": "fontWeight.bold",
                "align": "center",
                "marginBottom": "spacing.6"
              }
            },
            {
              "type": "component",
              "name": "Input",
              "properties": {
                "placeholder": "Email address",
                "marginBottom": "spacing.4"
              }
            },
            {
              "type": "component",
              "name": "Input",
              "properties": {
                "placeholder": "Password",
                "type": "password",
                "marginBottom": "spacing.6"
              }
            },
            {
              "type": "component",
              "name": "Button",
              "variant": "primary",
              "properties": {
                "value": "Sign In",
                "width": "100%"
              }
            }
          ]
        }
      }
    ]
  }
}
```

### 2. Navigation Layout
```json
{
  "Home": {
    "type": "screen",
    "platform": "mobile",
    "layout": {
      "type": "auto-layout",
      "direction": "column",
      "width": "100%",
      "height": "100vh",
      "overflow": "hidden"
    },
    "styles": {
      "backgroundColor": "colors.background.primary"
    },
    "children": [
      {
        "type": "component",
        "name": "Header",
        "layout": {
          "width": "100%",
          "height": "64px",
          "padding": "spacing.4"
        },
        "content": {
          "type": "container",
          "children": [
            {
              "type": "text",
              "properties": {
                "value": "App Title",
                "fontSize": "fontSize.lg",
                "fontWeight": "fontWeight.semibold"
              }
            },
            {
              "type": "component",
              "name": "Button",
              "variant": "ghost",
              "properties": {
                "value": "Menu"
              }
            }
          ]
        }
      },
      {
        "type": "component",
        "name": "Container",
        "layout": {
          "flex": 1,
          "overflow": "scroll",
          "padding": "spacing.4"
        },
        "content": {
          "type": "container",
          "children": [
            /* Main content area */
          ]
        }
      },
      {
        "type": "component",
        "name": "BottomNav",
        "layout": {
          "width": "100%",
          "height": "80px"
        },
        "content": {
          "type": "container",
          "children": [
            /* Navigation items */
          ]
        }
      }
    ]
  }
}
```

### 3. List/Grid Layout
```json
{
  "ProductList": {
    "type": "screen",
    "platform": "responsive",
    "layout": {
      "type": "auto-layout",
      "direction": "column",
      "width": "100%",
      "height": "100vh",
      "padding": "spacing.4"
    },
    "styles": {
      "backgroundColor": "colors.background.secondary"
    },
    "children": [
      {
        "type": "component",
        "name": "Container",
        "layout": {
          "width": "100%",
          "marginBottom": "spacing.6"
        },
        "content": {
          "type": "container",
          "children": [
            {
              "type": "text",
              "properties": {
                "value": "Products",
                "fontSize": "fontSize.2xl",
                "fontWeight": "fontWeight.bold"
              }
            },
            {
              "type": "component",
              "name": "Input",
              "properties": {
                "placeholder": "Search products...",
                "marginTop": "spacing.4"
              }
            }
          ]
        }
      },
      {
        "type": "component",
        "name": "Grid",
        "layout": {
          "columns": "2",
          "gap": "spacing.4",
          "flex": 1,
          "overflow": "scroll"
        },
        "content": {
          "type": "container",
          "children": [
            {
              "type": "component",
              "name": "ProductCard",
              "variant": "default"
            },
            {
              "type": "component",
              "name": "ProductCard",
              "variant": "default"
            }
            /* More product cards */
          ]
        }
      }
    ],
    "responsive": {
      "tablet": {
        "children": [
          {
            "type": "component",
            "name": "Grid",
            "layout": {
              "columns": "3"
            }
          }
        ]
      },
      "desktop": {
        "children": [
          {
            "type": "component",
            "name": "Grid",
            "layout": {
              "columns": "4"
            }
          }
        ]
      }
    }
  }
}
```

## 📱 Screen Types

### 1. Login/Authentication Screens
**Purpose**: User authentication and account management
**Common Patterns**:
- Centered form card
- Full background with form overlay
- Social login options
- Input fields for credentials
- Action buttons

### 2. Home/Dashboard Screens
**Purpose**: Main application interface
**Common Patterns**:
- Header with navigation
- Main content area
- Sidebar or bottom navigation
- Cards or widgets for information
- User profile section

### 3. List/Collection Screens
**Purpose**: Display collections of items
**Common Patterns**:
- Search/filter functionality
- Grid or list layout
- Pagination or infinite scroll
- Item cards with preview
- Sorting options

### 4. Detail/View Screens
**Purpose**: Detailed view of single item
**Common Patterns**:
- Header with back navigation
- Large image or media
- Detailed information sections
- Action buttons
- Related items

### 5. Form/Creation Screens
**Purpose**: User input for creating/editing content
**Common Patterns**:
- Form fields and inputs
- Validation indicators
- Save/cancel actions
- Multi-step forms
- Preview section

### 6. Settings/Profile Screens
**Purpose**: User preferences and account management
**Common Patterns**:
- User avatar and info
- Toggle switches
- Selection lists
- Logout/action buttons
- Account management options

## 🎨 Screen Composition Patterns

### 1. Header + Main + Footer
```json
{
  "layout": {
    "type": "auto-layout",
    "direction": "column",
    "height": "100vh"
  },
  "children": [
    {
      "type": "component",
      "name": "Header",
      "layout": { "height": "64px" }
    },
    {
      "type": "component",
      "name": "MainContent",
      "layout": { "flex": 1 }
    },
    {
      "type": "component",
      "name": "Footer",
      "layout": { "height": "80px" }
    }
  ]
}
```

### 2. Sidebar + Content
```json
{
  "layout": {
    "type": "auto-layout",
    "direction": "row",
    "height": "100vh"
  },
  "children": [
    {
      "type": "component",
      "name": "Sidebar",
      "layout": { "width": "240px" }
    },
    {
      "type": "component",
      "name": "MainContent",
      "layout": { "flex": 1 }
    }
  ],
  "responsive": {
    "mobile": {
      "layout": {
        "direction": "column"
      },
      "children": [
        {
          "type": "component",
          "name": "Sidebar",
          "layout": { "height": "60px" }
        }
      ]
    }
  }
}
```

### 3. Overlay/Modal Screen
```json
{
  "layout": {
    "type": "auto-layout",
    "width": "100%",
    "height": "100vh",
    "justifyContent": "center",
    "alignItems": "center"
  },
  "styles": {
    "backgroundColor": "colors.background.overlay"
  },
  "children": [
    {
      "type": "component",
      "name": "Modal",
      "layout": {
        "width": "90%",
        "maxWidth": "500px",
        "maxHeight": "80vh"
      }
    }
  ]
}
```

## 🔄 Responsive Design

### Breakpoint Strategy
- **Mobile**: 320px - 768px (portrait phones)
- **Tablet**: 768px - 1024px (tablets, landscape phones)
- **Desktop**: 1024px+ (desktop monitors)

### Responsive Patterns
```json
{
  "responsive": {
    "mobile": {
      "layout": {
        "direction": "column",
        "padding": "spacing.4"
      },
      "children": [
        /* Mobile-specific children */
      ]
    },
    "tablet": {
      "layout": {
        "direction": "row",
        "padding": "spacing.6"
      },
      "children": [
        /* Tablet-specific children */
      ]
    },
    "desktop": {
      "layout": {
        "direction": "row",
        "padding": "spacing.8",
        "maxWidth": "1200px",
        "margin": "0 auto"
      },
      "children": [
        /* Desktop-specific children */
      ]
    }
  }
}
```

## 🎯 Screen Best Practices

### 1. Layout Consistency
- Use consistent spacing and padding
- Maintain visual hierarchy
- Follow platform conventions
- Ensure proper touch targets

### 2. Content Organization
- Group related items together
- Use clear visual separation
- Maintain logical flow
- Consider content priority

### 3. Responsive Behavior
- Mobile-first design approach
- Progressive enhancement for larger screens
- Maintain functionality across all sizes
- Optimize for each platform

### 4. Performance Considerations
- Limit nested components
- Use efficient layout patterns
- Consider content loading strategies
- Optimize for different devices

## 📋 Screen Metadata

### Screen Properties
```json
{
  "ScreenName": {
    "type": "screen",
    "platform": "mobile | desktop | responsive",
    "metadata": {
      "title": "Screen Title",
      "description": "Screen description",
      "tags": ["login", "authentication"],
      "author": "Designer Name",
      "version": "1.0.0",
      "status": "draft | ready | deprecated"
    },
    "navigation": {
      "canGoBack": true,
      "nextScreen": "HomeScreen",
      "parentScreen": "WelcomeScreen"
    },
    "accessibility": {
      "screenReaderLabel": "Login form screen",
      "focusOrder": ["email-input", "password-input", "login-button"]
    }
  }
}
```

---

*This spec provides a comprehensive screen system that can represent complete user interfaces while maintaining consistency and responsive behavior across all platforms.*