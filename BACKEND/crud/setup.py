import os
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'charitize.settings')
django.setup()

def setup_project():
    print("Setting up Charitize Backend...")
    
    # Run migrations
    print("\n1. Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser
    print("\n2. Creating superuser...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@charitize.com',
            password='admin123',
            role='admin'
        )
        print("Superuser created: admin/admin123")
    
    # Create sample data
    print("\n3. Creating sample data...")
    from donations.models import Campaign
    
    if not Campaign.objects.exists():
        Campaign.objects.create(
            title="Help Children in Need",
            description="Providing education and healthcare for underprivileged children",
            goal_amount=100000,
            current_amount=45000,
            start_date="2024-01-01",
            end_date="2024-12-31",
            is_active=True
        )
        
        Campaign.objects.create(
            title="Environmental Conservation",
            description="Planting trees and cleaning our environment",
            goal_amount=50000,
            current_amount=15000,
            start_date="2024-03-01",
            end_date="2024-11-30",
            is_active=True
        )
        
        print("Sample campaigns created!")
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Quick Start Guide:")
    print("1. Run server: python manage.py runserver")
    print("2. Admin URL: http://127.0.0.1:8000/admin")
    print("3. API Base URL: http://127.0.0.1:8000/api")
    print("4. Login: admin / admin123")

if __name__ == '__main__':
    setup_project()