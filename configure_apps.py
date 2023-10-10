import argparse
import subprocess


"""
This script is a wrapper around playbooks/configure_apps.yml. It adds args to help
import the dokku_bot.ansible_dokku role without running through all its installation
steps again.

Args:
    inventory_env (str): Specifies the inventory environment ('staging',
        'production', etc.) to be used by the Ansible playbook.
    <ansible_playbook_params> (optional): Any additional parameters that are valid for 
        'ansible-playbook' can be passed here. These will be forwarded directly to the 
        'ansible-playbook' command.

Examples:
    Configure all apps on staging:
    >>> python configure_apps.py staging
    
    Configure supergood-reads app on staging:
    >>> python configure_apps.py staging --tags app=supergood-reads

    Add extra --skip-tags:
    >>> python configure_apps.py staging --skip-tags app=supergood-reads

Explanation:
    We need this script because importing the dokku_bot.ansible_dokku role will run all
    of its dependency roles as well -- even when we tell ansible_dokku to just run its
    dummy init.yml task.

    The additional command line options added by this script will skip most of the
    unnecessary tasks run by ansible_dokku's 2 dependency roles (geerlingguy.docker and
    nginxinc.nginx).
"""
def main():
    parser = argparse.ArgumentParser(description='Wrapper script for ansible-playbook')
    parser.add_argument('env', type=str, help='The server to ssh into')
    parser.add_argument('ansible_args', nargs=argparse.REMAINDER, help='Arguments to pass to ansible-playbook')
    args = parser.parse_args()

    # Tell the playbook that it was invoked by this python script
    invoked_by_script_args = ["--e", "invoked_by_script=true"]

    # See: https://github.com/nginxinc/ansible-role-nginx/blob/main/tasks/main.yml
    nginx_skip_tags = ",".join([
        "nginx_validate",
        "nginx_prerequisites",
        "nginx_key",
        "nginx_enable",
        "nginx_debug_output",
        "nginx_logrotate_config",
        "nginx_install_amplify",
    ])

    # See: https://github.com/geerlingguy/ansible-role-docker
    # Only works on v6.1.0 and higher of geerlingguy.ansible-role-docker.
    docker_role_args = [
        "--e", "docker_add_repo=false",
        "--e", "docker_install_compose_plugin=false", 
    ]

    # Extract skip-tags if they exist in the user input
    user_skip_tags = None
    if '--skip-tags' in args.ansible_args:
        index = args.ansible_args.index('--skip-tags')
        user_skip_tags = args.ansible_args[index + 1]
        del args.ansible_args[index:index + 2]  # Remove existing skip-tags from list

    # Combine skip-tags
    final_skip_tags = nginx_skip_tags
    if user_skip_tags:
        final_skip_tags = f"{nginx_skip_tags},{user_skip_tags}"
    skip_tag_args = ['--skip-tags', final_skip_tags]

    # Construct the final command
    final_command = (
        ['ansible-playbook', "-i", f"inventories/{args.env}", "playbooks/configure_apps.yml"]
        + invoked_by_script_args
        + skip_tag_args
        + docker_role_args
        + args.ansible_args
    )

    # Run the command
    print(" ".join(final_command))
    subprocess.run(final_command)

if __name__ == '__main__':
    main()
