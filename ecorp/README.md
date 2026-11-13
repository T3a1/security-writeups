# ecorp

Write-ups for ECorp, a capture-the-flag scenario from Epitech set in a
fictional company. Starting as an intern, each flag gives access to the next
step: exploiting C binaries with memory bugs, then the company's intranet.

Each write-up explains the vulnerable code, why it is exploitable and the
exploit used. Some come with a Python proof of concept (`poc_*.py`).

| Step | Class | Summary |
|------|-------|---------|
| [first-flag](first-flag.md) | Recon | Initial access found on the company flyer |
| [Ov3rwr1t3](stack/Ov3rwr1t3.md) | Stack | `gets()` overflows a password buffer into the next field of the struct |
| [Ov3rfl0w](stack/Ov3rfl0w.md) | Stack | Overflow of a fixed-size buffer that overwrites a `failsafe` flag |
| [Envir0n](stack/Envir0n.md) | Stack | Same struct overwrite, while getting past a partial `strncmp` hash check |
| [C4llb4ck](stack/C4llb4ck.md) | Stack | Overwrite of a function pointer stored next to a buffer |
| [R3t2func](stack/R3t2func.md) | Stack | Return address overwrite to jump to a hidden function |
| [St4ck0v3rfl0w](stack/St4ck0v3rfl0w.md) | Stack | Stack overflow in a root-owned binary called through a wrapper script |
| [H34pfun](heap/H34pfun.md) | Heap | Heap overflow in a 32-bit TCP chatbot service |
| [H34pGOt](heap/H34pGOt.md) | Heap | Heap overflow used to overwrite a GOT entry |
| [Ov3rf0rm4t](format/Ov3rf0rm4t.md) | Format string | Format string bug in a CGI binary called by the intranet API |
| [T1nk3r1ng](format/T1nk3r1ng.md) | Web | Command injection through unescaped GET parameters passed to `shell_exec` |

Tools: GDB, `objdump`, Python (`pwntools`).
