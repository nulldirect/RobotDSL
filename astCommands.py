import astNodes
COMMANDS_DSL = {
    "rst": astNodes.Rst,
    "turn": astNodes.Turn,
    "drive": astNodes.Drive,
    "slp": astNodes.Slp,
    "turn_vel": astNodes.TurnVel,
    "drive_vel": astNodes.DriveVel,
    "call": astNodes.Call,
    "var": astNodes.Var
}
COMMANDS_C = {
    "Drivetrain.setHeading": astNodes.Rst,
    "TurnToAngle": astNodes.Turn,
    "DriveForIN": astNodes.Drive,
    "sleep": astNodes.Slp,
    "Drivetrain.setTurnVelocity": astNodes.TurnVel,
    "Drivetrain.setDriveVelocity": astNodes.DriveVel,
    "var": astNodes.Var # special one, it manually looks for this and sets the command when parsing
}
ALLOWED_VARIABLE_TYPES = ["bool", "int", "float", "auto", "double"]