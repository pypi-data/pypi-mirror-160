#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from datetime import datetime

import click

from sagemaker.processing import ProcessingInput, ProcessingOutput

from ..aws.processing import get_sklearn_processor
from ..aws.s3 import download_s3_directory, get_s3_resource, parse_s3_path
from ..config import read_yaml
from ..constants import (
    EXCLUDE_FILES,
    EXCLUDE_FOLDERS,
    SAGEMAKER_CONTAINER_PATH_MAIN,
)
from ..log import get_logger, verbosity_option
from ..utils.zip import zip_directory
from . import rudderlabs

logger = get_logger(__name__)


def run_pipeline_step(
    pipeline_step_info: dict,
    creds: dict,
    instance_type: str,
    job_id: str,
    repository_path: str,
    exclude_folders: list,
    exclude_files: list,
) -> None:
    """Runs given pipeline step in sci-kit learn processor in amazon sagemaker

    Args:
        pipeline_step_info: Pipeline step information
        creds: AWS credentials
        instance_type: Instance type to use for the sagemaker job
        job_id: all the outputs will be saved under the folder with this name
        repository_path: Path to the repository
        exclude_folders: List of directories to be excluded from the zip
        exclude_files: List of files to be excluded from the zip

    Returns:
        None: None
    """
    # Get sklearn processor
    logger.info(f"Pipeline step: {pipeline_step_info['name']}")
    job_name = (
        f"{pipeline_step_info['name']}-{pipeline_step_info['job_suffix']}"
    )
    sklearn_processor = get_sklearn_processor(creds, instance_type, job_name)

    # Prepare source code and input data
    logger.info("Preparing source code")
    source_code_zip_path = zip_directory(
        repository_path,
        exclude_folders=exclude_folders,
        exclude_files=exclude_files,
    )

    input_data_zip_path = None
    input_data_path = pipeline_step_info.get("input_data").replace(
        "<job_id>", f"{job_id}"
    )

    # check input data path weather it is relative to repository or absolute
    if not os.path.isabs(input_data_path):
        input_data_path = os.path.join(repository_path, input_data_path)

    if os.path.exists(input_data_path):
        logger.info("Preparing input data")
        input_data_zip_path = zip_directory(input_data_path)

    sagemaker_input_data_path = os.path.join(
        SAGEMAKER_CONTAINER_PATH_MAIN, "data"
    )
    sagemaker_output_data_path = os.path.join(
        SAGEMAKER_CONTAINER_PATH_MAIN, "output"
    )
    sagemaker_code_path = os.path.join(SAGEMAKER_CONTAINER_PATH_MAIN, "code")
    sagemaker_req_path = os.path.join(
        SAGEMAKER_CONTAINER_PATH_MAIN, "requirements"
    )

    local_req_path = os.path.join(repository_path, "requirements.txt")

    # script parameters
    script_params = {f"{k}": v for k, v in pipeline_step_info["params"].items()}

    # Pass job id to the pipeline script as a parameter
    script_params["--job-id"] = job_id

    if input_data_zip_path is not None:
        script_params["--input-data-zip"] = os.path.join(
            sagemaker_input_data_path, os.path.basename(input_data_zip_path)
        )

    script_params["--output-data-path"] = sagemaker_output_data_path
    script_params["--source-code-zip"] = os.path.join(
        sagemaker_code_path, os.path.basename(source_code_zip_path)
    )
    script_params["--requirements-path"] = os.path.join(
        sagemaker_req_path, "requirements.txt"
    )

    arguments = []
    for k, v in script_params.items():
        arguments.append(f"{k}")
        arguments.append(f"{v}")

    logger.info(f"Arguments: {arguments}")
    inputs = [
        ProcessingInput(
            source=source_code_zip_path, destination=sagemaker_code_path
        ),
        ProcessingInput(source=local_req_path, destination=sagemaker_req_path),
    ]

    if input_data_zip_path:
        inputs.append(
            ProcessingInput(
                source=input_data_zip_path,
                destination=sagemaker_input_data_path,
            )
        )

    sklearn_processor.run(
        code=pipeline_step_info["code"],
        inputs=inputs,
        outputs=[
            ProcessingOutput(
                output_name=pipeline_step_info["name"],
                source=sagemaker_output_data_path,
            )
        ],
        arguments=arguments,
    )

    s3_bucket = None
    process_job_output_path = None

    if instance_type != "local":
        s3_bucket = creds["s3Bucket"]
        process_job_output_path = (
            f"{sklearn_processor.latest_job.job_name}/output/output-1/{job_id}"
        )
    else:
        preprocessing_job_description = sklearn_processor.jobs[-1].describe()
        output_config = preprocessing_job_description["ProcessingOutputConfig"]

        for output in output_config["Outputs"]:
            if output["OutputName"] != pipeline_step_info["name"]:
                continue

            output_s3_url = output["S3Output"]["S3Uri"]
            s3_bucket, process_job_output_path = parse_s3_path(output_s3_url)

    logger.info(f"S3 bucket: {s3_bucket}")
    logger.info(f"Process job output path: {process_job_output_path}")

    if s3_bucket is not None and process_job_output_path is not None:
        local_output_path = os.path.join(
            repository_path, pipeline_step_info["output_path"], f"{job_id}"
        )
        # Downloading model output files into local
        s3_resource = get_s3_resource(creds)

        download_s3_directory(
            s3_resource, s3_bucket, process_job_output_path, local_output_path
        )


