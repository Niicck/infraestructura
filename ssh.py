import argparse
import subprocess
import json


def main() -> None:
    """
    Helper for ssh-ing into hosts within dynamic inventory.
    Example:
        python ssh.py staging
    """
    env = env_from_args()
    inventory_data = fetch_ansible_inventory(env)
    ipv4 = ipv4_from_inventory_data(inventory_data)
    ssh(ipv4)


def env_from_args() -> str:
    parser = argparse.ArgumentParser(description='Prints the provided argument.')
    parser.add_argument('env', type=str, help='The server to ssh into')
    args = parser.parse_args()
    env = args.env
    if not env:
        raise ValueError("Please pass an inventory 'env' value")
    return env


def fetch_ansible_inventory(env: str) -> dict:
    inventory_path = f"inventories/{env}"
    command = ["ansible-inventory", "-i", inventory_path, "--list"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    inventory_data = json.loads(result.stdout)
    return inventory_data


def ipv4_from_inventory_data(inventory_data: dict) -> str:
    first_host_var = list(inventory_data["_meta"]["hostvars"].values())[0]
    ipv4 = first_host_var["ipv4"]
    return ipv4


def ssh(ipv4: str) -> None:
    subprocess.run(["ssh", "-t", f"nick@{ipv4}"])


if __name__ == '__main__':
    main()
