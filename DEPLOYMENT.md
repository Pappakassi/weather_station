# Veðrið hjá Óla Bj. - Deployment Guide

This guide covers deploying your weather station app to production.

## 🚀 Quick Deployment Options

### Option 1: Heroku (Recommended for beginners)

**Automated Deployment:**
```bash
./deploy.sh
```

**Manual Deployment:**

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create your-weather-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY="your-super-secret-key-here"
   heroku config:set DEBUG=False
   heroku config:set WEATHER_API_KEY="4f4244de5091498b8244de5091798b81"
   heroku config:set WEATHER_STATION_ID="IAKURE31"
   ```

4. **Add PostgreSQL database (optional)**
   ```bash
   heroku addons:create heroku-postgresql:essential-0
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Ready for production deployment"
   git push heroku main
   ```

6. **Open your app**
   ```bash
   heroku open
   ```

### Option 2: Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Set environment variables in Railway dashboard:**
   - `SECRET_KEY`: Generate a new secret key
   - `DEBUG`: False
   - `WEATHER_API_KEY`: 4f4244de5091498b8244de5091798b81
   - `WEATHER_STATION_ID`: IAKURE31
4. **Add PostgreSQL database from Railway's marketplace (optional)**
5. **Deploy automatically triggers**

### Option 3: DigitalOcean App Platform

1. **Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)**
2. **Create new app from GitHub**
3. **Configure environment variables**
4. **Add managed PostgreSQL database (optional)**
5. **Deploy**

## 🔧 Environment Variables Required

Create these environment variables in your hosting platform:

```bash
SECRET_KEY=your-super-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:pass@host:port/dbname  # Optional - SQLite used if not set
WEATHER_API_KEY=4f4244de5091498b8244de5091798b81
WEATHER_STATION_ID=IAKURE31
```

## ⚙️ Database Configuration

- **Development**: SQLite (automatic, no setup required)
- **Production**: SQLite (default) or PostgreSQL (optional)

**Note**: PostgreSQL requires Python 3.12 or earlier due to psycopg2 compatibility. The app works perfectly with SQLite for production use.

## 🔐 Security Checklist

- [ ] SECRET_KEY is set and unique
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS contains your domain
- [ ] Using HTTPS (most platforms enable this automatically)
- [ ] Database credentials are secure (if using PostgreSQL)
- [ ] Weather API key is kept private

## 📁 File Structure

```
weather_station_v2/
├── weather_station/        # Django project settings
├── weather/                # Weather app
├── templates/              # HTML templates
├── static/                 # Static files (development)
├── staticfiles/            # Static files (production)
├── logs/                   # Application logs
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku process file
├── runtime.txt            # Python version specification
├── env.example            # Environment variables template
├── deploy.sh              # Automated deployment script
├── generate_secret_key.py # Secret key generator
├── production_test.py     # Production settings test
└── DEPLOYMENT.md          # This file
```

## 🗄️ Database

- **Development**: SQLite (automatic)
- **Production**: SQLite (default) or PostgreSQL (optional)

The app automatically switches based on the `DATABASE_URL` environment variable.

**Python Version Compatibility:**
- Python 3.11-3.12: Full PostgreSQL support
- Python 3.13+: SQLite only (PostgreSQL libraries not yet compatible)

## 📊 Monitoring

The app includes comprehensive logging:
- Console output for immediate debugging
- File logging in production (`logs/django.log`)
- Weather service logging for API issues

## 🔄 Updates and Maintenance

1. **Update dependencies**
   ```bash
   pip freeze > requirements.txt
   ```

2. **Database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Collect static files** (if needed)
   ```bash
   python manage.py collectstatic --noinput
   ```

## 🚨 Troubleshooting

### Common Issues:

1. **Static files not loading**
   - Check `STATIC_ROOT` setting
   - Run `python manage.py collectstatic`
   - Ensure Whitenoise is configured

2. **Database connection errors**
   - Verify `DATABASE_URL` environment variable
   - Check database credentials
   - Fallback: Remove DATABASE_URL to use SQLite

3. **Weather data not loading**
   - Verify `WEATHER_API_KEY` and `WEATHER_STATION_ID`
   - Check API rate limits
   - Review logs for specific errors

4. **Security errors**
   - Ensure `SECRET_KEY` is set
   - Check `ALLOWED_HOSTS` includes your domain
   - Verify HTTPS is enabled

5. **PostgreSQL issues**
   - Use Python 3.12 or earlier
   - Consider using SQLite for simplicity

## 📞 Support

For deployment issues:
1. Check the application logs
2. Verify all environment variables are set
3. Test locally with production settings
4. Check your hosting platform's documentation

## 🧪 Testing

Test your production settings:
```bash
python production_test.py
```

Generate a secure secret key:
```bash
python generate_secret_key.py
```

Deploy automatically to Heroku:
```bash
./deploy.sh
```

## 🎉 Success!

Your weather station should now be live! The app features:
- ✅ Real-time weather data from your personal station
- ✅ 3-day local forecast
- ✅ Beautiful dark-themed Icelandic interface
- ✅ Interactive map
- ✅ Responsive design for all devices
- ✅ Production-ready security and performance 