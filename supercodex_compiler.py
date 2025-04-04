import sys
import subprocess

# SuperCodeX Compiler: Parses, Translates, Assembles, Links

# Mapping SuperCodeX Commands to x64 Assembly
SCDX_TO_ASM = {
    "PRINT": "mov rax, 0x2000004\nmov rdi, 1\nsyscall",
    "ADD": "add rax, rbx",
    "SUB": "sub rax, rbx",
    "MUL": "imul rax, rbx",
    "DIV": "idiv rbx",
}

# Compiler Function
def compile_supercodex(input_file):
    asm_code = [
        "section .text",
        "global _start",
        "_start:"
    ]

    with open(input_file, "r") as file:
        for line in file:
            tokens = line.strip().split()
            if not tokens:
                continue
            
            command = tokens[0].upper()
            if command in SCDX_TO_ASM:
                asm_code.append(SCDX_TO_ASM[command])
            elif command == "EXIT":
                asm_code.append("mov rax, 60\nxor rdi, rdi\nsyscall")
            else:
                print(f"Unknown command: {command}")
    
    asm_code.append("mov rax, 60\nxor rdi, rdi\nsyscall")  # Ensure program exits
    asm_code = "\n".join(asm_code)

    # Write Assembly File
    with open("output.asm", "w") as asm_file:
        asm_file.write(asm_code)
    
    print("[+] Assembly Code Generated: output.asm")

    # Assemble using NASM
    subprocess.run(["nasm", "-f", "win64", "output.asm", "-o", "output.obj"], check=True)

    # Link using LLD
    subprocess.run(["lld-link", "/subsystem:console", "/entry:_start", "output.obj"], check=True)

    print("[+] Compilation Successful! Run output.exe")

# Run Compiler
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python supercodex_compiler.py <input.scdx>")
        sys.exit(1)
    
    compile_supercodex(sys.argv[1])
