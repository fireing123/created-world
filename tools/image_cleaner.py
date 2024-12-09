
import os
import subprocess

base_path = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(base_path):
    png_files = [f for f in files if f.endswith(".png")]
    if png_files: 
        try:
            subprocess.run(["mogrify", "*.png"], cwd=root, check=True)
            print(f"mogrify executed in {root}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing mogrify in {root}: {e}")