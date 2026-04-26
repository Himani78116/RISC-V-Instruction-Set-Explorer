from collections import defaultdict

# imports the http library and json version
import requests  
import json

url = "https://raw.githubusercontent.com/rpsene/riscv-extensions-landscape/main/src/instr_dict.json"

#Downloads whatever lives at the URL
r = requests.get(url)

#Shows http response code for the request
print(r.status_code)

#Converts JSON response into python dict and show parsed data. if parsing fails, prints raw response
try:
    data = r.json()
    print(data)
except Exception:
    print(r.text)

extension_instructions = defaultdict(list)

multi_ext_instructions = {}

instruction_sources = {}

for instr_name, instr_data in data.items():
    tags = instr_data.get('extension_tags',[])

    if not tags:
        print(f"Warning: Instruction '{instr_name}' has no extension tags")

        continue
    normalized_tags = [tag.lower().strip() for tag in tags]

    for tag in normalized_tags:
        extension_instructions[tag].append(instr_name)

        if instr_name in instruction_sources:
            instruction_sources[instr_name].append(normalized_tags)

        else:
            instruction_sources[instr_name] = [normalized_tags]

            if len(normalized_tags) > 1:
                multi_ext_instructions[instr_name] = normalized_tags

    print("EXTENSION SUMMARY")
    print("-" * 50)
    print("Extension    | Count | Example")
    print("-" * 50)

    sorted_extensions = sorted(extension_instructions.items(),
                               key = lambda x: len(x[1]), reverse = True)
    
    for ext, instr_list in sorted_extensions:
        count = len(instr_list)
        example = instr_list[0]
        print(f"{ext:<12} | {count:4} instructions | e.g. {example}")

    print("" + "="*50)

    print(f"Instructions belonging to multiple extensions({len(multi_ext_instructions.items)}found):")
    for instr, tags in sorted(multi_ext_instructions.items()):
        print(f" {instr}: {','.join(tags)}")

    duplicates = {instr: sources for instr, sources in instruction_sources.items()
                  if len(set(tuple(sorted(tags)) for tags in sources)) > 1}
    if duplicates:
        print(f"Duplicate instructions found({len(duplicates)}):")
        for instr, sources in duplicates.items():
            print(f" {instr}:{sources}")

    else:
        print("No duplicate instructions found.") 


total_instructions = len(data)
total_extensions = len(extension_instructions)
print(f"SUMMARY STATS:")
print(f"Total instructions:{total_instructions}")
print(f"Total extensions:{total_extensions}")
print(f"Multi-extension instructions:{len(multi_ext_instructions)}")