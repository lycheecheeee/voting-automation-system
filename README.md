# 🚀 Voting Automation System - NVIDIA AI Powered

## ✨ Features

- ✅ Automated news fetching from Google News
- ✅ AI-powered topic generation (with fallback)
- ✅ NVIDIA Stable Diffusion 3 image generation
- ✅ One-click complete workflow
- ✅ Mobile responsive design
- ✅ Login protection (lychee / lycheechee2026)

## 🎯 Quick Start

### Local Development
\\\ash
cd C:\voting-automation
C:\Users\lyche\AppData\Local\Python\bin\python.exe app.py
\\\

Visit: http://localhost:5000/auto-generate

### Deploy to Vercel

1. Install Vercel CLI:
\\\ash
npm i -g vercel
\\\

2. Deploy:
\\\ash
vercel --prod
\\\

3. Set environment variables in Vercel dashboard:
   - NVIDIA_API_KEY
   - DMXAPI_API_KEY
   - ADMIN_USERNAME=lychee
   - ADMIN_PASSWORD=lycheechee2026

## 📁 Project Structure

\\\
voting-automation/
├── app.py                      # Flask main application
├── news_fetcher.py             # News fetching module
├── ai_topic_generator.py       # AI topic generator
├── auto_voting_workflow.py     # Automation workflow
├── nvidia_image_generator.py   # NVIDIA image generation
├── templates/
│   ├── index.html              # Main page
│   ├── nvidia_gen.html         # NVIDIA gen page
│   └── auto_generate.html      # Auto-gen page
├── .env                        # Environment variables (gitignored)
├── requirements.txt            # Python dependencies
└── vercel.json                 # Vercel configuration
\\\

## 🔑 API Keys

All API keys are stored in \.env\ file (not committed to Git).

## 🏆 User Lie-Down Index: 🛋️🛋️🛋️🛋️🛋️ 5/5

Users can fully relax - the system handles everything automatically!
