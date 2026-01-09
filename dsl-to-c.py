import sys


class Rst:
    def __init__(self, degrees: float):
        self.deg = degrees
    def __str__(self):
        return f"Drivetrain.setHeading({self.deg}, degrees);\n"
class Turn:
    def __init__(self, degrees: float):
        self.deg = degrees
    def __str__(self):
        return f"TurnToAngle({self.deg});\n"
class Drive:
    def __init__(self, distance: float):
        self.dist = distance
    def __str__(self):
        return f"DriveForIN({self.dist});\n"
class Call:
    def __init__(self, function: callable, *parameters):
        self.func = function
        self.params = parameters
    def __str__(self):
        param_str = ""
        for i, p in enumerate(self.params):
            param_str += p
            if i != len(self.params) - 1:
                param_str += ", "
        return f"{self.func}({param_str});\n"
class Slp:
    def __init__(self, seconds: float):
        self.time = seconds
    def __str__(self):
        return f"sleep({self.time});\n"
class TurnVel:
    def __init__(self, velocity: float):
        self.vel = velocity
    def __str__(self):
        return f"Drivetrain.setTurnVelocity({self.vel});\n"
class DriveVel:
    def __init__(self, velocity: float):
        self.vel = velocity
    def __str__(self):
        return f"Drivetrain.setDriveVelocity({self.vel});\n"
class Var:
    def __init__(self, name: str, var_type: str, value):
        self.name = name
        self.v_type = var_type
        self.value = value
    def __str__(self):
        return f"{self.v_type} {self.name} = {self.value};\n"



with open(sys.argv[1], "r") as f:
    data = f.read()

statements = data.split(";")

# remove comments
output = []
for s in statements:
    for l in s.split("\n"):
        cleaned = l.strip()
        if not cleaned.startswith("//") and cleaned:
            output.append(l)

c_code = "void " + sys.argv[1].split(".")[0] + "() {\n"
# tokenize
for s in output:
    statement_sequence = s.split(" ")
    to_call = statement_sequence[0]
    arguments = statement_sequence[1:]
    f = None
    if to_call == "rst":
        f = Rst(*arguments);
    if to_call == "turn":
        f = Turn(*arguments);
    if to_call == "drive":
        f = Drive(*arguments);
    if to_call == "call":
        function = arguments[0]
        f = Call(function, *arguments[2:]);
    if to_call == "slp":
        f = Slp(*arguments);
    if to_call == "turn_vel":
        f = TurnVel(*arguments);
    if to_call == "drive_vel":
        f = DriveVel(*arguments);
    if to_call == "var":
        f = Var(arguments[2], arguments[0], arguments[3])
    c_code += "\t" + str(f)

c_code += "}"
print(c_code)
with open(sys.argv[1].replace("dsl", "c"), "w") as f:
    f.write(c_code)
