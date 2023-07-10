import os
import time
import clipboard

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

def sudo_command(command):
    output = os.popen("sudo -S %s" % command).read()
    time.sleep(0.1)
    return output

def color_print(text:str, color:str):
    print(f"{color}{text}{bcolors.ENDC}")

def port_func(command):
    command_line = command.split()

    if len(command_line) == 1 or command_line[1] == "-a":
        result = sudo_command("sudo lsof -PiTCP -sTCP:LISTEN")
        color_print(result, bcolors.OKGREEN)

    elif command_line[1] == "-p":
        try:
            port = int(command_line[2])
            result = sudo_command(f"sudo lsof -i :{port}")
            color_print(result, bcolors.OKGREEN)

        except Exception as e:
            color_print(str(e), bcolors.FAIL)

    elif command_line[1] == "-k":
        try:
            pid = int(command_line[2])
            result = sudo_command(f"sudo kill -9 {pid}")
            color_print(result, bcolors.OKGREEN)

        except Exception as e:
            color_print(str(e), bcolors.FAIL)

def ec2_func(command):
    output = 'ssh -i "tommyfuture-jack.pem" ubuntu@ec2-43-200-109-147.ap-northeast-2.compute.amazonaws.com'
    clipboard.copy(output)
    color_print("copied: " + output, bcolors.OKGREEN)

def apitgateway_func(command):
    command_line = command.split()

    if len(command_line) == 1:
        output = "wss://3wzvptpx15.execute-api.ap-northeast-2.amazonaws.com/av_stage"
        clipboard.copy(output)
        color_print("copied: " + output, bcolors.OKGREEN)

    elif command_line[1] == "-wscat":
        output = "wscat -c wss://3wzvptpx15.execute-api.ap-northeast-2.amazonaws.com/av_stage"
        clipboard.copy(output)
        color_print("copied: " + output, bcolors.OKGREEN)

    elif command_line[1] == "-c":
        output = "https://3wzvptpx15.execute-api.ap-northeast-2.amazonaws.com/av_stage/@connections"
        clipboard.copy(output)
        color_print("copied: " + output, bcolors.OKGREEN)

def clear_func(command):
    os.system("clear")

def help_func(command):
    descript = f"""
    {bcolors.HEADER}[PORT]{bcolors.ENDC}
    port : Find a every port.
    port -a : Find a every port.
    port -p [PORT] : Find specific port usage.
    port -k [PID] : Kill port by using specific PID.
    
    {bcolors.HEADER}[EC2]{bcolors.ENDC}
    ec2 : Copy connect command.
    
    {bcolors.HEADER}[API Gateway]{bcolors.ENDC}
    api : Copy socket connection url.
    api -wscat : Copy wscat socket connection command.
    api -c : Copy Connection url for admin. (IAM Certificated)
    
    {bcolors.HEADER}[etc]{bcolors.ENDC}
    help : explain command.
    clear : clear terminal.
    """
    print(descript)

func_dict = {
    "port" : port_func,
    "ec2" : ec2_func,
    "api" : apitgateway_func,
    "help" : help_func,
    "clear" : clear_func
}

while True:
    command = input("helper> ")

    if command == "":
        continue

    elif command.lower() == "exit":
        break

    elif command.split()[0] in func_dict.keys():
        function = func_dict[command.split()[0]]
        function(command)

    else:
        color_print(f"`{command}` command doesn't exist.", bcolors.FAIL)
