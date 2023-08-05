import os
import sys
import time
from subprocess import TimeoutExpired
from typing import Dict

from kubernetes import config
from kubernetes.client import ApiException, ApiClient
from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from shellpython.helpers import Dir
from simple_term_menu import TerminalMenu

from pbsrollout.check_cluster_ready import check_cluster_ready
from pbsrollout.k8s_utils import import_kube_config
from pbsrollout.process_cluster import cutover_service, launch_pods, remove_old_pods, Status
from pbsrollout.utils import notify

CLUSTERS = [
    "aws.us-east-1-eks-23-v3",
    "aws.us-east-1-eks-24-v3",
    "aws.us-east-1-eks-25-v3",
    "aws.us-east-1-eks-26-v3",
    "aws.eu-west-1-eks-16-v3",
    "aws.ap-southeast-2-eks-33-v1",
    "aws.ap-southeast-2-eks-34-v1",
]

DD_BOARD_URL = "https://app.datadoghq.com/dashboard/e23-wak-w5b/prebid?live=true"


def print_help(console):
    mk = """
    Supported features:
    - Check that no other version are present
    - Launch pods + cutover
    - Check the service version + daemonset version
    - Clean pods

    Unsupported features (for now):
    - Rollback + remove old pods
    """

    md = Markdown(mk)
    console.print(md)


def print_welcome(console):
    console.print(
        "[blink underline italic dark_orange3]Better[/blink underline italic dark_orange3] [bold medium_purple3]Rollout[/bold medium_purple3]\n\n",
        justify="center")
    regions = {
        'US': [],
        'EU': [],
        'AUS': [],
    }
    for c in CLUSTERS:
        if 'eu-' in c:
            regions['EU'].append(c)
        elif 'us-' in c:
            regions['US'].append(c)
        elif 'ap-' in c:
            regions['AUS'].append(c)
        else:
            raise RuntimeError(f'unknown region for cluster: {c}')

    user_renderables = [f"[bold]{r}:[/bold]\n" + "\n".join([f"- [slate_blue1]{c}[/slate_blue1]" for c in regions[r]])
                        for r in regions]
    console.print(Columns(user_renderables), justify="center")


def get_cluster_name(c):
    return c.replace('aws.us-east-1-', '').replace('aws.eu-west-1-', '').replace('aws.ap-southeast-2-', '')


def update_prebid_tag(path: str, tag: str):
    path += "/namespace/api/pbs.prod.tag"
    print(f"Updating prebid tag to {tag} in file: {path}")
    with open(path, "w") as f:
        f.write(tag)


def ask_for_tag() -> str:
    tag = input("enter the prebid tag here (you can find it on circleci): ")
    terminal_menu = TerminalMenu(["[y] yes", "[n] no"], title=f"Is this your tag? --{tag}--",
                                 raise_error_on_interrupt=True)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        return tag
    return ask_for_tag()


def ask_to_open_datadog():
    terminal_menu = TerminalMenu(["[y] yes", "[n] I will open it myself!"], title=f"Please check datadog! Do you want me to open it for you?\n{DD_BOARD_URL}",
                                 raise_error_on_interrupt=True)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        os.system(f"open '{DD_BOARD_URL}'")


def ask_if_everything_look_fine_after_all_cutover() -> bool:
    terminal_menu = TerminalMenu(["[y] yes", "[n] no"], title=f"Is everything fine? (check datadog)\n{DD_BOARD_URL}",
                                 raise_error_on_interrupt=True)
    menu_entry_index = terminal_menu.show()
    return menu_entry_index == 0


def progress_sleep(console, t: int):
    with console.status(f"[bold green]Sleeping {t}seconds...") as status:
        for i in range(t):
            status.update(status=f"[bold green]Sleeping {t - i}seconds...")
            time.sleep(1)
    # for _ in tqdm(range(t), leave=False, desc=f"sleeping {t}s"):
    #     time.sleep(1)


def rollback(gopath: str, prebid_k8s_path, api_client: ApiClient):
    raise RuntimeError("NOT IMPLEMENTED :( Do a manual rollback, sorry :sad:")
    print("Step [X]: Rolling back the pods")
    print("Step [X-1]: Rollback to previous service")
    # TODO

    print("Step [X-2]: Remove new pods")
    # TODO


