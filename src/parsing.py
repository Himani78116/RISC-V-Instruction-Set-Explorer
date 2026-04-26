from collections import defaultdict
import requests


def fetch_instruction_data():

    url="https://raw.githubusercontent.com/rpsene/riscv-extensions-landscape/main/src/instr_dict.json"

    return requests.get(url).json()


def group_by_extension(data):

    extension_instructions=defaultdict(list)
    multi_ext_instructions={}

    for instr_name, instr_data in data.items():

        tags=instr_data.get("extension",[])

        if isinstance(tags,str):
            tags=[tags]

        if not tags:
            continue

        for tag in tags:
            extension_instructions[tag].append(instr_name)

        if len(tags)>1:
            multi_ext_instructions[instr_name]=tags

    return extension_instructions, multi_ext_instructions


def main():

    data=fetch_instruction_data()

    extension_instructions, multi_ext_instructions = group_by_extension(data)


    print("Extension | Count | Example")
    print("-"*40)

    for ext, instructions in sorted(
        extension_instructions.items(),
        key=lambda x: len(x[1]),
        reverse=True):

        print(
          f"{ext} | {len(instructions)} instructions | e.g. {instructions[0]}"
        )


    print("\nInstructions in multiple extensions:")

    for instr,tags in multi_ext_instructions.items():
        print(instr,tags)


if __name__=="__main__":
    main()