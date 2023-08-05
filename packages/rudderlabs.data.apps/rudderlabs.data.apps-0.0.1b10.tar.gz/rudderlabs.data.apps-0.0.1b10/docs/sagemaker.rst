.. vim: set fileencoding=utf-8 :

==============================
 Running Pipeline on SageMaker
==============================

Running The Pipeline
--------------------

The pipeline steps can be run as a SageMaker processing job on the cloud or locally using SageMaker pre-built docker containers.

flow diagram

      .. image:: img/run_pipeline_flow_diagram.png
         :align: center
         :alt: flow diagram
         :height: 371px

Use following command to run the pipeline

.. code-block:: bash

   #Example 1: Run the pipeline on the cloud
   $ rlabs aws run-pipeline --pipeline-config-file pipeline.yaml --credentials-file credentials.yaml --repository-path /path/to/repository --instance-type ml.t3.xlarge --job-id my-job-id

   #Example 2: Run the pipeline locally
   $ rlabs aws run-pipeline -p pipeline.yaml -c credentials.yaml -r /path/to/repository -i local -j 345687

.. note::

   Params:
      - ``-p``, ``--pipeline-config-file``: path to the pipeline configuration file
      - ``-c``, ``--credentials-file``: path to the credentials file (contains AWS credentials, data warehouse credentials)
      - ``-r``, ``--repository-path``: path to the data apps project repository
      - ``-i``, ``--instance-type``: instance type to run the pipeline [default: ml.t3.xlarge]
      - ``-j``, ``--job-id``: job id to run the pipeline, will get used while storing output or reading input inbetween processing pipeline steps


Arguments for the Pipeline Script
---------------------------------

There are few manditory arguments that the pipeline script needs to implement. these arguments will get passed from ``run-pipeline`` script

.. note::

   Mandatory arguments:
      - ``-j``, ``--job-id``: Job id to be passed to notebook execution script  [required]
      - ``-i``, ``--input-data-zip``: Path to input data zip file
      - ``-o``, ``--output-data-path``: Path to the output directory  [required]
      - ``-s``, ``--source-code-zip``: Path to the source code zip file  [required]
      - ``-r``, ``--requirements-path``: Path to the requirements.txt file  [required]

.. warning::

   Without these arguments, the pipeline script will fail to run.
