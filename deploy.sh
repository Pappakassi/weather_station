#!/bin/bash

# Deploy Veðrið hjá Óla Bj. to Heroku
# Run this script after setting up your Heroku app

echo "🚀 Deploying Veðrið hjá Óla Bj. to Heroku"
echo "=========================================="

# Check if heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   brew tap heroku/brew && brew install heroku"
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please log in to Heroku first:"
    heroku login
fi

# Get app name
read -p "Enter your Heroku app name: " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name is required"
    exit 1
fi

echo "🔧 Setting up Heroku app: $APP_NAME"

# Create app if it doesn't exist
heroku apps:info $APP_NAME &> /dev/null || heroku create $APP_NAME

# Generate and set secret key
echo "🔑 Generating secret key..."
SECRET_KEY=$(python generate_secret_key.py | grep "SECRET_KEY=" | cut -d'=' -f2)

# Set environment variables
echo "⚙️  Setting environment variables..."
heroku config:set SECRET_KEY="$SECRET_KEY" --app $APP_NAME
heroku config:set DEBUG=False --app $APP_NAME
heroku config:set WEATHER_API_KEY="4f4244de5091498b8244de5091798b81" --app $APP_NAME
heroku config:set WEATHER_STATION_ID="IAKURE31" --app $APP_NAME

# Set allowed hosts
heroku config:set ALLOWED_HOSTS="$APP_NAME.herokuapp.com,$APP_NAME.heroku.com" --app $APP_NAME

echo "🗄️  Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:essential-0 --app $APP_NAME || echo "Database already exists"

echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Production deployment" || echo "No changes to commit"

# Add heroku remote if it doesn't exist
git remote get-url heroku &> /dev/null || heroku git:remote -a $APP_NAME

# Deploy
git push heroku main

echo "🎉 Deployment complete!"
echo "📱 Your app is available at: https://$APP_NAME.herokuapp.com"
echo "🔧 To view logs: heroku logs --tail --app $APP_NAME"
echo "⚙️  To open app: heroku open --app $APP_NAME" 