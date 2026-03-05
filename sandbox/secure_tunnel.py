import subprocess


def open_secure_tunnel():
    
    # Command as a list of arguments
    result = subprocess.run(["ngrok", "http", "5000"])


    # Check the return code (0 usually means success)
    if result.returncode == 0:
        print("Command executed successfully")
    else:
        print(f"Command failed with return code {result.returncode}")