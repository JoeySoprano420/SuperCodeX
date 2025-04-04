class MemoryManager:
    def __init__(self):
        self.variables = {}
    
    def allocate(self, var_name, size):
        self.variables[var_name] = {'size': size, 'location': None}
    
    def deallocate(self, var_name):
        if var_name in self.variables:
            del self.variables[var_name]

class MemoryManager:
    def __init__(self):
        self.memory = {}

    def allocate(self, var_name, size):
        if var_name not in self.memory:
            self.memory[var_name] = {'size': size, 'address': None}

    def deallocate(self, var_name):
        if var_name in self.memory:
            del self.memory[var_name]

    def cleanup(self):
        for var_name in list(self.memory):
            if self.memory[var_name]['address'] is None:
                self.deallocate(var_name)
