# File: deploy.py
# A custom deployment script to upload all your project files to Windmill via its REST API.
# This script bypasses the problematic 'wmill sync' command.

import os
import requests
import json
import yaml
from typing import Dict, Any

# --- CONFIGURATION: EDIT THESE THREE VARIABLES ---
WINDMILL_URL = "http://5.78.138.105/:8088"  # <--- IMPORTANT: REPLACE WITH YOUR VPS IP
WINDMILL_TOKEN = "sBICrMZeDv0LtWH2D7xPSskyPNUSUX1y"    # <--- IMPORTANT: REPLACE WITH YOUR TOKEN
WINDMILL_WORKSPACE = "cryptex"       # The first workspace we will deploy to
# -------------------------------------------------

HEADERS = {"Authorization": f"Bearer {WINDMILL_TOKEN}"}

def deploy_script(filepath: str, workspace: str):
    """Deploys a single Python or TypeScript script."""
    with open(filepath, "r") as f:
        content = f.read()
    
    # Determine language from file extension
    language = "python" if filepath.endswith(".py") else "typescript"
    
    # Construct the path as Windmill expects it (e.g., scripts/inputs/s_webhook_trigger)
    path_in_windmill = os.path.splitext(os.path.relpath(filepath, "."))[0].replace(os.path.sep, "/")
    
    payload = {
        "path": path_in_windmill,
        "content": content,
        "language": language,
        "description": f"Deployed via custom script from {filepath}"
    }
    
    url = f"{WINDMILL_URL}/api/w/{workspace}/scripts/create"
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        # 409 Conflict means it already exists, so we try to update it
        if response.status_code == 409:
            print(f"INFO: Script '{path_in_windmill}' already exists. Updating...")
            url = f"{WINDMILL_URL}/api/w/{workspace}/scripts/update"
            response = requests.post(url, headers=HEADERS, json=payload)

        response.raise_for_status()
        print(f"✅ Successfully deployed SCRIPT: {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED to deploy SCRIPT: {filepath}")
        print(f"   Error: {e.response.text if e.response else e}")

def deploy_flow(filepath: str, workspace: str):
    """Deploys a single YAML flow."""
    with open(filepath, "r") as f:
        # We send the raw YAML content
        content = f.read()
        # We also parse it to get the path
        parsed_yaml = yaml.safe_load(content)

    path_in_windmill = os.path.splitext(os.path.basename(filepath))[0]
    
    payload = {
        "path": path_in_windmill,
        "value": parsed_yaml,
        "description": f"Deployed via custom script from {filepath}"
    }
    
    url = f"{WINDMILL_URL}/api/w/{workspace}/flows/create"
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 409:
            print(f"INFO: Flow '{path_in_windmill}' already exists. Updating...")
            url = f"{WINDMILL_URL}/api/w/{workspace}/flows/update"
            response = requests.post(url, headers=HEADERS, json=payload)

        response.raise_for_status()
        print(f"✅ Successfully deployed FLOW: {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED to deploy FLOW: {filepath}")
        print(f"   Error: {e.response.text if e.response else e}")

def main():
    """Main function to find and deploy all project files."""
    
    # --- DEPLOY CRYPTEX PROJECT ---
    print("\n--- Deploying cryptex_project to workspace: cryptex_ai_omega ---")
    os.chdir("cryptex_project")
    for root, _, files in os.walk("."):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith((".py", ".ts")):
                deploy_script(filepath, "cryptex_ai_omega")
            elif file.endswith(".yml"):
                deploy_flow(filepath, "cryptex_ai_omega")
    os.chdir("..") # Go back to the root project directory

    # --- DEPLOY CONTENT FACTORY PROJECT ---
    print("\n--- Deploying content_project to workspace: content_factory ---")
    os.chdir("content_project")
    for root, _, files in os.walk("."):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith((".py", ".ts")):
                deploy_script(filepath, "content_factory")
            elif file.endswith(".yml"):
                deploy_flow(filepath, "content_factory")
    os.chdir("..")

    print("\n🚀 Deployment complete!")


if __name__ == "__main__":
    # First, check if the configuration has been set
    if "YOUR_VPS_IP_ADDRESS" in WINDMILL_URL or "YOUR_WINDMILL_AUTH_TOKEN" in WINDMILL_TOKEN:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: Please edit the deploy.py script and fill in your")
        print("!!!        WINDMILL_URL and WINDMILL_TOKEN variables.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        main()