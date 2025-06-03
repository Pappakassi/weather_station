# 🌤️ Veðrið hjá Óla Bj.

A beautiful, modern weather station dashboard built with Django, featuring real-time data from a personal weather station and local forecasting.

![Weather Dashboard](https://img.shields.io/badge/Django-4.2.7-green) ![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## ✨ Features

- 🏠 **Personal Weather Station Integration** - Real-time data from IAKURE31 station
- 📊 **Beautiful Dark Dashboard** - Modern, responsive UI with Icelandic localization  
- 🌡️ **Comprehensive Metrics** - Temperature, humidity, wind speed, pressure, UV index
- 📈 **3-Day Local Forecast** - Reliable weather predictions
- 🗺️ **Interactive Map** - Station location with Leaflet integration
- 📱 **Mobile Responsive** - Perfect on all devices
- 🔒 **Production Ready** - Secure, scalable configuration

## 🎯 Live Features

### Current Weather Display
- Large temperature reading with gradient styling
- Weather conditions in Icelandic
- Wind speed in m/s (as preferred)
- Humidity, visibility, and pressure metrics
- UV index with visual gauge
- Sunrise/sunset times

### Forecasting
- 3-day weather forecast
- Realistic Iceland weather patterns
- Wind speed and precipitation data
- Beautiful card-based layout

### Interactive Elements
- Auto-refresh every 5 minutes
- Smooth animations and transitions
- Responsive sidebar navigation
- Weather station map with zoom controls

## 🚀 Quick Start

### Development Setup

1. **Clone and setup**
   ```bash
   git clone <your-repo-url>
   cd weather_station_v2
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment configuration**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

3. **Run development server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. **Open browser**
   ```
   http://127.0.0.1:8000
   ```

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions.

**Quick Heroku Deploy:**
```bash
# Generate secret key
python generate_secret_key.py

# Test production settings
python production_test.py

# Deploy to Heroku
heroku create your-weather-app
heroku config:set SECRET_KEY="your-generated-key"
heroku config:set DEBUG=False
git push heroku main
```

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, Custom CSS
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **APIs**: Weather.com Personal Station API
- **Deployment**: Heroku, Railway, DigitalOcean
- **Static Files**: Whitenoise
- **Maps**: Leaflet.js

## 📁 Project Structure

```
weather_station_v2/
├── weather_station/          # Django project settings
│   ├── settings.py          # Production-ready configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── weather/                  # Main weather app
│   ├── models.py            # Data models (future expansion)
│   ├── views.py             # View controllers
│   ├── services.py          # Weather API integration
│   └── urls.py              # App URL patterns
├── templates/               # HTML templates
│   ├── base.html            # Base template with navigation
│   └── weather/             # Weather-specific templates
├── static/                  # Static files (CSS, JS, images)
├── requirements.txt         # Python dependencies
├── Procfile                 # Heroku deployment
├── runtime.txt              # Python version
└── DEPLOYMENT.md            # Deployment guide
```

## 🌡️ Weather Data Sources

### Personal Station (Current Conditions)
- **Station ID**: IAKURE31
- **Location**: Akureyri, Iceland
- **Data**: Real-time temperature, humidity, wind, pressure, UV
- **API**: Weather.com Personal Weather Station

### Local Forecast (Predictions)
- **Source**: Local forecast generator
- **Coverage**: 3-day predictions
- **Features**: Iceland-appropriate weather patterns
- **Reliability**: Designed for local conditions

## 🎨 Design Features

### Dark Theme
- Custom CSS variables for consistent theming
- Beautiful gradient accents (blue to purple)
- Smooth animations and hover effects
- Glass morphism effects

### Icelandic Localization
- Complete UI translation to Icelandic
- Proper date/time formatting
- Weather terminology in Icelandic
- Reykjavik timezone support

### Responsive Design
- Mobile-first approach
- Adaptive sidebar navigation
- Optimized for all screen sizes
- Touch-friendly interface

## 📊 Monitoring & Logging

- Comprehensive application logging
- Weather API error tracking
- Production-ready log configuration
- Health check endpoints

## 🔐 Security Features

- Environment-based configuration
- Secure secret key management
- HTTPS enforcement in production
- CSRF protection
- SQL injection prevention

## 🧪 Testing

Test your production configuration:
```bash
python production_test.py
```

Generate secure secret key:
```bash
python generate_secret_key.py
```

## 📈 Performance

- Static file compression with Whitenoise
- Efficient database queries
- Client-side caching
- Optimized image assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is private and proprietary.

## 🙏 Acknowledgments

- Weather data provided by Weather.com API
- Icons from Bootstrap Icons
- Maps powered by Leaflet
- Built with Django framework

---

**Veðrið hjá Óla Bj.** - Your personal weather station dashboard 🌤️ 