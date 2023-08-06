import subprocess

try:
    output = subprocess.check_output(["powercfg", "-getactivescheme"])
except Exception as err___:
    print("Fatal Error 0x357")

if b"381b4222-f694-41f0-9685-ff5bb260df2e" in output:
    win_pp = "381b4222-f694-41f0-9685-ff5bb260df2e"
    gotten = True
elif b"8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c" in output:
    win_pp = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    gotten = True
elif b"a1841308-3541-4fab-bc81-f71556f20b4a" in output:
    win_pp = "a1841308-3541-4fab-bc81-f71556f20b4a"
    gotten = True
elif b"e9a42b02-d5df-448d-aa00-03f14749eb61" in output:
    win_pp = "e9a42b02-d5df-448d-aa00-03f14749eb61"
    gotten = True
else:
    gotten = False