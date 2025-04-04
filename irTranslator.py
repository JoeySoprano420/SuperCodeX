class IRTranslator:
    def __init__(self, ast):
        self.ast = ast
        self.assembly_code = []
    
    def translate(self):
        for statement in self.ast:
            if statement[0] == 'DEFINE':
                self.translate_define(statement)
            elif statement[0] == 'EXIT':
                self.translate_exit(statement)
        return '\n'.join(self.assembly_code)
    
    def translate_define(self, statement):
        func_name, args, body = statement[1], statement[2], statement[3]
        self.assembly_code.append(f"global {func_name}")
        self.assembly_code.append(f"{func_name}:")
        for stmt in body:
            self.assembly_code.append(self.translate_statement(stmt))
    
    def translate_exit(self, statement):
        self.assembly_code.append("mov rax, 60")
        self.assembly_code.append("xor rdi, rdi")
        self.assembly_code.append("syscall")
    
    def translate_statement(self, statement):
        if statement[0] == 'EXIT':
            return "mov rax, 60\nxor rdi, rdi\nsyscall"
        else:
            return ""
