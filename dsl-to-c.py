import sys
import shlex
import astCommands


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

nodes = []
for s in output:
    tokens = shlex.split(s)
    cmd = tokens[0]
    args = tokens[1:]
    print(cmd, args)
    node = astCommands.COMMANDS_DSL[cmd](*args)
    nodes.append(node)    

for node in nodes:
    c_code += "\t" + node.emit_c() + "\n"

c_code += "}"
print(c_code)
with open(sys.argv[1].replace("dsl", "c++"), "w") as f:
    f.write(c_code)
