import subprocess
import sys
import importlib

# Function to check if a Python package is installed
def is_package_installed(package_name):
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

# Function to install a Python package using pip
def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Function to check if wkhtmltopdf is installed
def is_wkhtmltopdf_installed():
    result = subprocess.run(['which', 'wkhtmltopdf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

# Function to install wkhtmltopdf
def install_wkhtmltopdf():
    subprocess.check_call(['sudo', 'apt-get', 'update'])
    subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'wkhtmltopdf'])

# Required Python packages
required_packages = ["pdfkit", "requests"]

# Check and install Python packages
for package in required_packages:
    if is_package_installed(package):
        print(f"Python package {package} is already installed.")
    else:
        print(f"Installing Python package {package}...")
        install_package(package)

# Check if 'os' and 'json' are available (they are part of Python's standard library)
print("Checking if 'os' and 'json' are available...")
try:
    import os
    import json
    print("'os' and 'json' packages are already available (part of Python standard library).")
except ImportError:
    print("Error: 'os' and/or 'json' are missing, but they should be part of the Python standard library.")
    sys.exit(1)

# Check and install wkhtmltopdf
if is_wkhtmltopdf_installed():
    print("wkhtmltopdf is already installed.")
else:
    print("Installing wkhtmltopdf...")
    install_wkhtmltopdf()

print("All necessary libraries and tools are installed.")
