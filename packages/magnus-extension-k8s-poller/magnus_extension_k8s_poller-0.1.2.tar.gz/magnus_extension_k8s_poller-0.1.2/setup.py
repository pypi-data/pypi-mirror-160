# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnus_extension_k8s_poller']

package_data = \
{'': ['*']}

install_requires = \
['kubernetes',
 'magnus-extension-datastore-db>=0.1.1,<0.2.0',
 'magnus>=0.3.12,<0.4.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'magnus.executor.BaseExecutor': ['k8s-poller = '
                                  'magnus_extension_k8s_poller.implementation:K8sExecutor'],
 'magnus.integration.BaseIntegration': ['k8s-poller-catalog-file-system = '
                                        'magnus_extension_k8s_poller.integration:K8sPollerComputeCatalogFileSystem',
                                        'k8s-poller-run_log_store-buffered = '
                                        'magnus_extension_k8s_poller.integration:K8sPollerComputeRunLogStoreBuffered',
                                        'k8s-poller-run_log_store-file-system '
                                        '= '
                                        'magnus_extension_k8s_poller.integration:K8sPollerComputeRunLogStoreFileSystem',
                                        'k8s-poller-run_log_store-s3 = '
                                        'magnus_extension_k8s_poller.integration:K8sPollerComputeRunLogStoreS3']}

setup_kwargs = {
    'name': 'magnus-extension-k8s-poller',
    'version': '0.1.2',
    'description': 'Description you want to give',
    'long_description': '# K8s Polling based Execution\n\nThis package is an extension to [magnus](https://github.com/AstraZeneca/magnus-core).\n\n## Provides \n\nProvides functionality to execute a pipeline on K8s cluster.\nThe jobs would be polled to understand the status and traverse the graph.\n\n## Installation instructions\n\n```pip install magnus_extension_k8s_poller```\n\n## Set up required to use the extension\n\nKube Configuration file is required to submit the jobs to the K8s cluster.\n\n## Config parameters\n\nThe full configuration of the AWS secrets manager is:\n\n```yaml\nmode:\n  type: k8s-poller\n  config:\n    config_path: Required and should be pointing to the kube config.\n    polling_time: defaults to 30 secs\n    secrets_to_use: A list of secrets to use that are part of K8s secrets manager.\n    namespace: defaults to "default", the namespace to submit the jobs.\n    job_ttl: maximum job run time.\n    enable_parallel: Defaults to True, submit parallel jobs to the K8s cluster\n    image_name: Required, the full name of the docker image.\n\n```\n\n### **config_path**:\n\nThe path of the config file to interact with the K8s cluster.\n\n### **polling_time**:\n\nDefaults to 30 seconds. The frequency to poll k8s to the job status.\n\n\n### **secrets_to_use**:\n\nA list of secrets to use as part of the Kubernetes cluster.\n\n\n### **namespace**:\n\nThe namespace to submit jobs, defaults to "default".\n\n\n### **job_ttl**:\n\nThe maximum run tile for a job in K8s cluster.\n\n\n### **enable_parallel**:\n\nControls if the jobs should be submitted parallelly to the K8s cluster. Default is True.\n\n\n\n### **image_name**:\n\nThe full name of the docker image to run. Kubernetes cluster should be able to pull the image from the registry.\n\n\n\n\n\n',
    'author': 'Vijay Vammi',
    'author_email': 'vijay.vammi@astrazeneca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AstraZeneca/magnus-extensions/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
