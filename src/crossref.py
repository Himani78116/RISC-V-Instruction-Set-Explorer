def normalize(ext):

    ext = ext.lower().strip()

    for prefix in ["rv32_","rv64_","rv_"]:
        if ext.startswith(prefix):
            ext = ext[len(prefix):]

    return ext

def split_extensions(tag):

    parts = tag.lower().split("_")

    prefixes={"rv","rv32","rv64"}

    return [
        p for p in parts
        if p not in prefixes
    ]

def main():
    import requests
    import re

    url = "https://raw.githubusercontent.com/rpsene/riscv-extensions-landscape/main/src/instr_dict.json"

    data = requests.get(url).json()

    json_extensions = set()

    for instr, info in data.items():

        tags = info.get("extension", [])

        if isinstance(tags,str):
            tags=[tags]

        for tag in tags:
            parts = tag.lower().split("_")

            prefixes={"rv","rv32","rv64"}

            for p in parts:
                if p not in prefixes:
                    json_extensions.add(p)



    json_extensions = {
        normalize(x)
        for x in json_extensions
    }

    manual_files = [
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/b-st-ext.adoc",
    # "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/bibliography.adoc",
    # "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/contributors.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/index.adoc",
    # "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/license.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/intro.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/naming.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/riscv-spec.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/rv32.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/rv32e.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/rv64.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/scalar-crypto.adoc",
    # "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/symbols.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/v-st-ext.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/unpriv.adoc",
    "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/vector-crypto.adoc"
    ]

    manual_extensions=set()

    pattern = re.compile(
    r'\b(?:Z[a-zA-Z0-9]+|[IMAFDQCBVH])\b'
    )

    for manual_url in manual_files:

        text = requests.get(manual_url).text

        matches = pattern.findall(text)

        ignore = {
            "zero", "zeros",
            "b", "zb"
        }

        for m in matches:
            candidate = m.lower()

            if candidate in ignore:
                continue

            if candidate in json_extensions:
                manual_extensions.add(candidate)


    matched = json_extensions & manual_extensions

    json_only = json_extensions - manual_extensions

    manual_only = manual_extensions - json_extensions

    profile_prefixes=("zve","zvl")

    manual_only = {
    x for x in manual_only
    if not x.startswith(profile_prefixes)
    }

    print(f"{len(matched)} matched")

    print(f"{len(json_only)} JSON only")

    print(f"{len(manual_only)} manual only")

    print("\nJSON only:")
    for x in sorted(json_only):
        print(x)

    print("\nManual only:")
    for x in sorted(manual_only):
        print(x)

if __name__=="__main__":
    main()