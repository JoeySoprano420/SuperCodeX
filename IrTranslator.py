class IRTranslator:
    def __init__(self):
        self.asm_code = []

    def translate(self, ast):
        for stmt in ast:
            if stmt[0] == 'DEFINE':
                self.translate_function(stmt)
            elif stmt[0] == 'EXIT':
                self.translate_exit()
        return '\n'.join(self.asm_code)

    def translate_function(self, stmt):
        func_name, args, body = stmt[1], stmt[2], stmt[3]
        self.asm_code.append(f"global {func_name}")
        self.asm_code.append(f"{func_name}:")
        self.asm_code.append("push rbx")  # save registers
        self.asm_code.append("push rbp")
        for statement in body:
            self.asm_code.append(self.translate_statement(statement))
        self.asm_code.append("pop rbp")  # restore registers
        self.asm_code.append("pop rbx")
        self.asm_code.append("ret")

    def translate_exit(self):
        self.asm_code.append("mov rax, 60")  # Exit syscall
        self.asm_code.append("xor rdi, rdi")  # Return code 0
        self.asm_code.append("syscall")

    def translate_statement(self, stmt):
        if stmt[0] == 'EXIT':
            return "mov rax, 60\nxor rdi, rdi\nsyscall"
        return ""
