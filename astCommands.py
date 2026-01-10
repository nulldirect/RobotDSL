import astNodes
COMMANDS_DSL = {
    "rst": astNodes.Rst,
    "turn": astNodes.Turn,
    "drive": astNodes.Drive,
    "slp": astNodes.Slp,
    "turn_vel": astNodes.TurnVel,
    "drive_vel": astNodes.DriveVel,
    "call": astNodes.Call,
    "var": astNodes.Var,
    "inc": astNodes.Include,
    "proc": astNodes.Proc,
    "end": astNodes.End,
    "use": astNodes.Use,
    "func": astNodes.NotImpl,
    "ret": astNodes.NotImpl,
}
COMMANDS_C = {
    "Drivetrain.setHeading": astNodes.Rst,
    "TurnToAngle": astNodes.Turn,
    "DriveForIN": astNodes.Drive,
    "sleep": astNodes.Slp,
    "Drivetrain.setTurnVelocity": astNodes.TurnVel,
    "Drivetrain.setDriveVelocity": astNodes.DriveVel,
    "var": astNodes.Var, # special one, it manually looks for this and sets the command when parsing
    "#include": astNodes.Include,
    "void": astNodes.Proc, # won't work in some cases like void pointers, but idc rn
    "}": astNodes.End, # used for both endproc and endfunc
    "using": astNodes.Use,
    "return": astNodes.NotImpl,
    "func": astNodes.NotImpl,
    "for": astNodes.NotImpl,
    "while": astNodes.NotImpl,
    "if": astNodes.NotImpl,
}
ALLOWED_VARIABLE_TYPES = ["bool", "int", "float", "auto", "double", "char"]
