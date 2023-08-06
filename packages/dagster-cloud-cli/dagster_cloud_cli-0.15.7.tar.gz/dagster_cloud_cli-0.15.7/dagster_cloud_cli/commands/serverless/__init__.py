import json
import os
import subprocess
import sys
import time
from pathlib import Path

import dagster._check as check
from dagster.utils import file_relative_path
from dagster_cloud_cli import gql, ui
from dagster_cloud_cli.config_utils import (
    DEPLOYMENT_CLI_OPTIONS,
    dagster_cloud_options,
    get_location_document,
)
from dagster_cloud_cli.utils import add_options
from typer import Argument, Option, Typer

app = Typer(help="Build and deploy your code to Dagster Cloud.")

_DOCKER_OPTIONS = {
    "source_directory": (
        Path,
        Option(
            None,
            "--source-directory",
            "-d",
            exists=False,
            help="Source directory to build for the image.",
        ),
    ),
}


@app.command(name="build", short_help="Build image for Dagster Cloud code location.")
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(_DOCKER_OPTIONS)
def build_command(
    api_token: str,
    url: str,
    agent_timeout: int,  # pylint: disable=unused-argument
    image: str = Argument(None, help="Image name."),
    **kwargs,
):
    """Add or update the image for a repository location in the workspace."""
    dockerfile_template = file_relative_path(__file__, "Dockerfile")
    source_directory = str(kwargs.get("source_directory"))

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]

        cmd = [
            "docker",
            "build",
            source_directory,
            "--file",
            dockerfile_template,
            "-t",
            f"{registry}:{image}",
        ]
        retval = subprocess.call(cmd, stderr=sys.stderr, stdout=sys.stdout)
        if retval == 0:
            ui.print(f"Built image {registry}:{image}")


@app.command(
    name="upload",
    short_help="Upload the built code location image to Dagster Cloud's image repository.",
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def upload_command(
    api_token: str,
    url: str,
    agent_timeout: int,  # pylint: disable=unused-argument
    image: str = Argument(None, help="Image name."),
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a repository location in the workspace."""

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]
        aws_access_key_id = ecr_info["aws_access_key_id"]
        aws_secret_access_key = ecr_info["aws_secret_access_key"]

        subprocess.check_output(
            f"aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin {registry}",
            env={
                **os.environ,
                "AWS_ACCESS_KEY_ID": aws_access_key_id,
                "AWS_SECRET_ACCESS_KEY": aws_secret_access_key,
            },
            shell=True,
        )
        retval = subprocess.call(
            ["docker", "push", f"{registry}:{image}"], stderr=sys.stderr, stdout=sys.stdout
        )
        if retval == 0:
            ui.print(f"Pushed image {image} to {registry}")


@app.command(
    name="registry-info",
    short_help="Get registry information and temporary creds for an image repository",
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def registry_info_command(
    api_token: str,
    url: str,
    agent_timeout: int,  # pylint: disable=unused-argument
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a repository location in the workspace."""

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry_url = ecr_info["registry_url"]
        aws_access_key_id = ecr_info["aws_access_key_id"]
        aws_secret_access_key = ecr_info["aws_secret_access_key"]
        aws_region = ecr_info.get("aws_region", "us-west-2")
        ui.print(
            f"""REGISTRY_URL={registry_url}
AWS_ACCESS_KEY_ID={aws_access_key_id}
AWS_SECRET_ACCESS_KEY={aws_secret_access_key}
AWS_DEFAULT_REGION={aws_region}
"""
        )


@app.command(
    name="deploy",
    short_help="Add a code location from a local directory",
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(DEPLOYMENT_CLI_OPTIONS)
def deploy_command(
    api_token: str,
    url: str,
    agent_timeout: int,  # pylint: disable=unused-argument
    source_directory: Path = Argument(".", help="Source directory."),
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a repository location in the workspace."""

    location_name = kwargs.get("location_name")
    if not location_name:
        raise ui.error(
            "No location name provided. You must specify the location name as an argument."
        )

    if not source_directory:
        raise ui.error("No source directory provided.")

    dockerfile_template = file_relative_path(__file__, "Dockerfile")

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]
        aws_access_key_id = ecr_info["aws_access_key_id"]
        aws_secret_access_key = ecr_info["aws_secret_access_key"]

        image = kwargs.get("image")
        if not image:
            image = location_name

        image_tag = f"{registry}:{image}"
        location_args = {**kwargs, "image": image_tag}
        location_document = get_location_document(location_name, location_args)

        cmd = [
            "docker",
            "build",
            str(source_directory),
            "--file",
            dockerfile_template,
            "-t",
            image_tag,
        ]
        retval = subprocess.call(cmd, stderr=sys.stderr, stdout=sys.stdout)
        if retval != 0:
            return

        subprocess.check_output(
            f"aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin {registry}",
            env={
                **os.environ,
                "AWS_ACCESS_KEY_ID": aws_access_key_id,
                "AWS_SECRET_ACCESS_KEY": aws_secret_access_key,
            },
            shell=True,
        )
        retval = subprocess.call(
            ["docker", "push", image_tag], stderr=sys.stderr, stdout=sys.stdout
        )
        if retval != 0:
            return

        gql.add_or_update_code_location(client, location_document)
        ui.print(f"Added or updated location {location_name}.")
