#include <string.h>
#include <stdio.h>


void gadjets() {
  asm("pop %rax ; ret");
  asm("pop %rdi ; ret");
  asm("pop %rsi ; ret");
  asm("pop %rdx ; ret");
  asm("pop %rcx ; ret");
  asm("pop %r8 ; ret");
  asm("pop %r9 ; ret");
  asm("pop %r15 ;ret");
  asm("mov %rax,%rdi ; ret");
  asm("xor %rax,(%rdi); ret");
  asm("xor %rax,(%r15) ; ret");
  asm("syscall ; ret");
  asm("pop %r10; ret");
}

void beba(char* s1,char* s2,int n) {
  if(!strncmp(s1,s2,n)){
    puts("Perfecto!");
  }
  else {  
    puts("You lose!");
  }
}

size_t pop_rax = (long)gadjets+8;
size_t pop_rdi = (long)gadjets+8+2;
size_t pop_rsi = (long)gadjets+8+4;
size_t pop_rdx = (long)gadjets+8+6;
size_t pop_rcx = (long)gadjets+8+8;
size_t pop_r8 = (long)gadjets+8+10;
size_t pop_r9 = (long)gadjets+8+13;
size_t pop_r15 = (long)gadjets+8+16;
size_t mov_rdi_rax = (long)gadjets+8+19;
size_t xor_qrdi_rax = (long)gadjets+8+23;
size_t xor_qr15_rax = (long)gadjets+8+27;
size_t syscall = (long)gadjets+8+31;
size_t pop_r10 = (long)gadjets+8+34;


int idx = 0;

int main() {
  size_t buf[5000]= {0x500000};
  buf[idx++] = pop_rax;
  buf[idx++] = 0x9;
  buf[idx++] = pop_rdi;
  buf[idx++] = 0x1000000;
  buf[idx++] = pop_rsi;
  buf[idx++] = 0x4000;
  buf[idx++] = pop_rdx;
  buf[idx++] = 0x7;
  buf[idx++] = pop_r10;
  buf[idx++] = 32 | 2;
  buf[idx++] = pop_r8;
  buf[idx++] = -1;
  buf[idx++] = pop_r9;
  buf[idx++] = 0;
  buf[idx++] = syscall;
  // mmap memory
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1001000;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x6520657361656c50;
  buf[idx++] = xor_qr15_rax;
  // write string to memory
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1001008;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x756f79207265746e;
  buf[idx++] = xor_qr15_rax;
  //
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1001010;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x0a2167616c662072;
  buf[idx++] = xor_qr15_rax;
  //
  buf[idx++] = pop_rax;
  buf[idx++] = 1;
  buf[idx++] = pop_rdi;
  buf[idx++] = 1;
  buf[idx++] = pop_rsi;
  buf[idx++] = 0x1001000;
  buf[idx++] = pop_rdx;
  buf[idx++] = 23;
  buf[idx++] = syscall;
  // write to stdin
  buf[idx++] = pop_rax;
  buf[idx++] = 0;
  buf[idx++] = pop_rdi;
  buf[idx++] = 0;
  buf[idx++] = pop_rsi;
  buf[idx++] = 0x1000000;
  buf[idx++] = pop_rdx;
  buf[idx++] = 31;
  buf[idx++] = syscall;
  //
  //xor and check
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1002000;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x5f6c6579735f6179;
  buf[idx++] = xor_qr15_rax;
  // write string to memory
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1002008;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x5f6f6e5f61646564;
  buf[idx++] = xor_qr15_rax;
  //
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1002010;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x745f656e5f6f7465;
  buf[idx++] = xor_qr15_rax;
  //
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1002018;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x6f6e68636f;
  buf[idx++] = xor_qr15_rax;
  //xor and check
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1000000;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x2f031702143e0d1f;
  buf[idx++] = xor_qr15_rax;
  //xor and check
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1000008;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x29300a3a1205073b;
  buf[idx++] = xor_qr15_rax;
  //xor and check
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1000010;
  buf[idx++] = pop_rax;
  buf[idx++] = 0xe2500312c062b08;
  buf[idx++] = xor_qr15_rax;
  //xor and check
  buf[idx++] = pop_r15;
  buf[idx++] = 0x1000018;
  buf[idx++] = pop_rax;
  buf[idx++] = 0x1214121915;
  buf[idx++] = xor_qr15_rax;
  buf[idx++] = pop_rdi;
  buf[idx++] = 0x1000000;
  buf[idx++] = pop_rsi;
  buf[idx++] = 0x1002000;
  buf[idx++] = pop_rdx;
  buf[idx++] = 29;
  buf[idx++] = beba;
  asm("ret"); 
}
