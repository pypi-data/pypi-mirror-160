import logging
import time
import shlex
import re
from random import randint
import json

from kubernetes import client
from kubernetes import config as k8s_config
from tqdm import tqdm

from magnus import defaults
from magnus.executor import BaseExecutor
from magnus.nodes import BaseNode
from magnus import utils
from magnus.graph import Graph, search_node_by_internal_name


logger = logging.getLogger(defaults.NAME)


class K8sExecutor(BaseExecutor):
    """

    Example config:
    mode:
      type: k8s-poller
      config:
        config_path: Required and should be pointing to the kube config.
        polling_time: defaults to 30 secs
        secrets_to_use: A list of secrets to use that are part of K8s secrets manager.
        namespace: defaults to "default", the namespace to submit the jobs.
        job_ttl: maximum job run time.
        image_name: Required, the full name of the docker image.
    """
    service_name = 'k8s-poller'
    DEFAULT_POLLING_TIME = 30
    DEFAULT_JOB_TTL = 1000
    DEFAULT_KUBE_NAMESPACE = "default"

    def __init__(self, config):
        super().__init__(config)
        assert 'config_path' in config, "config_path is required for k8s execution"

        # This holds all the jobs that we triggered on K8s
        self.triggered_jobs = {}

    @property
    def config_path(self) -> str:
        """
        Returns the config path of the K8s

        Returns:
            str: Returns the config path of K8s
        """
        return self.config['config_path']

    @property
    def _client(self):
        k8s_config.load_kube_config(config_file=self.config_path)
        return client

    @property
    def polling_time(self):
        """
        Time in seconds to be used for polling k8s job completion
        """
        return self.config.get('polling_time', self.DEFAULT_POLLING_TIME)

    @property
    def secrets_to_use(self):
        """
        Time in seconds to be used for polling k8s job completion
        """
        return self.config.get('secrets_to_use', [])

    @property
    def namespace(self):
        """
        K8s namespace to be used for execution
        """
        return self.config.get('namespace', self.DEFAULT_KUBE_NAMESPACE)

    @property
    def job_ttl(self):
        """
        Max completion Time in seconds for k8s job
        """
        return self.config.get('job_ttl', self.DEFAULT_JOB_TTL)

    def is_parallel_execution(self):
        # Should be False to keep it in a single instance of executor
        return False

    def execute_from_graph(self, node: BaseNode, map_variable: dict = None, **kwargs):
        # Add the step to triggered jobs and call the super to do its job.
        resolved_name = node.resolve_map_placeholders(name=node.internal_name, map_variable=map_variable)
        self.triggered_jobs[resolved_name] = (node, map_variable)

        return super().execute_from_graph(node, map_variable, **kwargs)

    def execute_graph(self, dag: Graph, map_variable: dict = None, **kwargs):
        """
        Trigger the first job of the dag.

        If we are in the parent dag, start polling.
        """
        working_on = dag.get_node_by_name(dag.start_at)
        self.execute_from_graph(working_on, map_variable=map_variable, **kwargs)

        if dag.internal_branch_name is None:
            # We poll here.
            # At every round, look for the step log of the jobs in self.triggered_jobs
            # If the job name does not exist, it is still not started.
            # If the job name reaches an edn state, it finished.
            # IF the job name is processing, it started and waiting to be finished.
            while True:
                for _ in tqdm(range(self.polling_time), desc="waiting..."):
                    time.sleep(1)

                logger.info(self.triggered_jobs)

                for key, value in self.triggered_jobs.copy().items():
                    # Check for status of the logs and traverse only for finished jobs

                    node, m_variable = value
                    step_log = self.run_log_store.get_step_log(
                        node.get_step_log_name(m_variable), self.run_id)
                    logger.info(f'The current node {node.internal_name} is of status {step_log.status}')

                    if step_log.status in [defaults.SUCCESS, defaults.FAIL]:
                        self.traverse(node=node, map_variable=m_variable)
                        del self.triggered_jobs[key]

                run_log = self.run_log_store.get_run_log_by_id(run_id=self.run_id)
                logger.info(f'Found the run log status to be {run_log.status}')

                if run_log.status in [defaults.SUCCESS, defaults.FAIL]:
                    logger.info("We are done with the whole graph, exiting now")
                    logger.info(json.dumps(run_log.dict(), indent=4))
                    break

    def traverse(self, node: BaseNode, map_variable: dict = None, **kwargs):
        """
        Trigger the next node.

        Args:
            node (BaseNode): The current node being worked on
            map_variable (dict, optional): The map variable if the node is part of map. Defaults to None.
        """
        dag_being_run = self.dag

        if node.node_type in ['success', 'fail']:
            # Case where the graph containing the node is simple and has no branches
            if node.internal_branch_name is None:
                logger.info('We reached the end of the graph!')
                return
            # Case where the graph containing the node has branches.
            logger.info(f'We have reached the end of the sub-graph: {node.internal_branch_name}')
            parent_step_name = '.'.join(node.internal_branch_name.split('.')[:-1])
            parent_step, _ = search_node_by_internal_name(dag=self.dag, internal_name=parent_step_name)
            parent_step_log = self.run_log_store.get_step_log(parent_step.internal_name, self.run_id)
            parent_step_log.status = defaults.SUCCESS

            time.sleep(randint(1, 5))  #  To avoid syncs, we wait for a random time between 1 and 5 seconds

            for _, branch in parent_step_log.branches.items():
                if branch.status == defaults.PROCESSING:
                    return
                if branch.status == defaults.FAIL:
                    parent_step_log.status = defaults.FAIL
                    break
            # Point the node to the step that contains the branches
            node = parent_step
            self.run_log_store.add_step_log(parent_step_log, self.run_id)

        if node.internal_branch_name:
            _, dag_being_run = search_node_by_internal_name(self.dag, node.internal_name)

        _, next_node_name = self.get_status_and_next_node_name(node, dag_being_run, map_variable=map_variable)
        next_node = dag_being_run.get_node_by_name(next_node_name)
        self.execute_from_graph(next_node, map_variable=map_variable)

    def get_job_name(self, node: BaseNode, map_variable: dict) -> str:
        """
        Generate a job name based on the node being executed.

        Args:
            node (BaseNode): The node being executed
            map_variable (dict): The map variable if running as a map node

        Returns:
            str: The job name, maximum size of 63 characters
        """
        resolved_name = node.resolve_map_placeholders(name=node.internal_name, map_variable=map_variable)
        return re.sub('[^A-Za-z0-9]+', '-', f'{self.run_id}-{resolved_name}')[:63]

    def trigger_job(self, node: BaseNode, map_variable: dict = None, **kwargs):
        self._submit_k8s_job(node=node, map_variable=map_variable)

    def _submit_k8s_job(self, node: BaseNode, map_variable: dict, **kwargs):  # pylint: disable=unused-argument
        """
        Submit a job to the K8's cluster

        Args:
            node (BaseNode): The node being processed
            map_variable (dict): The map variables if the node is part of a map
        """

        command = utils.get_node_execution_command(self, node, map_variable=map_variable)
        logger.info(f'Triggering a batch job with {command}')

        mode_config = self.resolve_node_config(node)

        image_name = mode_config.get('image_name', None)
        assert image_name is not None, "Complete image_name should be passed for k8s execution"

        resource_configuration = mode_config.get('resource', None)
        # volume_configuration = mode_config.get('volume', None) # TODO Should this also be a list?

        labels = mode_config.get('labels', {})
        labels['job_name'] = self.get_job_name(node=node, map_variable=map_variable)

        k8s_batch = self._client.BatchV1Api()

        secret_configuration = None
        if self.secrets_to_use:
            secret_configuration = []
            for secret_name in self.secrets_to_use:
                k8s_secret_env_source = self._client.V1SecretEnvSource(name=secret_name)
                secret_configuration.append(self._client.V1EnvFromSource(secret_ref=k8s_secret_env_source))

        base_container = self._client.V1Container(
            name=labels['job_name'],
            image=image_name,
            command=shlex.split(command),
            resources=resource_configuration,
            env_from=secret_configuration,
            image_pull_policy="Always"
        )

        pod_volume_template = None
        # if volume_configuration:
        #     pod_volume_template = self.create_pod_volume_template()
        pod_spec = self._client.V1PodSpec(volumes=pod_volume_template,
                                          restart_policy='Never',
                                          containers=[base_container])
        pod_spec.termination_grace_period_seconds = self.job_ttl

        pod_template = self._client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=labels),
            spec=pod_spec)

        job_spec = client.V1JobSpec(template=pod_template, backoff_limit=2)

        job_spec.ttl_seconds_after_finished = 2 * self.polling_time

        job_spec.active_deadline_seconds = self.job_ttl

        job = client.V1Job(
            api_version='batch/v1',
            kind='Job',
            metadata=client.V1ObjectMeta(name=labels['job_name']),
            spec=job_spec)

        k8s_batch.create_namespaced_job(
            body=job,
            namespace=self.namespace)
