# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from pathlib import Path
import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("--repo", help="path to repo", required=True)
parser.add_argument("--secrets", help="json file with secrets from trufflehog", required=True)
parser.add_argument("--dry_run", help="defaults to true, change to false to remove secrets")
args = parser.parse_args()

def remove_secrets(repo_to_scan):
    secrets = []
    with open(args.secrets, 'r',  encoding="utf-8") as json_file:
        data=json_file.readlines()
        for line in data:
            secrets_json = json.loads(line)
            secrets.append(secrets_json["Raw"].strip())

    json_file.close()
    files = Path(repo_to_scan).rglob('*')
    for file in files:
        if (os.path.isfile(file) and ".git" not in str(file)):
            with open(file, 'r+',  encoding="utf-8") as opened_file:
                for secret in secrets:
                    read_file = opened_file.read()
                    if secret in read_file:
                        if args.dry_run == "false":
                            opened_file.seek(0)
                            clean = read_file.replace(secret, "***REMOVED***")
                            opened_file.write(clean)
                            opened_file.truncate()
                            print(f"Removed sensitive data from file={str(file)}")
                        else:
                            print(f"Found {secret} in file={str(file)} \n")
                    opened_file.seek(0)
                opened_file.close()

if __name__ == "__main__":
    remove_secrets(args.repo)
