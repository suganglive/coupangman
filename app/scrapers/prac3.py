import re

# Define the pattern to include both letters and numbers
pattern = re.compile(r"^(?=.*[A-Z])(?=.*[0-9])[A-Z0-9]+(-[A-Z0-9]+)?$")

# List of strings to filter
strings = [
    "T8602KUG",
    "TCL",
    "85C845",
    "QLED",
    "KQ85QC67AFXKR",
    "UHD",
    "KQ85QNB85AFXKR",
    "L55M8-A2KR",
    "L50M8-A2KR",
    "TCL",
    "50P735",
]

# Filter the strings
filtered_strings = [s for s in strings if pattern.match(s)]

for s in strings:
    if pattern.match(s):
        lst.append(s)
print(filtered_strings)
