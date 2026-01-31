# Luxury Furniture Studio

A premium furniture e-commerce application with interactive 3D visualization and AI-powered design assistance. Deploy in minutes, no local setup required.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fquantnexusai%2Fluxury-furniture-app&env=NEXT_PUBLIC_SUPABASE_URL,NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY,ANTHROPIC_API_KEY&envDescription=Get%20keys%20from%20Supabase%20and%20Anthropic&envLink=https%3A%2F%2Fgithub.com%2Fquantnexusai%2Fluxury-furniture-app%23environment-variables&project-name=luxury-furniture-studio&repository-name=luxury-furniture-app)

## Features

- **Collection Gallery** - Browse curated luxury furniture with filtering and search
- **3D Configurator** - Interactive Three.js visualization with material customization
- **Claude AI Assistant** - AI-powered design recommendations and consultation
- **Custom Design Service** - Request bespoke furniture creation
- **Material Customization** - Explore different materials, finishes, and colors
- **Design Consultation** - Schedule sessions with senior designers

## Quick Start

### Step 1: Get Your API Keys

Before deploying, you'll need:

1. **Supabase** - Create a free project at [supabase.com](https://supabase.com)
2. **Anthropic** - Get an API key at [console.anthropic.com](https://console.anthropic.com)

### Step 2: Deploy to Vercel

Click the deploy button above and enter your API keys when prompted.

### Step 3: Set Up Database

Run `supabase/schema.sql` in your Supabase SQL Editor to create tables and seed data.

### Step 4: Done!

Your luxury furniture studio is now live.

## Environment Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Supabase > Settings > API |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | Supabase anon key | Supabase > Settings > API |
| `ANTHROPIC_API_KEY` | Claude API key | console.anthropic.com |

## Local Development

For local UI development without API keys, the app includes sample data:

- Sample furniture catalog displayed throughout
- Simulated Claude AI responses
- Full UI functionality for testing

```bash
cd frontend/frontend
npm install
npm run dev
```

**Note:** Local preview is for development only. Deployment requires valid API keys.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed setup instructions.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js 14 (App Router) |
| Styling | Tailwind CSS |
| 3D Graphics | Three.js, React Three Fiber |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| AI | Claude API |
| Hosting | Vercel |

## Project Structure

```
luxury-furniture-app/
├── frontend/frontend/     # Next.js application
│   ├── app/               # App Router pages
│   ├── src/               # Components & utilities
│   └── public/            # Static assets
├── supabase/
│   └── schema.sql         # Database schema with seed data
├── assets/                # Furniture images
└── data/                  # Sample data (JSON)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development and contribution guidelines.

## Need Help?

For assistance with deployment, configuration, or customization (MCP servers, AI agents, etc.), contact us at **ari@quantnexus.ai**

## License

MIT License - use freely for personal or commercial projects.
