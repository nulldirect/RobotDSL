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
    def __init__(self, velocity: float):
        self.vel = velocity
    def emit_c(self):
        return f"Drivetrain.setTurnVelocity({self.vel});"
    def emit_dsl(self):
        return f"turn_vel {self.vel};"
    
class DriveVel(ASTNode):
    def __init__(self, velocity: float):
        self.vel = velocity
    def emit_c(self):
        return f"Drivetrain.setDriveVelocity({self.vel});"
    def emit_dsl(self):
        return f"drive_vel {self.vel};"


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