from kubernetes import client, config
from kubernetes.client import ApiClient
from rich.console import Console

from pbsrollout.k8s_utils import import_kube_config


def check_cluster_ready(name: str, path: str, api_client: ApiClient) -> bool:
    console = Console()
    print(f'\tChecking cluster {name}')
    daemonset_check = check_only_one_daemonset(path)
    if daemonset_check:
        console.print("\t\t[grey66]only one daemonset[/grey66]:................. [bold green]SUCCESS")
    else:
        console.print("\t\t[grey66]only one daemonset[/grey66]:................. [bold red]FAILED")
        return False

    return True


def check_only_one_daemonset(path: str) -> bool:
    config.load_kube_config(config_file=import_kube_config(path + '/.k8s-assets/kubeconfig'))

    v1 = client.AppsV1Api()
    daemonsets = v1.list_namespaced_daemon_set(namespace='api')
    if len(daemonsets.items) == 0:
        print('\t\terror: no daemonset found')
        return False

    pbs_daemonsets = []
    for d in daemonsets.items:
        name = d.metadata.name
        if name.startswith('pbs-prod'):
            pbs_daemonsets.append(name)
    if len(pbs_daemonsets) == 1:
        return True
    else:
        print(f'\t\terror: more than 1 daemonset found: {pbs_daemonsets}')
        return False
