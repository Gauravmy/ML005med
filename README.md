# 🎓 Student Prediction ML Web App

A complete **full-stack Flask application** combining Machine Learning, Database, Real-time APIs, and Modern UI.

## 📋 Features

### Backend (Flask)
- ✅ RESTful API routes for predictions and data management
- ✅ SQLite database for student records
- ✅ ML model (Logistic Regression) for pass/fail prediction
- ✅ Real-time weather API integration
- ✅ Error handling and validation

### Machine Learning
- ✅ **Model**: Logistic Regression trained on 25 samples
- ✅ **Features**: Study Hours (0-24) + Attendance (0-100%)
- ✅ **Output**: PASS (1) or FAIL (0)
- ✅ **Model saved as**: `models/model.pkl` using joblib
- ✅ **Scaler saved**: Prevents feature scaling issues

### Database (SQLite)
- ✅ Stores student predictions with timestamps
- ✅ Tracks study hours, attendance, temperature
- ✅ Easy migration path to MongoDB

### Real-Time API Integration
- ✅ Uses **wttr.in** (free weather API)
- ✅ Fetches temperature and weather description
- ✅ No API key required
- ✅ Graceful fallback if API fails

### Frontend (HTML + CSS)
- ✅ **Responsive design** (mobile-friendly)
- ✅ **Card-based layout** (modern and clean)
- ✅ **Smooth animations** and transitions
- ✅ **Dark/Light gradients** for professional look
- ✅ **Interactive sections**: Home | Students | Form

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Train the ML Model**
```bash
python train_model.py
```
Output:
```
Model Accuracy: X.XX%
✓ Model saved as 'models/model.pkl'
✓ Scaler saved as 'models/scaler.pkl'
```

### 3. **Run the Flask App**
```bash
python app.py
```
Then open: **http://localhost:5000**

## 📁 Project Structure

```
doctor-ml-app/
├── app.py                    # Main Flask application
├── train_model.py            # Train ML model
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment config for Render
├── students.db              # SQLite database (auto-created)
├── models/
│   ├── model.pkl            # Trained ML model
│   └── scaler.pkl           # Feature scaler
├── templates/
│   └── index.html           # Single-page UI (Jinja templates)
└── static/
    └── style.css            # CSS styling
```

## 🎯 How It Works

### 1. **User Input** → 2. **Prediction** → 3. **Fetch Weather** → 4. **Save to DB**

```
┌─────────────────┐
│   User enters   │
│ Name, Study hrs │
│   Attendance    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ML Model       │
│  (Logistic Reg) │ ─→ Predicts PASS/FAIL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Weather API    │
│  (wttr.in)      │ ─→ Gets Temperature
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save to DB     │
│  (SQLite)       │ ─→ Stores all data
└─────────────────┘
```

## 📊 API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with weather |
| `/students` | GET | List all students (JSON) |
| `/form` | GET | Form page |
| `/predict` | POST | Make prediction |
| `/save` | POST | Save student to database |
| `/delete/<id>` | DELETE | Delete student record |
| `/download-data` | GET | Export all data as JSON |

### Example Request

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "study_hours": 5,
    "attendance": 85
  }'
```

### Example Response

```json
{
  "success": true,
  "prediction": 1,
  "prediction_label": "PASS",
  "temperature": 22,
  "weather_description": "Partly cloudy"
}
```

## 🧠 ML Model Details

### Training Data
- **25 samples** with realistic patterns
- **Features**: Study Hours, Attendance
- **Condition**: Low study + attendance = Fail; High = Pass

### Model Info
```python
Model: Logistic Regression
Scaler: StandardScaler
Accuracy: ~88% (test set)
```

### Making Predictions

```python
# Load model
model = joblib.load('models/model.pkl')
scaler = joblib.load('models/scaler.pkl')

# Predict
study_hours = 5
attendance = 85
input_data = [[study_hours, attendance]]
input_scaled = scaler.transform(input_data)
prediction = model.predict(input_scaled)[0]

