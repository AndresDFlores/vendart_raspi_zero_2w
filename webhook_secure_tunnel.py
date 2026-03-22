import subprocess
import time


def run_secure_tunnel(stop_event):
    """
    Runs `ngrok http 9999` in a subprocess and stops cleanly when stop_event is set.
    """

    print("[secure_tunnel] Starting ngrok tunnel...")

    # Start ngrok as a long-running subprocess
    process = subprocess.Popen(
        ["ngrok", "http", "9999"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    try:
        # Loop until stop_event is set
        while not stop_event.is_set():

            # Read ngrok output without blocking forever
            line = process.stdout.readline()
            if line:
                print("[secure_tunnel]", line.strip())

            # Small sleep so the loop stays responsive
            time.sleep(0.1)

            # If ngrok crashed, break out so we can exit
            if process.poll() is not None:
                print("[secure_tunnel] ngrok exited unexpectedly")
                break

    finally:
        print("[secure_tunnel] Stopping ngrok...")

        if process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                print("[secure_tunnel] Force killing ngrok...")
                process.kill()

        print("[secure_tunnel] ngrok stopped cleanly.")