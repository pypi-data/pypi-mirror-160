# -*- coding: utf-8 -*-

# flake8: noqa

# import getpass
# import os

# from pygitm.constants import PYGITM_PASSWORD, PYGITM_SSH_KEY, PYGITM_USERNAME


# class SSHAuth:
#     def __init__(self, ssh_key: str) -> None:
#         self._ssh_key = ssh_key

#     @classmethod
#     def from_identity_file(cls, filepath: str) -> None:
#         with open(filepath) as f:
#             ssh_key = f.read()
#         return cls(ssh_key)

#     @classmethod
#     def from_env(cls, ssh_key_var: str = PYGITM_SSH_KEY) -> None:
#         return cls(os.environ[ssh_key_var])


# class HTTPSAuth:
#     def __init__(self, username: str, password: str) -> None:
#         self._username = username
#         self._password = password

#     @classmethod
#     def from_prompt(cls) -> None:
#         return cls(getpass.getuser(), getpass.getpass())

#     @classmethod
#     def from_env(
#         cls, username_var: str = PYGITM_USERNAME, password_var: str = PYGITM_PASSWORD
#     ) -> None:
#         return cls(os.environ[username_var], os.environ[password_var])