def _main():
    console = Console()

    if 'GOPATH' not in os.environ or os.environ['GOPATH'] == '':
        print('GOPATH should be set in your environ! Contact a publica engineer for help')
        return 1
    gopath = os.environ['GOPATH']

    # 1. CD Inside the prebid kube manifest directory
    prebid_k8s_path = gopath + '/src/github.com/publica-project/prebid-kube-manifests'
    with Dir(prebid_k8s_path):
        console.print("[bold]Step 1: updating prebid tag")
        tag = ask_for_tag()
        if tag == "":
            print("error: tag must not be empty")
            return

        update_prebid_tag(prebid_k8s_path, tag)

        # dev step: assign k8s clients to clusters map
        clusters_to_k8s_client = {}  # type: Dict[str, ApiClient]
        for c in CLUSTERS:
            clusters_to_k8s_client[c] = config.new_client_from_config(
                config_file=import_kube_config(prebid_k8s_path + '/' + c + '/.k8s-assets/kubeconfig'))

        console.print("\n[bold]Step 2: Checking that the cluster is ready")
        for c in CLUSTERS:
            success = check_cluster_ready(get_cluster_name(c), prebid_k8s_path + '/' + c, clusters_to_k8s_client[c])
            if not success:
                raise RuntimeError(f"cluster {get_cluster_name(c)} is not ready")

        console.print("\n[bold]Step 3: Launching the new pods")
        for c in CLUSTERS:
            success = launch_pods(get_cluster_name(c), prebid_k8s_path + '/' + c, clusters_to_k8s_client[c])
            if not success:
                raise RuntimeError(f"failed to launch pods for cluster {get_cluster_name(c)}")
            progress_sleep(console, 60)

        ask_to_open_datadog()

        console.print("\n[bold]Step 4: Cutting over to the new service")
        for c in CLUSTERS:
            while True:
                status = cutover_service(get_cluster_name(c), prebid_k8s_path + '/' + c, clusters_to_k8s_client[c])
                if status == Status.WAIT:
                    progress_sleep(console, 30)
                    continue
                if status == Status.SUCCESS:
                    break
                if status == Status.FAIL:
                    raise RuntimeError(f"failed to cutover the service for cluster {get_cluster_name(c)}")

        is_everything_fine_after_cutover = ask_if_everything_look_fine_after_all_cutover()
        if not is_everything_fine_after_cutover:
            rollback(gopath, prebid_k8s_path, clusters_to_k8s_client[c])
            return 1

        console.print("\n[bold]Step 5: Remove old pods")
        for c in CLUSTERS:
            err = remove_old_pods(get_cluster_name(c), prebid_k8s_path + '/' + c, clusters_to_k8s_client[c])
            if err is not None:
                raise RuntimeError(f'failed to remove old pods for cluster: {get_cluster_name(c)}\n{err}')

        notify("Rollout prebid successfull!", "PBS Rollout")

        console.print("\n[bold green]Done! Don't forget to add the file to git and commit it!")
        console.print(
            f"[grey66]git add namespace/api/pbs.prod.tag; git commit -m 'updating pbs to tag: {tag} with better_rollout'; git push")
        return 0


def main():
    console = Console()
    print_welcome(console)
    if 'help' in sys.argv:
        print_help(console)
    print("\n\n")
    try:
        _main()
    except Exception as e:
        notify("Error during Rollout prebid!", "PBS Rollout", sound=True)
        if isinstance(e, ApiException) and e.reason == 'Unauthorized':
            console.print("[bold red]\nerror: please run `zaws_ctv_engineer` to login")
            return 1
        elif isinstance(e, RuntimeError):
            console.print(f"[bold red]\nError: {e}")
        elif isinstance(e, TimeoutExpired):
            console.print(f"[bold red]\nerror: {e}")
        else:
            console.print_exception()
            console.print('[orange3]please send this to Dimitri Wyzlic on Slack!')
            return 1
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Interrupted by user (keyboard -> CTRL-C)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
