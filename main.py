import paramiko
import configparser
import subprocess

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

def ping(host):
    command = ['ping', '-c', '1', host]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        if result.returncode == 0:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        return False

def calculate_power_usage(watt_percent, config):
    ups_wattage = config.get("Power", "ups_wattage")

    try:
        if watt_percent > 0:
            watts_used = ups_wattage * (watt_percent * 0.01) # convert to percentage
            return watts_used
        if watt_percent == 0:
            if ping(config.get("Power", "host_to_check_1")): # machine is online
                return config.get("Power", "no_value_power_usage_if_checks_pass")
            elif ping(config.get("Power", "host_to_check_2")): # machine is online
                return config.get("Power", "no_value_power_usage_if_checks_pass")
            else: # both machines offline
                return config.get("Power", "no_value_power_usage")
        else:
            print("Error: Unexpected output wattage")
            return None
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    config = parse_config_file("config.ini")

    host = config.get("Connection", "host")
    username = config.get("Connection", "username")
    password = config.get("Connection", "password")
    
    output = ssh_connection(host, username, password)

    output_wattage_percent = parse_detstatus(output)

    result = calculate_power_usage(output_wattage_percent, config)
    print(result)
