class ASTNode:
    def emit_c(self) -> str:
        raise NotImplementedError
    def emit_dsl(self) -> str:
        raise NotImplementedError
    
class SpecialASTNode(ASTNode):
    def emit_c(self) -> str:
        return super().emit_c()
    def emit_dsl(self) -> str:
        return super().emit_dsl()
    def parse_c(self, *parameters) -> list[str]:
        return list(parameters)
    def parse_dsl(self, *parameters) -> list[str]:
        params = list(parameters)
        if ':' in params:
            params.remove(':')
        return params

class Rst(ASTNode):
    def __init__(self, degrees: float, unit: str):
        self.deg = degrees
        self.unit = unit
    def emit_c(self):
        return f"Drivetrain.setHeading({self.deg}, {self.unit});"
    def emit_dsl(self):
        return f"rst {self.deg} {self.unit};"
    
class Turn(ASTNode):
    def __init__(self, degrees: float):
        self.deg = degrees
    def emit_c(self):
        return f"TurnToAngle({self.deg});"
    def emit_dsl(self):
        return f"turn {self.deg};"
    
class Drive(ASTNode):
    def __init__(self, distance: float):
        self.dist = distance
    def emit_c(self):
        return f"DriveForIN({self.dist});"
    def emit_dsl(self):
        return f"drive {self.dist};"
        
class Slp(ASTNode):
    def __init__(self, seconds: float):
        self.time = seconds
    def emit_c(self):
        return f"sleep({self.time});"
    def emit_dsl(self):
        return f"slp {self.time};"
    
class TurnVel(ASTNode):
    def __init__(self, velocity: float, unit: str):
        self.vel = velocity
        self.unit = unit
    def emit_c(self):
        return f"Drivetrain.setTurnVelocity({self.vel}, {self.unit});"
    def emit_dsl(self):
        return f"turn_vel {self.vel} {self.unit};"
    
class DriveVel(ASTNode):
    def __init__(self, velocity: float, unit: str):
        self.vel = velocity
        self.unit = unit
    def emit_c(self):
        return f"Drivetrain.setDriveVelocity({self.vel}, {self.unit});"
    def emit_dsl(self):
        return f"drive_vel {self.vel} {self.unit};"
    
class End(ASTNode):
    def emit_c(self):
        return "}"
    def emit_dsl(self):
        return "end;"

class Ret(ASTNode):
    def __init__(self, value: str = ""):
        self.value = value
    def emit_c(self):
        if self.value != "":
            return f"return {self.value};"
        else:
            return "return;"
    def emit_dsl(self):
        if self.value != "":
            return f"ret {self.value};"
        else:
            return "ret;"

# Special AST Nodes are nodes that require complex parsing in order to use
class Call(SpecialASTNode):
    def __init__(self, *parameters):
        self.params = parameters
    def emit_c(self):
        call_params = self.parse_dsl(*self.params)
        func = call_params[0]
        params = call_params[1:]
        return f"{func}({", ".join(params)});"
    def emit_dsl(self):
        call_params = self.parse_c(*self.params)
        func = call_params[0]
        f_params = call_params[1:]
        if f_params != []:
            return f"call {func} : {",".join(f_params)};"
        else:
            return f"call {func};"
        
    def parse_dsl(self, *parameters) -> list[str]:
        return super().parse_dsl(*parameters)
    
    def parse_c(self, *parameters) -> list[str]:
        return list(parameters)
        
class Var(SpecialASTNode):
    def __init__(self, *parameters):
        self.params = parameters

    def emit_c(self):
        parsed = self.parse_dsl(*self.params)
        v_type = parsed[0]
        name = parsed[1]
        value = parsed[2]
        return f"{v_type} {name} = {value};"
    
    def emit_dsl(self):
        parsed = self.parse_c(*self.params)
        v_type = parsed[0]
        name = parsed[1]
        value = parsed[2]
        return f"var {v_type} : {name} {value};"
    
    def parse_dsl(self, *parameters) -> list[str]:
        return super().parse_dsl(*parameters)
    
    def parse_c(self, *parameters) -> list[str]:
        params = list(parameters)
        if "=" in params:
            params.remove("=")
        return params
    
class Include(SpecialASTNode):
    def __init__(self, filename: str, type: str = ""):
        self.filename = filename
        self.type = type
    def emit_c(self):
        if self.type == "sys":
            return f'#include <{self.filename}>'
        elif self.type == "user":
            return f'#include "{self.filename}"'
        else:
            # technically not possible, if the code is correct, but the linter is yelling at me for no return
            return f'#include "{self.filename}"'
    def emit_dsl(self):
        params = self.parse_c(self.filename, self.type)
        filename = params[0]
        t = params[1]
        return f'inc {filename} {t};'
    def parse_dsl(self, *parameters) -> list[str]:
        return super().parse_dsl(*parameters)
    def parse_c(self, *parameters) -> list[str]:
        # determine if system or user include
        params = list(parameters)
        if params[0].startswith("<") and params[0].endswith(">"):
            filename = params[0][1:-1]
            return [filename, "sys"]
        elif params[0].startswith('"') and params[0].endswith('"'):
            filename = params[0][1:-1]
            return [filename, "user"]
        else:
            return [params[0], "user"]

class Proc(SpecialASTNode):
    def __init__(self, *parameters):
        self.name = parameters[0]
        self.params = parameters[1:] # skip the name
    def emit_c(self):
        # parse
        params = self.parse_dsl(*self.params)
        return f"void {self.name}({", ".join(params)}) {{"
    def emit_dsl(self):
        params = self.parse_c(*self.params)
        if len(params) > 0:
            return f"proc {self.name} : ({", ".join(params)});"
        else:
            return f"proc {self.name};"
    def parse_c(self, *parameters) -> list[str]:
        params = list(parameters) 
        params.remove('{')

        # take pairs of type and value ex double x , double y
        type_name_pairs = []
        for i in range(0, len(params), 2):
            type_name_pairs.append(f"{params[i]} {params[i+1]}")
        return type_name_pairs
    def parse_dsl(self, *parameters) -> list[str]:
        params = list(parameters) 
        # take pairs of type and value ex double x , double y
        if ":" in params:
            params.remove(":")
            type_name_pairs = []
            for i in range(0, len(params), 2):
                type_name_pairs.append(f"{params[i]} {params[i+1]}")
            return type_name_pairs
        return []

class Func(SpecialASTNode):
    def __init__(self, *parameters):
        self.params = parameters # skip the name
    def emit_c(self):
        # parse
        params = self.parse_dsl(*self.params)
        return f"{self.return_type} {self.name}({", ".join(params)}) {{"
    def emit_dsl(self):
        params = self.parse_c(*self.params)
        return f"func {self.name} : ({", ".join(params)}) -> {self.return_type};"
    def parse_c(self, *parameters) -> list[str]:
        params = list(parameters)
        self.return_type = params[0]
        self.name = params[1]
        type_name_pairs = []
        for i in range(2, len(params)-1, 2):
            type_name_pairs.append(f"{params[i]} {params[i+1]}")
        return type_name_pairs
    def parse_dsl(self, *parameters) -> list[str]:
        params = list(parameters) 
        # take pairs of type and value ex double x , double y
        if ":" in params:
            params.remove(":")
            params.remove("->")
            type_name_pairs = []
            for i in range(1, len(params)-1, 2):
                type_name_pairs.append(f"{params[i]} {params[i+1]}")
            # last param is return type
            self.return_type = params[-1]
            self.name = params[0]
            return type_name_pairs
        raise NotImplementedError # don't allow functions with no parameters, but with return type because