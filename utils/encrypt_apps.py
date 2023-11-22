from .run_app_playbook import run_app_playbook


def main():
    run_app_playbook("playbooks/encrypt_apps.yml")


if __name__ == '__main__':
    main()
