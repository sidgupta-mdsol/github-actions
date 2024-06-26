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
    return result.returncode == 0

# Function to check if wkhtmltopdf is installed
def is_wkhtmltopdf_installed():
    result = subprocess.run(["which", "wkhtmltopdf"])
    return result.returncode == 0

# Function to install wkhtmltopdf
def install_wkhtmltopdf():
    result_install = subprocess.run(['apt-get', 'install', '-y', 'wkhtmltopdf'])
    return result_install.returncode == 0

# Required Python packages
requested_packages = ["requests", "pdfkit", "os", "json"]

# Dictionary to track installation status
install_status = {}

# Check and install Python packages
for package in requested_packages:
    if is_package_installed(package):
        print(f"Python package \"{package}\" is already installed.")
        install_status[package] = "Already installed"
    else:
        print(f"Installing Python package \"{package}\"...")
        if install_package(package):
            print(f"Successfully installed Python package \"{package}\".")
            install_status[package] = "Installed successfully"
        else:
            print(f"Failed to install Python package \"{package}\".")
            install_status[package] = "Failed to install"
            exit(1)

# Check and install wkhtmltopdf
if is_wkhtmltopdf_installed():
    print("wkhtmltopdf is already installed.")
    install_status["wkhtmltopdf"] = "Already installed"
else:
    print("Installing wkhtmltopdf...")
    if install_wkhtmltopdf():
        print("Successfully installed wkhtmltopdf.")
        install_status["wkhtmltopdf"] = "Installed successfully"
    else:
        print("Failed to install wkhtmltopdf.")
        install_status["wkhtmltopdf"] = "Failed to install"
        exit(1)

# Final summary
print("\nInstallation summary:")
for package, status in install_status.items():
    print(f"- {package}: {status}")
