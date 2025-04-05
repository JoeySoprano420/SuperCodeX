class FunctionEngine:
    def __init__(self):
        self.functions = {}
    
    def define_function(self, func_name, body):
        self.functions[func_name] = body
    
    def execute_function(self, func_name):
        if func_name in self.functions:
            self.functions[func_name]()
