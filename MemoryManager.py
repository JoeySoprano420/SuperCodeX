class MemoryManager:
    def __init__(self):
        self.variables = {}
    
    def allocate(self, var_name, size):
        self.variables[var_name] = {'size': size, 'location': None}
    
    def deallocate(self, var_name):
        if var_name in self.variables:
            del self.variables[var_name]
