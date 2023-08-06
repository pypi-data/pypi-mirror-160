import re
import sys
import base64
import hashlib
import getpass
import argparse
from cryptography.fernet import Fernet

def make_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="what do you want to do?", choices=["encrypt", "decrypt", "run"])
    parser.add_argument("input", help="the file to open")
    parser.add_argument("-o", "--output", help="the desired output path")
    args, unknown = parser.parse_known_args()
    output = args.output or "output"
    return args.mode, args.input, output, unknown


def get_password_and_count():
    password = getpass.getpass("Password: ")
    end = re.search(r"-(\d+)$", password)
    count = 1
    if end: count = int(end[1])
    return password, count


def encrypt_script(input_path, output_path, password, count):
    with open(input_path) as f:
        code = f.read()
    password_hash = hashlib.md5(password.encode()).hexdigest()[:32].encode()
    key = base64.urlsafe_b64encode(password_hash)
    fernet = Fernet(key)
    encrypted = code.encode()
    for _ in range(count):
        encrypted = fernet.encrypt(encrypted)
    encrypted = bytes([256 - x for x in encrypted])
    with open(output_path, "wb") as f:
        f.write(encrypted)


def get_code(input_path, password, count):
    key = base64.urlsafe_b64encode(
        hashlib.md5(password.encode()).hexdigest()[:32].encode()
    )
    fernet = Fernet(key)
    with open(input_path, "rb") as f:
        blob = f.read()
    blob = bytes([256 - x for x in blob])
    code = blob
    for _ in range(count):
        code = fernet.decrypt(code)
    return code.decode()


def decrypt_script(input_path, output_path, password, count):
    code = get_code(input_path, password, count)
    with open(output_path, "w") as f:
        f.write(code)


def decrypt_and_run(input_path, password, count, unknown_args):
    code = get_code(input_path, password, count)
    sys.argv[1:] = unknown_args
    exec(code, globals())


def main():
    mode, input_path, output_path, unknown_args = make_arg_parser()
    password, count = get_password_and_count()
    if mode == "encrypt":
        encrypt_script(input_path, output_path, password, count)
    elif mode == "decrypt":
        decrypt_script(input_path, output_path, password, count)
    else:
        decrypt_and_run(input_path, password, count, unknown_args)


if __name__ == "__main__":
    main()