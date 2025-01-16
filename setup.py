import os
import subprocess
import time
import shutil

# Function to install system dependencies
def install_system_packages():
    packages = [
        "airgeddon",
        "iputils-tracepath",
        "python3-venv",  # Added venv for pwncat
        "python3-poetry",  # Added poetry for pwncat
        "golang"
    ]

    for package in packages:
        print(f"Installing {package}...")
        result = subprocess.run(["sudo", "apt", "install", "-y", package], text=True, capture_output=True)
        if result.returncode == 0:
            print(f"{package} installed successfully.")
        else:
            print(f"Failed to install {package}: {result.stderr}")

# Function to install asnmap via Go and copy to the desired directory
def install_asnmap(home_dir):
    print("Installing asnmap...")
    result = subprocess.run(["go", "install", "github.com/projectdiscovery/asnmap/cmd/asnmap@latest"], text=True, capture_output=True)
    if result.returncode == 0:
        print("asnmap installed successfully.")
        time.sleep(2)  # Wait for installation to complete
        asnmap_binary = shutil.which("asnmap")
        if asnmap_binary:
            target_path = os.path.join(home_dir, "asnmap")
            shutil.copy(asnmap_binary, target_path)
            print(f"asnmap binary copied to {target_path}.")
        else:
            print("asnmap binary not found after installation.")
    else:
        print(f"Failed to install asnmap: {result.stderr}")

# Function to install pwncat
def install_pwncat(home_dir):
    print("Installing pwncat...")

    # Clone the pwncat repository
    repo_url = "https://github.com/calebstewart/pwncat"
    repo_path = os.path.join(home_dir, "pwncat")

    if not os.path.exists(repo_path):
        print("Cloning pwncat repository...")
        result = subprocess.run(["git", "clone", repo_url, repo_path], text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Failed to clone pwncat: {result.stderr}")
            return
        print(f"Cloned pwncat into {repo_path}.")
    else:
        print(f"pwncat already exists in {repo_path}. Skipping clone.")

    # Install pwncat-cs in the pwncat directory
    print("Installing pwncat-cs...")
    result = subprocess.run(["pip", "install", "pwncat-cs"], cwd=repo_path, text=True, capture_output=True)
    if result.returncode == 0:
        print("pwncat-cs installed successfully.")
    else:
        print(f"Failed to install pwncat-cs: {result.stderr}")

    # Install distutils module via apt (for Ubuntu-based systems)
    print("Installing distutils module...")
    result = subprocess.run(["sudo", "apt", "install", "-y", "python3-distutils"], text=True, capture_output=True)
    if result.returncode == 0:
        print("distutils installed successfully.")
    else:
        print(f"Failed to install distutils: {result.stderr}")

    # Ensure poetry is installed and working
    print("Checking if poetry is installed...")
    result = subprocess.run(["poetry", "--version"], text=True, capture_output=True)
    if result.returncode == 0:
        print(f"Poetry version: {result.stdout.strip()}")
    else:
        print(f"Poetry not installed or not found: {result.stderr}")
        return

    # Install dependencies with poetry in the pwncat directory
    print("Installing dependencies using poetry...")
    result = subprocess.run(["poetry", "install"], cwd=repo_path, text=True, capture_output=True)
    if result.returncode == 0:
        print("pwncat dependencies installed successfully.")
    else:
        print(f"Failed to install pwncat dependencies: {result.stderr}")

    # Give some time to ensure everything is installed properly
    time.sleep(4)

    # Run poetry lock --no-update to ensure the lock file is up-to-date
    print("Running poetry lock --no-update...")
    result = subprocess.run(["poetry", "lock", "--no-update"], cwd=repo_path, text=True, capture_output=True)
    if result.returncode == 0:
        print("poetry lock completed successfully.")
    else:
        print(f"Failed to run poetry lock: {result.stderr}")

# Function to install routersploit
def install_routersploit(home_dir):
    print("Installing routersploit...")
    repo_url = "https://github.com/threat9/routersploit"
    setup_repository(repo_url, "routersploit", "python3 setup.py install", home_dir)

# Function to install cerbrutus
def install_cerbrutus(home_dir):
    print("Installing cerbrutus...")
    repo_url = "https://github.com/Cerbrutus-BruteForcer/cerbrutus"
    setup_repository(repo_url, "cerbrutus", None, home_dir)

# Function to install g2l
def install_g2l(home_dir):
    print("Installing g2l...")
    repo_url = "https://github.com/biskit069/g2l"
    setup_repository(repo_url, "g2l", "python3 setup.py install", home_dir)

# Function to add tools to PATH
def add_tools_to_path(home_dir):
    bashrc_path = os.path.expanduser("~/.bashrc")

    with open(bashrc_path, "a") as bashrc:
        bashrc.write(f"\n# Add tools to PATH\n")
        bashrc.write(f"export PATH=\"$PATH:{home_dir}\"\n")

    print(f"Tools directory {home_dir} added to PATH. Please restart your terminal for changes to take effect.")

# Main setup function
def main():
    print("Setting up tools...")

    # Get the home directory based on the current user
    home_dir = os.path.expanduser(f"/home/{os.getlogin()}")

    # Ensure the home directory exists
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)

    # Install system dependencies
    install_system_packages()

    # Install asnmap
    install_asnmap(home_dir)

    # Install pwncat
    install_pwncat(home_dir)

    # Install other tools (routersploit, cerbrutus, g2l)
    install_routersploit(home_dir)
    install_cerbrutus(home_dir)
    install_g2l(home_dir)

    # Add tools to PATH
    add_tools_to_path(home_dir)

    print(f"Setup complete! All tools are installed in the directory: {home_dir}.")

if __name__ == "__main__":
    main()
