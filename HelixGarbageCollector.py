class HelixicalGC:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
    
    def collect_garbage(self):
        for var_name in list(self.memory_manager.variables):
            if self.memory_manager.variables[var_name]['location'] is None:
                self.memory_manager.deallocate(var_name)
