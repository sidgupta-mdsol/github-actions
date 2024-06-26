import subprocess
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
    result = subprocess.run(["pip3", "install", package_name])
    if result.returncode == 0:
        return True
    else:
        return False

# Function to check if wkhtmltopdf is installed
def is_wkhtmltopdf_installed():
    result = subprocess.run(["which", "wkhtmltopdf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

# Function to install wkhtmltopdf
def install_wkhtmltopdf():
    result = subprocess.run(["apt-get", "install", "-y", "wkhtmltopdf"])
    if result.returncode == 0:
        return True
    else:
        return False

# Required Python packages
requested_packages = ["requests", "pdfkit", "os", "json"]

# Check and install Python packages
for package in requested_packages:
    if is_package_installed(package):
        print(f"Python package \"{package}\" is already installed.")
    else:
        print(f"Installing Python package \"{package}\"...")
        if install_package(package):
            print(f"Successfully installed Python package \"{package}\".")
        else:
            print(f"Failed to install Python package \"{package}\".")

# Check and install wkhtmltopdf
if is_wkhtmltopdf_installed():
    print("wkhtmltopdf is already installed.")
else:
    print("Installing wkhtmltopdf...")
    if install_wkhtmltopdf():
        print("Successfully installed wkhtmltopdf.")
    else:
        print("Failed to install wkhtmltopdf.")

print("All necessary libraries and tools are installed.")
