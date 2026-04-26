from collections import defaultdict
import requests

url = "https://raw.githubusercontent.com/rpsene/riscv-extensions-landscape/main/src/instr_dict.json"

data = requests.get(url).json()

extension_instructions = defaultdict(list)
multi_ext_instructions = {}

for instr_name, instr_data in data.items():

    tags = instr_data.get("extension", [])   # verify key!

    if isinstance(tags, str):
        tags = [tags]

    if not tags:
        continue

    for tag in tags:
        extension_instructions[tag].append(instr_name)

    if len(tags) > 1:
        multi_ext_instructions[instr_name] = tags


print("Extension | Count | Example")
print("-"*40)

for ext, instructions in sorted(
        extension_instructions.items(),
        key=lambda x: len(x[1]),
        reverse=True):

    print(f"{ext} | {len(instructions)} instructions | e.g. {instructions[0]}")

print("\nInstructions in multiple extensions:")
for instr, tags in multi_ext_instructions.items():
    print(instr, tags)