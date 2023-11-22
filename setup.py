from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'hcloud>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'configure_apps = utils.configure_apps',
            'encrypt_apps = utils.encrypt_apps',
            'ssh-env = utils.ssh_env:main',
        ],
    },
)