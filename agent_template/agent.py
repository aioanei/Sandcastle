import os
import time
import requests

# Load the target URL from the environment
TARGET_URL = os.environ.get("TARGET_URL", "http://192.168.100.1")
# The scoreboard API endpoint on the vulnerable web server
SCOREBOARD_URL = f"{TARGET_URL}/api/submit_flag"

TEAM_NAME = os.environ.get("TEAM_NAME", "AI_Agent_01")
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

def run_agent():
    print(f"[{TEAM_NAME}] Starting attack on: {TARGET_URL}")
    while True:
        try:
            # 1. INITIAL RECONNAISSANCE 
            # In a real scenario, you would pass the response to an LLM to decide the next step
            response = requests.get(TARGET_URL)
            print(f"[{TEAM_NAME}] Visited {TARGET_URL} | Status: {response.status_code}")
            
            # Example: Agent finds a flag in the HTML or by triggering an exploit
            # If the LLM successfully parses a flag out of the content:
            
            # 2. SUBMIT FLAG
            # flag_found = "FLAG{example_flag}"
            # print(f"[{TEAM_NAME}] Found flag! Submitting...")
            # submit_res = requests.post(SCOREBOARD_URL, json={
            #     "team_name": TEAM_NAME,
            #     "flag": flag_found
            # })
            # print(f"Scoreboard Response: {submit_res.json()}")

        except Exception as e:
            print(f"[{TEAM_NAME}] Error connecting to target: {e}")
        
        # Delay for the autonomous loop (prevents spamming the server too hard initially)
        time.sleep(5)

if __name__ == "__main__":
    run_agent()
