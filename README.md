# RISC-V Instruction Set Explorer

## Features

- Tier 1 instruction parsing
- Tier 2 ISA manual cross-reference
- Tier 3 extension overlap graph

## Install

pip install requests networkx matplotlib

## Run

python src/parsing.py  
python src/crossref.py  
python src/extension_graph.py

## Run Tests

python -m unittest tests.test_parser

## Sample Output

40 matched
36 JSON only
0 manual only

## Assumptions

- rv_zba normalized to zba
- composite tags split on "_"
- vector profile aliases excluded