@click.command(
    epilog="""
    The command to run given notebookes in the pipeline.

    Examples:

        $ rlabs aws run-pipeline --pipeline-config-file pipeline.yaml --credentials-file credentials.yaml --repository-path /path/to/repository --instance-type ml.t3.xlarge --job-id my-job-id

        $ rlabs aws run-pipeline -p pipeline.yaml -c credentials.yaml -r /path/to/repository -i local -j my-job-id
    """
)
@click.option(
    "-j",
    "--job-id",
    default=None,
    help="Job id to be used for the pipeline, used to store output files in S3/local",
)
@click.option(
    "-c",
    "--credentials-file",
    type=click.Path(exists=True, readable=True, resolve_path=True),
    show_default=True,
    default=os.path.join(os.path.realpath(os.curdir), "credentials.yaml"),
)
@click.option(
    "-i",
    "--instance-type",
    default="ml.t3.xlarge",
    show_default=True,
    help="The instance type to use for the amazon sagemaker notebook instance.",
)
@click.option(
    "-p",
    "--pipeline-config-file",
    type=click.Path(exists=True, readable=True, resolve_path=True),
    help="The pipeline config file to use.",
)
@click.option(
    "-r",
    "--repository-path",
    default=os.path.realpath(os.curdir),
    show_default=True,
    type=click.Path(exists=True, readable=True, resolve_path=True),
    help="The repository path to use.",
)
@verbosity_option()
@rudderlabs.raise_on_error
def run_pipeline(
    job_id: str,
    credentials_file: click.Path,
    instance_type: str,
    pipeline_config_file: click.Path,
    repository_path: click.Path,
) -> None:

    logger.info("Running pipeline")
    logger.info("credentials_file: %s", credentials_file)
    logger.info("Instance type: %s", instance_type)

    if job_id is None:
        job_id = int(datetime.now().timestamp())

    # Load the pipeline config file
    pipeline_config = read_yaml(pipeline_config_file)
    logger.info("Pipeline config: %s", pipeline_config)

    # Load the credentials file
    config = read_yaml(credentials_file)
    exclude_files = pipeline_config.get("exclude", [])
    print(exclude_files)

    # Runing pipeline
    for pipeline_step in pipeline_config["pipeline"]:
        logger.info("Running pipeline step: %s", pipeline_step["name"])

        exclude_folders = (
            pipeline_step.get("exclude_folders", []) + EXCLUDE_FOLDERS
        )
        exclude_files = pipeline_step.get("exclude_files", []) + EXCLUDE_FILES

        run_pipeline_step(
            pipeline_step_info=pipeline_step,
            creds=config,
            instance_type=instance_type,
            job_id=job_id,
            repository_path=repository_path,
            exclude_folders=exclude_folders,
            exclude_files=exclude_files,
        )
