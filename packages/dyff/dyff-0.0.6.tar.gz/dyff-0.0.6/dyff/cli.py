"""Command line utility for uploading file contents to Google bucket.
Providing you already have a user account, the CLI will take your
user account identifier, password, and path and then wrap up the path
and send it to the Google Bucket.
"""
import tarfile
import tempfile

import click
import requests
from decouple import config

GET_UPLOAD_URL_URL = config(
    "GET_UPLOAD_URL_URL",
    default="https://us-central1-dyff-354017.cloudfunctions.net/getUploadUrl",
)


def login(username, password):
    """Login to the dyff servers"""

    print(
        "In the future this will actually produce credentials to be posted to the server"
    )
    print(f"Getting: {GET_UPLOAD_URL_URL}")
    r = requests.get(
        GET_UPLOAD_URL_URL, params={"email": username, "password": password}
    )
    print(r.json())
    return r.json()


def upload_files(username, password, path):
    """Upload files to the server after authenticating."""
    upload_url = login(username, password)["url"]
    headers = {"content-type": "application/octet-stream"}

    with tempfile.TemporaryFile(suffix=".tar.bz2") as f:
        with tarfile.open(fileobj=f, mode="w:bz2") as tar:
            tar.add(path)
        f.flush()
        f.seek(0)

        print(f"Putting {path} to Dyff servers...")
        response = requests.put(
            upload_url,
            data=f,
            verify=False,
            headers=headers,
        )
        print(response.text)
        return


@click.group()
@click.version_option()
def cli_main():
    pass


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=False)
def upload(path, username, password):
    click.echo("upload: %s" % path)
    click.echo("username: %s" % username)
    click.echo("password: %s" % password)
    upload_files(username, password, path)


cli_main.add_command(upload)

if __name__ == "__main__":
    cli_main()
