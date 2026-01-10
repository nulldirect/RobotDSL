import sys
import astCommands
import astNodes

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
# tokenize
for s in output:
    # skip code blocks for now
    if "{" in s or "}" in s: 
        continue
    tokens = s.replace("(", " ").replace(")", " ").replace(",", " ").split()
    cmd = tokens[0]
    args = tokens[1:]
    if cmd in astCommands.ALLOWED_VARIABLE_TYPES:
        args.insert(0, cmd) # add type as argument
        cmd = "var"
    try:
        node = astCommands.COMMANDS_C[cmd](*args)
    except KeyError:
        node = astNodes.Call(*tokens)
    print(node, args)
    dsl_code += node.emit_dsl() + "\n"

print(dsl_code)
# with open(sys.argv[1].replace("c++", "dsl"), "w") as f:
#     f.write(dsl_code)
