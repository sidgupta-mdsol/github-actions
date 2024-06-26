import subprocess
import importlib

# Function to check if a Python package is installed
def is_package_installed(package_name):
    try: 
        importlib.import_module(package_name)
        return True
    except ImportError as e:
        print(str(e))
        return False

# Function to install a Python package using pip        
def install_package(package_name):
    subprocess.run(["pip3", "install", package_name])

# Function to check if wkhtmltopdf is installed
def is_wkhtmltopdf_installed():
    result= subprocess.run(["which", "wkhtmltopdf"])
    return result==0

# Function to install wkhtmltopdf
def install_wkhtmltopdf():
    subprocess.run(["apt-get" , "install", "-y", "wkhtmltopdf"])

# Required Python packages
requested_packages=["requests", "pdfkit","os","json"]

# Check and install Python packages
for package in requested_packages:
    present = is_package_installed(package)
    if present:
        print(f"Python package \"{package}\" is alerady installled")
    else:
        install_package(package)
        print(f"Installing Python package \"{package}\" ...")

# Check and install wkhtmltopdf
if is_wkhtmltopdf_installed():
    print("wkhtmltopdf is already installed.")
else:
    print("Installing wkhtmltopdf...")
    install_wkhtmltopdf()

print("All necessary libraries and tools are installed.")


