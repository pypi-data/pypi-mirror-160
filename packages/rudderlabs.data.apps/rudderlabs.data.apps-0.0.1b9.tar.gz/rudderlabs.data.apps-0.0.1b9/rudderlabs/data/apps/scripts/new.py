#!/usr/bin/env python

import os

import click
import jinja2

from ..constants import SAGEMAKER_CONTAINER_PATH_MAIN
from ..log import get_logger, verbosity_option
from . import rudderlabs

logger = get_logger(__name__)


def render_template(jenv, template, context, output_dir):
    """Renders a template to the output directory using specific context.

    Args:

      jenv: The Jinja2 environment to use for rendering the template
      template: The path to the template, from the internal templates directory
      context: A dictionary with the context to render the template with
      output_dir: Where to save the output
    """

    output_file = os.path.join(output_dir, template)

    basedir = os.path.dirname(output_file)
    if not os.path.exists(basedir):
        logger.info("mkdir %s", basedir)
        os.makedirs(basedir)

    with open(output_file, "wt") as f:
        logger.info("rendering %s", output_file)
        T = jenv.get_template(template)
        f.write(T.render(**context))


@click.command(
    epilog="""
Examples:

  1. Generates a new project for Bob:

     $ rlabs new -vv data-apps-leadscoring -t "Lead Scoring" -o ~/Projects

     $ rlabs new -vv <project> -t <title> -o <output_dir>
"""
)
@click.argument("project")
@click.option(
    "-t",
    "--title",
    show_default=True,
    default="New project",
    help="This entry defines the project title. "
    "The project title should be a few words only.  It will appear "
    "at the description of your project and as the title of your "
    "documentation",
)
@click.option(
    "-o",
    "--output-dir",
    help="Directory where to dump the new " "project - must not exist",
)
@verbosity_option()
@rudderlabs.raise_on_error
def new(project, title, output_dir):
    """Creates a folder structure for a new rudderlabs data apps project."""

    # the jinja context defines the substitutions to be performed
    context = dict(
        project=project,
        title=title,
        sagemaker_container_path=SAGEMAKER_CONTAINER_PATH_MAIN,
    )

    # copy the whole template structure and de-templatize the needed files
    if output_dir is None:
        output_dir = os.path.join(os.path.realpath(os.curdir), project)

    logger.info(
        "Creating structure for %s at directory %s", project, output_dir
    )

    if os.path.exists(output_dir):
        raise IOError(
            "The project directory %s already exists - cannot "
            "overwrite!" % output_dir
        )

    logger.info("mkdir %s", output_dir)
    os.makedirs(output_dir)

    # base jinja2 engine
    env = jinja2.Environment(
        loader=jinja2.PackageLoader("rudderlabs.data.apps", "templates"),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )

    # other standard files
    simple = [
        ".gitignore",
        ".gitattributes",
        "config/sample.yaml",
        "credentials_template.yaml",
        "data/.gitignore",
        "notebooks/sample_notebook.ipynb",
        "README.md",
        "requirements.txt",
        "conda/environment.yaml",
        "data_loader.py",
        "pipelines/sample_pipeline.yaml",
        "run_notebook_wrapper.py",
    ]
    for k in simple:
        render_template(env, k, context, output_dir)

    logger.info(f"Creating base {project} structure in {output_dir}")
