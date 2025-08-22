#!/bin/bash

# HopeSecure SendGrid Quick Setup Script

echo "🚀 HopeSecure SendGrid Setup"
echo "=========================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    source env/bin/activate
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your SendGrid credentials."
else
    echo "✅ .env file already exists"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q sendgrid email-validator requests beautifulsoup4

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "📧 SendGrid Configuration Steps:"
echo "================================"
echo "1. Sign up at https://sendgrid.com"
echo "2. Create an API key with 'Full Access'"
echo "3. Edit .env file and add your API key:"
echo "   SENDGRID_API_KEY=your-api-key-here"
echo "   DEFAULT_FROM_EMAIL=security@yourdomain.com"
echo ""
echo "4. Test your setup:"
echo "   python test_sendgrid.py"
echo ""
echo "5. Start the Django server:"
echo "   python manage.py runserver"
echo ""
echo "🎯 Ready to create phishing campaigns!"
