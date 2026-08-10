# ECorp

Write-ups documenting a series of **binary exploitation (pwn) challenges** set in a fictional corporate scenario, "ECorp". Each challenge targets a custom-built C service or binary containing a deliberate memory-safety vulnerability, requiring reverse engineering and exploit development to recover a flag.

## Scope

Challenges are organized by vulnerability class:

- **Stack** — buffer overflows, stack overwrites, function pointer / callback hijacking, environment variable abuse, return-to-function attacks
- **Heap** — heap overflows leading to memory corruption and GOT overwrites
- **Format** — format string vulnerabilities used for memory read/write primitives

## Structure

- Each `.md` file documents one challenge: a **Vulnerability** section explaining the flawed code and how it was identified, followed by a **PoC** section with the Python exploit script used to trigger it.
- Companion `poc_*.py` scripts alongside some write-ups contain the working proof-of-concept exploits.
- `First flag.md` documents the initial access step used to reach the challenge environment.

## Approach

Each challenge was approached through static analysis of the provided C source or disassembly to identify the vulnerable pattern (unsafe functions such as `gets()`/`strcpy()`, missing bounds checks, unsafe `strncmp`/`strcmp` comparisons, format string misuse), followed by exploit development in Python to reliably reproduce the compromise.
