# Set the default shell
set shell := ["bash", "-cu"]

# Setup development environment with uv (recommended)
setup-uv:
    uv venv
    uv pip install -r requirements.txt
    @echo "✅ Environment ready! Activate with: source .venv/bin/activate"

# Setup development environment with pip
setup-pip:
    python -m venv venv
    ./venv/bin/pip install -r requirements.txt
    @echo "✅ Environment ready! Activate with: source venv/bin/activate"

# Install dependencies (works with any active environment)
install:
    pip install -r requirements.txt

# Install dependencies with uv (faster)
install-uv:
    uv pip install -r requirements.txt

# Activate virtualenv
activate:
    source venv/bin/activate

# Run development server
run:
    python manage.py runserver

# Run server with specific IP and port
serve ip="127.0.0.1" port="8000":
    python manage.py runserver {{ip}}:{{port}}

# Run migrations
migrate:
    python manage.py makemigrations
    python manage.py migrate

# Create a superuser
superuser:
    python manage.py createsuperuser

# Collect static files
collectstatic:
    python manage.py collectstatic --noinput

# Open Django shell
shell:
    python manage.py shell

# Run tests
test:
    python manage.py test

# Run tests with verbose output
test-verbose:
    python manage.py test --verbosity=2

# Run specific test class
test-class CLASS:
    python manage.py test {{CLASS}}

# Run specific test method
test-method METHOD:
    python manage.py test {{METHOD}}

# Run tests with coverage
coverage:
    coverage run manage.py test && coverage report

# Generate HTML coverage report
coverage-html:
    coverage run manage.py test && coverage html && open htmlcov/index.html

# Clear `.pyc` files
clean:
    find . -name "*.pyc" -delete

# Load initial data
loaddata:
    python manage.py loaddata initial_data.json

