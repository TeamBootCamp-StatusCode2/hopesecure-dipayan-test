from django.core.management.base import BaseCommand
from employees.models import Employee, Department
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample employees'

    def handle(self, *args, **options):
        # Create departments first
        departments_data = [
            {'name': 'Engineering', 'description': 'Software development and engineering'},
            {'name': 'Marketing', 'description': 'Marketing and communications'},
            {'name': 'Finance', 'description': 'Financial operations and accounting'},
            {'name': 'HR', 'description': 'Human resources and people operations'},
            {'name': 'IT', 'description': 'Information technology and support'},
        ]

        for dept_data in departments_data:
            department, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults=dept_data
            )
            if created:
                self.stdout.write(f'Created department: {department.name}')

        # Get departments
        engineering = Department.objects.get(name='Engineering')
        marketing = Department.objects.get(name='Marketing')
        finance = Department.objects.get(name='Finance')
        hr = Department.objects.get(name='HR')
        it = Department.objects.get(name='IT')

        sample_employees = [
            {
                'employee_id': 'EMP001',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@company.com',
                'department': engineering,
                'position': 'Software Engineer',
                'hire_date': date(2023, 1, 15),
                'risk_level': 'medium',
                'phone_number': '+1-555-0101',
                'manager_email': 'manager@company.com',
                'office_location': 'New York',
                'is_active': True,
                'phishing_susceptibility_score': 45
            },
            {
                'employee_id': 'EMP002',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@company.com',
                'department': marketing,
                'position': 'Marketing Manager',
                'hire_date': date(2022, 8, 10),
                'risk_level': 'low',
                'phone_number': '+1-555-0102',
                'manager_email': 'director@company.com',
                'office_location': 'San Francisco',
                'is_active': True,
                'phishing_susceptibility_score': 25
            },
            {
                'employee_id': 'EMP003',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'email': 'mike.johnson@company.com',
                'department': finance,
                'position': 'Financial Analyst',
                'hire_date': date(2023, 3, 20),
                'risk_level': 'high',
                'phone_number': '+1-555-0103',
                'manager_email': 'cfo@company.com',
                'office_location': 'Chicago',
                'is_active': True,
                'phishing_susceptibility_score': 75
            },
            {
                'employee_id': 'EMP004',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'email': 'sarah.wilson@company.com',
                'department': hr,
                'position': 'HR Specialist',
                'hire_date': date(2022, 11, 5),
                'risk_level': 'medium',
                'phone_number': '+1-555-0104',
                'manager_email': 'hr.director@company.com',
                'office_location': 'Austin',
                'is_active': True,
                'phishing_susceptibility_score': 50
            },
            {
                'employee_id': 'EMP005',
                'first_name': 'David',
                'last_name': 'Brown',
                'email': 'david.brown@company.com',
                'department': it,
                'position': 'System Administrator',
                'hire_date': date(2021, 6, 12),
                'risk_level': 'low',
                'phone_number': '+1-555-0105',
                'manager_email': 'it.manager@company.com',
                'office_location': 'Seattle',
                'is_active': True,
                'phishing_susceptibility_score': 20
            }
        ]

        created_count = 0
        for employee_data in sample_employees:
            employee, created = Employee.objects.get_or_create(
                email=employee_data['email'],
                defaults=employee_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created employee: {employee.first_name} {employee.last_name}')
            else:
                self.stdout.write(f'Employee already exists: {employee.first_name} {employee.last_name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new employees')
        )
