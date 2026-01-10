import sys
import shlex
import astCommands
import astNodes

def parse_cpp_statement(s):
    tokens = shlex.split(s.replace("(", " ").replace(")", " ").replace(",", " "), posix=False)
    cmd = tokens[0]
    args = tokens[1:]
    # assume that if it starts with type, and has opening curly brace, its a function
    if cmd in astCommands.ALLOWED_VARIABLE_TYPES and "{" in args:
        # args.insert(0, cmd)
        # cmd = "func"
        raise NotImplementedError("Function support has been removed due to not having a way to use return values at the moment")
    elif cmd in astCommands.ALLOWED_VARIABLE_TYPES:
        args.insert(0, cmd) # add type as argument
        cmd = "var"
    try:
        node = astCommands.COMMANDS_C[cmd](*args)
    except KeyError:
        node = astNodes.Call(*tokens)
    return node

def parse_dsl_statement(s):
    tokens = shlex.split(s.replace("(", " ").replace(")", " ").replace(",", " "), posix=False)
    cmd = tokens[0]
    args = tokens[1:]
    node = astCommands.COMMANDS_DSL[cmd](*args)
    return node


if "cpp" in sys.argv[1]:
    target="dsl"
    start="cpp"
else:
    target="cpp"
    start="dsl"

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

#c_code = "void " + sys.argv[1].split(".")[0] + "() {\n"
output_code = ""
nodes = []
for s in output:
    if target == "cpp":
        node = parse_dsl_statement(s)
    else:
        node = parse_cpp_statement(s)
    nodes.append(node)

block_level = 0
for node in nodes:
    if target == "cpp":
        f = node.emit_c
    else:
        f = node.emit_dsl
    if isinstance(node, astNodes.Proc):
        block_level += 1
        output_code += "   " * (block_level - 1) + f() + "\n"
    elif isinstance(node, astNodes.Func):
        block_level += 1
        output_code += "   " * (block_level - 1) + f() + "\n"
    elif isinstance(node, astNodes.End):
        block_level -= 1
        output_code += "   " * block_level + f() + "\n"
    else:
        output_code += "   " * block_level + f() + "\n"
    
print(output_code)
with open(sys.argv[1].replace(start, target), "w") as f:
    f.write(output_code)
