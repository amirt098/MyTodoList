# My Todo List - Frontend

Modern React frontend for the My Todo List application, built with mobile-first responsive design.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS framework (mobile-first)
- **React Router** - Client-side routing
- **Zustand** - Lightweight state management
- **TanStack Query** - Server state management
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **date-fns** - Date formatting

## Features

- 📱 **Mobile-First Design** - Optimized for mobile devices, responsive for desktop
- 🎨 **Modern UI** - Clean, beautiful interface with Tailwind CSS
- 🔐 **Authentication** - Login and registration
- ✅ **Todo Management** - Create, update, delete todos
- 📋 **Kanban Board** - Visual task management
- 👥 **Projects** - Project management and collaboration
- 🤖 **AI Features** - Smart todo creation with AI assistance
- 📊 **Dashboard** - Overview of todos and statistics

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── layout/      # Layout components (Header, Sidebar, etc.)
│   │   ├── todos/       # Todo-related components
│   │   └── ui/          # Basic UI components (Button, Card, etc.)
│   ├── pages/           # Page components
│   │   ├── auth/        # Authentication pages
│   │   ├── dashboard/   # Dashboard page
│   │   ├── todos/       # Todo pages
│   │   ├── kanban/      # Kanban board page
│   │   ├── projects/    # Project pages
│   │   └── settings/    # Settings page
│   ├── services/        # API services
│   ├── store/           # Zustand stores
│   ├── types/           # TypeScript types
│   ├── utils/           # Utility functions
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── public/              # Static assets
└── package.json
```

## Mobile-First Design

The application is designed mobile-first with Tailwind CSS:

- **Base styles** target mobile devices (< 640px)
- **sm:** Small screens (≥ 640px)
- **md:** Medium screens (≥ 768px)
- **lg:** Large screens (≥ 1024px)
- **xl:** Extra large screens (≥ 1280px)

### Responsive Features

- **Mobile Navigation** - Bottom navigation bar on mobile
- **Desktop Sidebar** - Sidebar navigation on desktop
- **Responsive Grids** - Adapts from 1 column (mobile) to multiple columns (desktop)
- **Touch-Friendly** - Large touch targets for mobile users
- **Safe Areas** - Respects device safe areas (notches, etc.)

## API Integration

The frontend connects to the Django backend API. Make sure the backend is running on `http://localhost:8000`.

API endpoints are configured in `src/services/api.ts`.

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

