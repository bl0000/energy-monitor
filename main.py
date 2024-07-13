import paramiko
import configparser

def parse_config_file(filename):
    config = configparser.ConfigParser()
    try:
        config.read(filename)
        return config
    except Exception as e:
        print("Error occurred while parsing", filename, "\nError:", e)
        return None

def ssh_connection(hostname, username, password):

    command_output = ""

    # based on https://community.se.com/t5/APC-UPS-Data-Center-Enterprise/Scripting-SSH-connections-to-NMC-s-take-2/td-p/449384

    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
    hostname,
    username=username,
    password=password,
    allow_agent=False,
    look_for_keys=False
    )

    shell = client.invoke_shell()

    result = shell.recv(65535).decode('ascii') # empty the receive buffer first so the card moves on to its prompt
    shell.send(bytes("detstatus -om\n", 'ascii'))       # important to send a newline with the command otherwise its still waiting
    result = shell.recv(65535).decode('ascii') # empty the buffer again so I can capture the output

    command_output = str(result).split("\r\napc>detstatus -om\r\n")[-1]
    
    print(str(result)) #debug

    client.close()

    return command_output

def parse_detstatus(command_output):
    lines = command_output.split('\n')
    for line in lines:
        if "Output Watts Percent" in line:
            print(line)
            percent_str = line.split(':')[-1].strip()
            try:
                percent_value = float(percent_str.rstrip('%'))
                return percent_value
            except ValueError as e:
                print(e)
                return None
    return None

if __name__ == "__main__":
    config = parse_config_file("config.ini")

    host = config.get("Connection", "host")
    username = config.get("Connection", "username")
    password = config.get("Connection", "password")
    
    output = ssh_connection(host, username, password)

    output_wattage_percent = parse_detstatus(output)


    try:
        print("%:", output_wattage_percent)
        print((output_wattage_percent * 3))
    except:
        print("Fail")    
