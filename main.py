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
    shell.send(bytes("help\n", 'ascii'))       # important to send a newline with the command otherwise its still waiting
    result = shell.recv(65535).decode('ascii') # empty the buffer again so I can capture the output

    print("buffer contains:")
    print(
    str(result)
    )

    print("What I actually wanted was:")
    print(
    str(result).split("\r\napc>help\r\n")[-1]
    )

    client.close()

if __name__ == "__main__":
    config = parse_config_file("config.ini")

    host = config.get("Connection", "host")
    username = config.get("Connection", "username")
    password = config.get("Connection", "password")
    ssh_connection(host, username, password)