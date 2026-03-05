import subprocess

def run_secure_tunnel():
    
    #  command as a list of arguments
    result = subprocess.run(["ngrok", "http", "9999"])

    #  check the return code (0 usually means success)
    if result.returncode == 0:
        print("Command executed successfully")
    else:
        print(f"Command failed with return code {result.returncode}")

if __name__=="__main__":
    run_secure_tunnel()