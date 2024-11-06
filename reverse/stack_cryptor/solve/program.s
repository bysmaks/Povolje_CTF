start:
	loop1:	
		call get_str_addr
		push [bx]
		push 0x5A
		xor
		pop ex
		mov [bx], ex

		inc ax
		cmp ax, [str_len]
		jle loop1

	mov ax, 0
	loop2:
		call get_str_addr
		push bx
		push 1
		add
		pop cx

		call xor_next
		mov [bx], ex

		call xor_next
		mov [cx], ex

		call xor_next
		mov [bx], ex

		inc ax
		inc ax
		cmp ax, [str_len]
		jl loop2

	print str
	hlt

xor_next:
	push [bx]
	push [cx]
	xor
	pop ex
	ret

get_str_addr:
	push ax
	push str
	add
	pop bx
	ret

str:
	db "sussy_baka", 0

str_len:
	db 9