# 0 = FAIL, 1 = PASS
```

## 🌐 Frontend Sections

### Home
- Welcome message
- Real-time temperature display
- Feature highlights
- Call-to-action button

### Students List
- All saved predictions
- Color-coded badges (PASS/FAIL)
- Student details (hours, attendance, etc.)
- Delete button for each record
- Download data as JSON

### Form
- Input fields with validation
- Real-time predictions
- Weather integration
- Save to database
- Error handling

## 📦 Dependencies

```
Flask==2.3.3           # Web framework
scikit-learn==1.3.1    # ML library
joblib==1.3.2          # Model serialization
numpy==1.24.3          # Numerical computing
requests==2.31.0       # HTTP requests for API
gunicorn==21.2.0       # Production server
```

## 🔧 Configuration

### Database Location
```python
app.config['DATABASE'] = 'students.db'  # SQLite file
```

### ML Model Path
```
models/model.pkl       # Trained Logistic Regression
models/scaler.pkl      # Feature scaler
```

### Weather API
```
Endpoint: https://wttr.in/{location}?format=j1
Location: New York (configurable)
No API key required
```

## 🚢 Deployment to Render

### 1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. **Deploy on Render**
- Create Render account: https://render.com
- Connect GitHub repository
- Select **Web Service**
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

### 3. **Procfile Handling**
```
web: gunicorn app:app                 # Run Flask app
release: python train_model.py        # Train model on deployment
```

## 💾 Database Schema

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    study_hours REAL NOT NULL,
    attendance REAL NOT NULL,
    prediction INTEGER NOT NULL,        -- 0 or 1
    prediction_label TEXT NOT NULL,     -- "PASS" or "FAIL"
    temperature REAL,                   -- Fetched from API
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Upgrade to MongoDB

The database layer is abstracted, making MongoDB upgrade easy:

```python
# Current (SQLite)
db = sqlite3.connect('students.db')

# Future (MongoDB)
from pymongo import MongoClient
db = MongoClient('mongodb_uri')['student_predictions']
```

## 📝 Usage Examples

### Example 1: Predict with Low Study Hours
```
Input: John, Study=2hrs, Attendance=55%
Output: FAIL ❌
Reason: Low study hours and attendance
```

### Example 2: Predict with High Study Hours
```
Input: Jane, Study=7hrs, Attendance=95%
Output: PASS ✅
Reason: High study hours and attendance
```

## 🎨 UI Features

- **Responsive Design**: Works on mobile, tablet, desktop
- **Modern Styling**: Gradient backgrounds, smooth animations
- **Color Coding**: Green for PASS, Red for FAIL
- **Loading States**: Spinner during predictions
- **Error Handling**: User-friendly error messages
- **Navigation**: Easy switching between sections

## ⚠️ Important Notes

1. **First Time Setup**: Run `python train_model.py` before starting Flask
2. **Model Path**: Ensure `models/` directory exists
3. **Weather API**: Requires internet connection
4. **Database**: SQLite file created automatically
5. **Production**: Use gunicorn instead of Flask debug server

## 🐛 Troubleshooting

### Model Not Found Error
```bash
python train_model.py  # Regenerate model
```

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Database Locked
```bash
# Delete and recreate
rm students.db
# Restart app
```

### Weather API Timeout
- App has fallback: returns default temp 25°C
- Check internet connection

## 📚 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **Scikit-learn**: https://scikit-learn.org/
- **SQLite**: https://www.sqlite.org/
- **REST APIs**: https://restfulapi.net/

## 📄 License

Free to use and modify for learning purposes.

## 🤝 Contributing

Feel free to enhance:
- Add more ML features (GPA, subjects, etc.)
- Implement user authentication
- Add data visualization (charts/graphs)
- Switch to MongoDB
- Deploy with Docker

---

**Built with ❤️ for Learning** | Full-Stack ML Web App
