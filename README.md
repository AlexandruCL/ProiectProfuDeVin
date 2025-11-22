# 🍷 ProfuDeVin - Wine E-Commerce Platform

A modern, full-featured e-commerce platform for wine and spirits, built with Django and styled with a beautiful burgundy theme.

![Django](https://img.shields.io/badge/Django-5.2.7-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Authentication](#authentication)
- [Email Configuration](#email-configuration)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🛒 E-Commerce Functionality
- **Product Catalog**: Browse wines and spirits with detailed information
- **Shopping Cart**: Add/remove items, update quantities
- **Checkout System**: Complete order processing with customer information
- **Order History**: Track past orders and their status
- **Product Search**: Find wines and spirits easily

### 👤 User Management
- **Custom Authentication**: Sign up with email/username
- **Social Authentication**: Login with Google/Facebook via django-allauth
- **Password Security**: 
  - Custom password validators (uppercase, digit, special character, 8+ chars)
  - Password visibility toggle on all forms
  - Secure password reset via email
- **User Profiles**: Update personal information and view order history
- **Set Password Feature**: Social login users can add password for email/password login

### 🎨 Modern UI/UX
- **Responsive Design**: Beautiful burgundy-themed interface using Tailwind CSS
- **Animated Elements**: Smooth transitions and hover effects
- **Custom Checkboxes**: Styled form elements matching the brand
- **Password Visibility Toggle**: Eye icon to show/hide passwords
- **Error Handling**: User-friendly error messages with tooltips

### 📧 Email Features
- **Password Reset**: Email-based password recovery
- **SendGrid Integration**: Reliable email delivery
- **Custom Email Templates**: Branded email communications

### 🔒 Security Features
- **CSRF Protection**: Built-in Django CSRF tokens
- **Password Strength Validation**: Custom validators
- **Session Management**: 2-day session timeout
- **Secure Password Storage**: Django's built-in password hashing

## 🛠 Tech Stack

### Backend
- **Django 5.2.7**: Web framework
- **Python 3.11**: Programming language
- **SQLite**: Database (development)
- **django-allauth**: Social authentication

### Frontend
- **Tailwind CSS**: Styling framework
- **Vanilla JavaScript**: Interactive elements
- **Custom CSS**: Brand-specific styling

### Email
- **SendGrid**: Email delivery service
- **SMTP**: Email protocol

### Other Tools
- **python-decouple**: Environment variable management
- **pandas**: Data processing (if needed)

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AlexandruCL/ProiectProfuDeVin.git
   cd ProiectProfuDeVin
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   cd my_project
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   
   Create a `.env` file in the `my_project` directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   
   # Email Configuration (SendGrid)
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=your-sendgrid-api-key
   DEFAULT_FROM_EMAIL=your-verified-email@example.com
   
   # Google OAuth (optional)
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   
   # Facebook OAuth (optional)
   FACEBOOK_APP_ID=your-facebook-app-id
   FACEBOOK_APP_SECRET=your-facebook-app-secret
   ```

6. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Main site: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/

## ⚙️ Configuration

### Social Authentication Setup

#### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - `http://yourdomain.com/accounts/google/login/callback/` (production)
6. Add credentials to Django admin:
   - Go to `/admin/socialaccount/socialapp/`
   - Add Google as a Social Application
   - Enter Client ID and Secret Key
   - Select your site

#### Facebook OAuth
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login product
4. Configure OAuth redirect URIs:
   - `http://127.0.0.1:8000/accounts/facebook/login/callback/`
5. Add credentials to Django admin (similar to Google)

### Database Configuration

For production, replace SQLite with PostgreSQL or MySQL:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📧 Email Configuration

### SendGrid Setup

1. **Create SendGrid Account**
   - Sign up at [SendGrid](https://sendgrid.com/)
   - Free tier: 100 emails/day

2. **Generate API Key**
   - Go to Settings > API Keys
   - Create API Key with "Mail Send" permissions
   - Copy the key (you won't see it again)

3. **Verify Sender Identity**
   - Go to Settings > Sender Authentication
   - Verify a Single Sender
   - Use the email you want to send from

4. **Update .env file**
   ```env
   EMAIL_HOST_PASSWORD=your-sendgrid-api-key
   DEFAULT_FROM_EMAIL=verified-email@example.com
   ```

### Testing Email (Console Backend)

For development, use console backend to see emails in terminal:

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 🚀 Usage

### Running the Development Server

```bash
cd my_project
python manage.py runserver
```

### Creating Sample Data

Use Django admin panel to add products:

1. Login to admin: http://127.0.0.1:8000/admin/
2. Add Wines and Spirits through the admin interface
3. Upload product images to the media folder

### Managing Orders

Orders can be managed through:
- Django admin panel (`/admin/`)
- Custom order management views (if implemented)

## 📁 Project Structure

```
ProiectProfuDeVin/
├── my_project/                    # Main Django project
│   ├── manage.py                  # Django management script
│   ├── requirements.txt           # Python dependencies
│   ├── db.sqlite3                 # SQLite database
│   ├── my_project/                # Project configuration
│   │   ├── settings.py            # Django settings
│   │   ├── urls.py                # Main URL configuration
│   │   ├── wsgi.py                # WSGI configuration
│   │   └── asgi.py                # ASGI configuration
│   ├── my_app/                    # Main application
│   │   ├── models.py              # Database models
│   │   ├── views.py               # View functions
│   │   ├── forms.py               # Custom forms
│   │   ├── validators.py          # Password validators
│   │   ├── admin.py               # Admin configuration
│   │   ├── context_processors.py # Template context
│   │   ├── migrations/            # Database migrations
│   │   └── templatetags/          # Custom template filters
│   ├── templates/                 # HTML templates
│   │   ├── my_app/                # App-specific templates
│   │   │   ├── home.html
│   │   │   ├── signup.html
│   │   │   ├── login.html
│   │   │   ├── profile.html
│   │   │   ├── wine_list.html
│   │   │   ├── cart.html
│   │   │   ├── checkout.html
│   │   │   ├── set_password.html
│   │   │   └── password_reset_*.html
│   │   └── socialaccount/         # Social auth templates
│   │       ├── login.html
│   │       └── signup.html
│   ├── static/                    # Static files
│   │   ├── css/                   # Stylesheets
│   │   └── images/                # Images
│   └── media/                     # User-uploaded files
│       ├── wines/                 # Wine images
│       └── spirits/               # Spirit images
├── databseschema.drawio           # Database schema diagram
└── README.md                      # This file
```

## 🔐 Authentication

### User Registration
- Email/username + password
- Password requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one digit
  - At least one special character (@#$%^&*)

### Social Login
- Google OAuth
- Facebook OAuth
- Automatic account creation
- Optional password setup for social users

### Password Reset
1. User clicks "Forgot Password"
2. Enters email address
3. Receives reset link via email
4. Creates new password
5. Redirects to login

### Password Change (Logged-in Users)
- Two options:
  1. **Email Flow**: Click "Change Password" → logout → receive email
  2. **Set Password**: For social login users to add password

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Alexandru Cristea Laurențiu**
- GitHub: [@AlexandruCL](https://github.com/AlexandruCL)
- Email: alex.cristea.laur2004@gmail.com

## 🙏 Acknowledgments

- Django Framework
- Tailwind CSS
- SendGrid
- django-allauth
- All open-source contributors

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/AlexandruCL/ProiectProfuDeVin/issues)
- Contact: alex.cristea.laur2004@gmail.com

## 🔮 Future Enhancements

- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Advanced product filtering and search
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Admin dashboard with analytics
- [ ] Email notifications for order status
- [ ] Multi-language support
- [ ] Mobile app
- [ ] API for third-party integrations
- [ ] Inventory management system

---

**Made with ❤️ and 🍷 by Alexandru Cristea Laurențiu**
