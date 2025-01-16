import os
import subprocess
import shutil

# Function to install system dependencies
def install_system_packages():
    packages = [
        "python3-venv",  # Added venv for pwncat
        "python3-poetry",  # Added poetry for pwncat
    ]

    for package in packages:
        print(f"Installing {package}...")
        result = subprocess.run(["sudo", "apt", "install", "-y", package], text=True, capture_output=True)
        if result.returncode == 0:
            print(f"{package} installed successfully.")
        else:
            print(f"Failed to install {package}: {result.stderr}")

# Function to install pwncat-cs via pip
def install_pwncat_cs():
    print("Installing pwncat-cs...")
    result = subprocess.run(["pip", "install", "pwncat-cs"], text=True, capture_output=True)
    if result.returncode == 0:
        print("pwncat-cs installed successfully.")
    else:
        print(f"Failed to install pwncat-cs: {result.stderr}")

# Function to install pwncat
def install_pwncat(home_dir):
    print("Installing pwncat...")
    repo_url = "https://github.com/calebstewart/pwncat"
    repo_path = os.path.join(home_dir, "pwncat")

    # Clone the pwncat repository
    if not os.path.exists(repo_path):
        result = subprocess.run(["git", "clone", repo_url, repo_path], text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Failed to clone pwncat: {result.stderr}")
            return
        print(f"Cloned pwncat into {repo_path}.")

    # Install dependencies with poetry in the pwncat directory
    result = subprocess.run(["poetry", "install"], cwd=repo_path, text=True, capture_output=True)
    if result.returncode == 0:
        print("pwncat dependencies installed successfully.")
    else:
        print(f"Failed to install pwncat dependencies: {result.stderr}")

# Function to install asnmap via Go and copy to the specified directory
def install_asnmap(home_dir):
    print("Installing asnmap...")
    result = subprocess.run(["go", "install", "github.com/projectdiscovery/asnmap/cmd/asnmap@latest"], text=True, capture_output=True)
    if result.returncode == 0:
        print("asnmap installed successfully.")
        
        # Copy the binary from /bin to the host directory
        asnmap_binary = "/bin/asnmap"
        target_path = os.path.join(home_dir, "asnmap")  # Path to copy the asnmap binary
        if os.path.exists(asnmap_binary):
            print(f"Copying asnmap binary to {target_path}...")
            subprocess.run(f"cp {asnmap_binary} {target_path}", shell=True)
            print(f"asnmap binary copied to {target_path}.")
        else:
            print("asnmap binary not found after installation.")
    else:
        print(f"Failed to install asnmap: {result.stderr}")

# Function to clone repositories and run their setup
def setup_repository(repo_url, repo_name, setup_command=None, target_dir=None):
    print(f"Cloning {repo_name}...")
    clone_path = target_dir if target_dir else os.getcwd()
    repo_path = os.path.join(clone_path, repo_name)

    if not os.path.exists(repo_path):
        result = subprocess.run(["git", "clone", repo_url, repo_path], text=True, capture_output=True)
        if result.returncode == 0:
            print(f"Cloned {repo_name} into {repo_path}.")
            if setup_command:
                print(f"Setting up {repo_name}...")
                setup_result = subprocess.run(setup_command, cwd=repo_path, shell=True, text=True, capture_output=True)
                if setup_result.returncode == 0:
                    print(f"{repo_name} setup completed successfully.")
                else:
                    print(f"Failed to set up {repo_name}: {setup_result.stderr}")
        else:
            print(f"Failed to clone {repo_name}: {result.stderr}")
    else:
        print(f"{repo_name} already exists in {repo_path}. Skipping clone.")

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

    # Install pwncat-cs first
    install_pwncat_cs()

    # Install pwncat
    install_pwncat(home_dir)

    # Install other tools
    install_asnmap(home_dir)
    install_routersploit(home_dir)
    install_cerbrutus(home_dir)
    install_g2l(home_dir)

    # Add tools to PATH
    add_tools_to_path(home_dir)

    print(f"Setup complete! All tools are installed in the directory: {home_dir}.")

if __name__ == "__main__":
    main()
