# 🗣️ Talk2db.ai

**Learn SQL by asking questions in plain English!**

An interactive educational platform that converts natural language queries into SQL statements, helping students understand database concepts through hands-on learning.

## ✨ Features

- 💬 **Natural Language to SQL**: Ask questions in plain English
- 📚 **Educational Focus**: Learn SQL concepts through interactive examples
- 📊 **Database Schema Viewer**: Explore table structures and relationships
- 📝 **Query History**: Track your learning progress
- 🎓 **Teaching Tool**: Perfect for SQL courses and database education

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL
- OpenAI API Key

### Local Development

#### Backend

```bash
cd backend
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and OpenAI API key

# Run the server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your backend URL

# Run the development server
npm start
```

## 📦 Project Structure

```
Talk2DB/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py   # Main application
│   │   ├── core/     # Database configuration
│   │   ├── models/   # Database models
│   │   ├── services/ # Business logic
│   │   └── utils/    # Utilities
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── App.js       # Main app component
│   └── package.json
└── DEPLOYMENT_GUIDE.md  # Deployment instructions
```

## 🌐 Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for complete deployment instructions on Render.

### Quick Deploy Steps

1. Push code to GitHub
2. Create PostgreSQL database on Render
3. Deploy backend service
4. Deploy frontend static site
5. Set environment variables
6. Initialize database

## 🛠️ Technologies

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, OpenAI API
- **Frontend**: React.js, Axios
- **Deployment**: Render

## 📝 Environment Variables

### Backend

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `FRONTEND_URL`: Frontend URL for CORS
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins

### Frontend

- `REACT_APP_API_URL`: Backend API URL

## 📚 API Documentation

Once deployed, visit `/docs` on your backend URL for interactive API documentation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For deployment help, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

---

Made with ❤️ for SQL learners everywhere!
