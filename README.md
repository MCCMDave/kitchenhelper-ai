# KitchenHelper-AI 🍳

AI-powered recipe generator that creates personalized recipes based on your available ingredients. Special support for diabetes with carb unit (KE/BE) calculations.

**English Version** | [Deutsche Version](docs/README.de.md)

## ✨ Features

- 🤖 **AI Recipe Generation** - Generate recipes from your ingredients
- 📦 **Ingredient Management** - Track ingredients with categories and expiry dates
- ⭐ **Favorites System** - Save favorite recipes with PDF export
- 🍽️ **Diet Profiles** - Support for Diabetic, Vegan, Keto, Gluten-free, and more
- 🌍 **Multi-Language** - English and German support
- 🌙 **Dark Mode** - Toggle light/dark theme
- 📱 **Responsive Design** - Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git
- A web browser

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/kitchenhelper-ai.git
cd kitchenhelper-ai

# Set up backend
cd backend
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with test users
python scripts/db_manager.py reset

# Start backend server
uvicorn app.main:app --reload
```

### Open Frontend
Simply open `frontend/index.html` in your browser or use VS Code Live Server.

The API will be available at: http://127.0.0.1:8000
Swagger docs: http://127.0.0.1:8000/docs

### Test Users

| Email | Username | Password |
|-------|----------|----------|
| a@a.a | aaa | aaaaaa |
| b@b.b | bbb | bbbbbb |
| test@test.de | testuser | test123 |

## 📁 Project Structure

```
kitchenhelper-ai/
├── docs/                   # Documentation
│   ├── README-full.md     # Full documentation
│   ├── README.de.md       # German documentation
│   ├── CLAUDE.md          # Claude AI integration notes
│   ├── ENCODING-RULES.md  # Encoding guidelines
│   ├── SHORTCUTS.md       # Development shortcuts
│   └── STATUS-REPORT.md   # Project status
├── scripts/               # Utility scripts
│   ├── dev-start.ps1     # Quick development start
│   ├── deploy.sh         # Deployment script
│   └── logs-view.ps1     # Log viewer
├── backend/               # FastAPI backend
├── frontend/              # Vanilla JS frontend
├── docker-compose.yml    # Docker setup
└── README.md             # This file
```

## 🛠️ Development Scripts

```powershell
# Quick start development server
.\scripts\dev-start.ps1

# View logs
.\scripts\logs-view.ps1

# Deploy to production
.\scripts\deploy.sh
```

## 🐳 Docker Deployment

```bash
# Build and start containers
docker-compose up -d

# Stop containers
docker-compose down
```

## 📚 Documentation

For complete documentation, API details, and development guides:
- [**Full Documentation (English)**](docs/README-full.md)
- [**Vollständige Dokumentation (Deutsch)**](docs/README.de.md)
- [**Development Shortcuts**](docs/SHORTCUTS.md)
- [**Project Status**](docs/STATUS-REPORT.md)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read the documentation for development guidelines.

---

**Built with FastAPI, SQLAlchemy, and Vanilla JavaScript**
