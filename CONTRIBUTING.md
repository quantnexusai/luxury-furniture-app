# Contributing to Luxury Furniture Studio

Thank you for your interest in contributing! This guide will help you get set up for local development.

## Local Development

### Prerequisites

- Node.js 18+
- npm or yarn
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/quantnexusai/luxury-furniture-app.git
   cd luxury-furniture-app
   ```

2. **Install dependencies**
   ```bash
   cd frontend/frontend
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   The app will be available at http://localhost:3000

### Local Preview Mode

The app includes sample data for local development. Without API keys configured, you'll see:
- Sample furniture catalog with demo data
- Simulated Claude AI responses
- Full UI functionality for testing

This allows you to explore and develop the UI without setting up external services.

### Running with Real Services

To connect to real services:

1. Copy `.env.example` to `.env.local`
2. Add your Supabase and Anthropic API keys
3. Run the Supabase schema (`supabase/schema.sql`) in your Supabase SQL Editor
4. Restart the development server

## Code Style

- **TypeScript** - Use proper types, avoid `any`
- **Tailwind CSS** - Use utility classes, follow existing patterns
- **Components** - Keep components focused and reusable
- **File naming** - Use kebab-case for files, PascalCase for components

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test locally (both with and without API keys)
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

### PR Guidelines

- Keep PRs focused on a single feature or fix
- Include a clear description of changes
- Add screenshots for UI changes
- Ensure no TypeScript errors (`npm run build`)

## Project Structure

```
luxury-furniture-app/
├── frontend/frontend/          # Next.js application
│   ├── app/                    # App Router pages
│   ├── src/
│   │   ├── components/         # React components
│   │   └── lib/                # Utilities and types
│   └── public/                 # Static assets
├── supabase/
│   └── schema.sql              # Database schema
├── assets/                     # Furniture images
└── data/                       # Sample data
```

## Need Help?

- Open an issue for bugs or feature requests
- Contact: ari@quantnexus.ai

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
