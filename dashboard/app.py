from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Ensure we are in the correct directory to run the script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/containers")
def get_containers():
    try:
        # Get docker containers
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.ID}}|{{.Names}}|{{.Status}}|{{.Ports}}"], 
            capture_output=True, text=True, check=True
        )
        containers = []
        if result.stdout.strip():
            for line in result.stdout.strip().split("\n"):
                parts = line.split("|")
                if len(parts) >= 4:
                    containers.append({
                        "id": parts[0],
                        "name": parts[1],
                        "status": parts[2],
                        "ports": parts[3]
                    })
        return jsonify(containers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/start", methods=["POST"])
def start_everything():
    try:
        # Run the start script asynchronously or wait for it
        script_path = os.path.join(BASE_DIR, "run_all.sh")
        # Run with default 5 bots or a specified number if it's there
        bots_count = request.json.get("bots", "5")
        
        subprocess.run(["bash", script_path, str(bots_count)], cwd=BASE_DIR, check=True)
        return jsonify({"status": "success", "message": "Containers started successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/stop", methods=["POST"])
def stop_everything():
    try:
        # Hardcoding the stop command for these stacks to keep it clean
        subprocess.run(["docker", "compose", "-f", "user_docker/user-docker-compose.yml", "down"], cwd=BASE_DIR)
        subprocess.run(["docker", "compose", "-f", "bot_docker/bot1-docker-compose.yml", "down"], cwd=BASE_DIR)
        return jsonify({"status": "success", "message": "Containers stopped successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
