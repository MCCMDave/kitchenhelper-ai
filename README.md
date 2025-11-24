# KitchenHelper-AI

AI-powered recipe generator that creates personalized recipes based on your available ingredients. Special support for diabetes with carb unit (KE/BE) calculations.

## Features

- **AI Recipe Generation** - Generate recipes from your ingredients (Mock AI for demo)
- **Ingredient Management** - Track your ingredients with categories and expiry dates
- **Favorites System** - Save your favorite recipes with PDF export
- **Diet Profiles** - Support for multiple diet profiles:
  - Diabetic (with KE/BE calculations)
  - Vegan / Vegetarian
  - Gluten-free / Lactose-free
  - Keto / Low-Carb / High-Protein
- **Multi-Language** - English and German (toggle in header)
- **Dark Mode** - Toggle light/dark theme
- **Responsive Design** - Works on desktop and mobile

## Quick Start (For Testers)

### Prerequisites

- **Python 3.10+** installed
- **Git** installed
- A web browser (Chrome, Firefox, Edge)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/kitchenhelper-ai.git
   cd kitchenhelper-ai
   ```

2. **Set up the backend**
   ```bash
   cd backend

   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1

   # Windows Git Bash:
   source venv/Scripts/activate

   # macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Initialize the database with test users**
   ```bash
   # Still in backend folder with venv activated
   python scripts/db_manager.py reset
   ```

4. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at: http://127.0.0.1:8000

   Swagger docs: http://127.0.0.1:8000/docs

5. **Open the frontend**

   Simply open `frontend/index.html` in your browser.

   Or use VS Code with the "Live Server" extension.

### Test Users

After running `db_manager.py reset`, these test users are available:

| Email | Username | Password |
|-------|----------|----------|
| a@a.a | aaa | aaaaaa |
| b@b.b | bbb | bbbbbb |
| test@test.de | testuser | test123 |

Login with either email OR username.

## Project Structure

```
kitchenhelper-ai/
├── backend/
│   ├── app/
│   │   ├── models/        # SQLAlchemy Models
│   │   ├── routes/        # API Endpoints
│   │   ├── schemas/       # Pydantic Schemas
│   │   ├── services/      # Business Logic (PDF, Recipe Gen)
│   │   └── utils/         # Helpers (auth, database, jwt)
│   ├── database/          # SQLite Database
│   ├── scripts/           # Utility Scripts
│   │   ├── db_manager.py  # Database management
│   │   └── test_login.py  # Login test script
│   └── requirements.txt
├── frontend/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript Modules
│   ├── index.html         # Login/Register Page
│   └── dashboard.html     # Main Application
├── docs/                  # Documentation
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login (email or username)
- `POST /api/auth/request-password-reset` - Request reset token
- `POST /api/auth/reset-password` - Reset password with token

### User
- `GET /api/users/me` - Get current user info
- `PUT /api/users/me` - Update profile (username, email, emoji, password)
- `DELETE /api/users/me` - Delete account

### Ingredients
- `GET /api/ingredients` - List all ingredients
- `POST /api/ingredients` - Add ingredient
- `PUT /api/ingredients/{id}` - Update ingredient
- `DELETE /api/ingredients/{id}` - Delete ingredient

### Recipes
- `POST /api/recipes/generate` - Generate recipes from ingredients
- `GET /api/recipes/history` - Get recipe history
- `GET /api/recipes/{id}` - Get single recipe
- `GET /api/recipes/{id}/export/pdf` - Export recipe as PDF

### Favorites
- `GET /api/favorites` - List favorites
- `POST /api/favorites` - Add favorite
- `DELETE /api/favorites/{id}` - Remove favorite

### Diet Profiles
- `GET /api/profiles` - List profiles
- `POST /api/profiles` - Create profile
- `PUT /api/profiles/{id}` - Update profile
- `DELETE /api/profiles/{id}` - Delete profile

## Testing the App

### Basic Flow

1. **Register** a new account or login with test user
2. **Add ingredients** in the Ingredients tab
3. **Generate recipes** in the Recipes tab
   - Select ingredients
   - Click "Generate Recipes"
4. **Favorite** recipes you like (star button)
5. **View favorites** - click to open details modal
6. **Export PDF** - download recipe as PDF

### Features to Test

- [ ] User registration with username + emoji
- [ ] Login with email OR username
- [ ] Password reset flow
- [ ] Add/edit/delete ingredients
- [ ] Filter ingredients by category
- [ ] Generate recipes (Mock AI)
- [ ] Add/remove favorites
- [ ] View favorite details in modal
- [ ] Export recipe as PDF
- [ ] Create diet profiles (Diabetic, Vegan, etc.)
- [ ] Multiple active profiles
- [ ] Language toggle (EN/DE)
- [ ] Dark/Light mode toggle
- [ ] Responsive design (resize browser)
- [ ] User menu dropdown (Settings, Profiles, Logout)

## Troubleshooting

### Backend won't start
```bash
# Make sure venv is activated
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux

# Check all dependencies installed
pip install -r requirements.txt

# Check port 8000 is free
```

### Database errors
```bash
# Reset database completely
python scripts/db_manager.py reset
```

### Frontend can't connect
- Make sure backend is running on http://127.0.0.1:8000
- Check browser console for errors
- Check CORS settings in backend

### PDF Export not working
```bash
# Make sure reportlab is installed
pip install reportlab==4.0.7
# Restart backend after installing
```

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Auth**: JWT Bearer Tokens
- **PDF**: ReportLab
- **Deployment**: Docker (x86_64 & ARM64)

---

## Docker Setup

### Development (Windows)

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Copy environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
3. Edit `.env` and change `JWT_SECRET_KEY`
4. Start container:
   ```powershell
   docker compose up -d
   ```
5. Visit: http://localhost:8000

**Or use the helper script:**
```powershell
.\dev-start.ps1 -Docker    # Start in Docker
.\dev-start.ps1            # Start local dev server
.\dev-start.ps1 -Help      # Show all options
```

### Production (Raspberry Pi)

See: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### Docker Commands

```bash
docker compose build       # Build image
docker compose up -d       # Start container
docker compose down        # Stop container
docker compose logs -f     # View logs
```

Full documentation: [docs/DOCKER-SETUP.md](docs/DOCKER-SETUP.md)

## Subscription Tiers (Demo)

| Tier | Recipes/Day | Favorites |
|------|-------------|-----------|
| Demo | 3 | 5 |
| Basic | 50 | 50 |
| Premium | Unlimited | Unlimited |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and demonstration purposes.

---

**Questions?** Open an issue on GitHub!
