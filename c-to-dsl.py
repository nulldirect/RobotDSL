import sys


class RstFromC:
    def __init__(self, degrees: float):
        self.deg = degrees
    def __str__(self):
        return f"rst {self.deg};\n"
class TurnFromC:
    def __init__(self, degrees: float):
        self.deg = degrees
    def __str__(self):
        return f"turn {self.deg};\n"
class DriveFromC:
    def __init__(self, distance: float):
        self.dist = distance
    def __str__(self):
        return f"drive {self.dist};\n"
class CallFromC:
    def __init__(self, function: callable, *parameters):
        self.func = function
        self.params = parameters
    def __str__(self):
        if self.params[0] != "":
            param_str = ""
            for i, p in enumerate(self.params):
                param_str += p
                if i != len(self.params) - 1:
                    param_str += ","
            return f"call {self.func} : {param_str};\n"
        else:
            return f"call {self.func};\n"
class SlpFromC:
    def __init__(self, seconds: float):
        self.time = seconds
    def __str__(self):
        return f"slp {self.time};\n"
class TurnVelFromC:
    def __init__(self, velocity: float):
        self.vel = velocity
    def __str__(self):
        return f"turn_vel {self.vel};\n"
class DriveVelFromC:
    def __init__(self, velocity: float):
        self.vel = velocity
    def __str__(self):
        return f"drive_vel {self.vel};\n"
class VarFromC:
    def __init__(self, var_type: str, name: str, value: str):
        self.name = name
        self.v_type = var_type
        self.value = value
    def __str__(self):
        return f"var {self.v_type} : {self.name} {self.value};\n"



with open(sys.argv[1], "r") as f:
    c_code = f.read()

statements = c_code.split(";")

# remove comments
output = []
for s in statements:
    for l in s.split("\n"):
        cleaned = l.strip()
        if not cleaned.startswith("//") and cleaned:
            output.append(l)

dsl_code = ""
variable_types = ["int", "double", "float", "bool"]
# tokenize
for s in output:
    if "{" in s or "}" in s:
        continue
    statement_sequence = s.strip().split("(")
    function = statement_sequence[0]
    # nothing
    variable_statement = [0]
    if len(statement_sequence) > 1:
        arguments = [i.strip() for i in statement_sequence[1].replace(")", "").split(",")]
    else:
        variable_statement = function.split(" ")
    f = None
    if function == "Drivetrain.setHeading":
        f = RstFromC(arguments[0])
    elif function == "TurnToAngle":
        f = TurnFromC(*arguments)
    elif function == "DriveForIN":
        f = DriveFromC(*arguments)
    elif function == "sleep":
        f = SlpFromC(*arguments)
    elif function == "Drivetrain.setTurnVelocity":
        f = TurnVelFromC(arguments[0])
    elif function == "Drivetrain.setDriveVelocity":
        f = DriveVelFromC(arguments[0])
    elif variable_statement[0] in variable_types:
        variable_statement.remove('=');
        f = VarFromC(*variable_statement)
    else:
        f = CallFromC(function, *arguments);
    dsl_code += str(f)
    f = None

print(dsl_code)
with open(sys.argv[1].replace("c", "dsl"), "w") as f:
    f.write(dsl_code)
