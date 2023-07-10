import clipboard
import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def coloredPrint(text, color=bcolors.ENDC):
    print(f"{color}{text}{bcolors.ENDC}")

def coloredText(text, color=bcolors.ENDC):
    return f"{color}{text}{bcolors.ENDC}"

def commandLine2Query(command):
    div_refer = command.split(" -> ")

    child_side = div_refer[0].split(".")
    child_table = child_side[0]
    child_foreignkey = child_side[1]

    parents_side = div_refer[1].split(".")
    parents_table = parents_side[0]
    parents_foreignkey = parents_side[1]

    constraint = f"FK_{child_table}_TO_{parents_table}"

    result = f"ALTER TABLE {child_table} ADD CONSTRAINT {constraint} FOREIGN KEY ({child_foreignkey}) REFERENCES {parents_table} ({parents_foreignkey});"
    coloredPrint(">> " + result, bcolors.OKCYAN)

    return result


while True:
    coloredPrint("EX) ChildTable.foreignkey -> ParentsTable.foreignkey", bcolors.HEADER)
    command = input("Command: ")

    if(command.lower() == "exit"):
        coloredPrint("Tool Exit...", bcolors.OKGREEN)
        break

    if(command.lower() == "clear"):
        os.system("clear")
        continue

    result = commandLine2Query(command)
    clipboard.copy(result)
    print("\n")

