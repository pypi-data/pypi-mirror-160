import os
from typing import List

from wton.utils import storage

# workdir
DEFAULT_LOCAL_WORKDIR: str = storage.local_workdir(".wton")
GLOBAL_WORKDIR: str = storage.global_workdir()
LOCAL_WORKDIR: str = storage.find_local_workdir(".wton")
CURRENT_WORKDIR = LOCAL_WORKDIR if LOCAL_WORKDIR is not None else GLOBAL_WORKDIR

# config paths
INIT_LOCAL_CONFIG_PATH: str = os.path.join(
    DEFAULT_LOCAL_WORKDIR, "config.yaml")
GLOBAL_CONFIG_PATH: str = os.path.join(
    GLOBAL_WORKDIR, "config.yaml")
LOCAL_CONFIG_PATH: str = os.path.join(
    DEFAULT_LOCAL_WORKDIR if LOCAL_WORKDIR is None else LOCAL_WORKDIR, "config.yaml")
EXTRA_CONFIG_PATH: str = os.environ.get('wton_CONFIG_PATH')
CONFIG_PATHS: List[str] = [
    GLOBAL_CONFIG_PATH, LOCAL_CONFIG_PATH]
if EXTRA_CONFIG_PATH:
    CONFIG_PATHS.append(EXTRA_CONFIG_PATH)

# dapp
DAPP_MAINNET_GRAPHQL_URL = "https://dapp-01.tontech.io/graphql"
DAPP_MAINNET_BROADCAST_URL = "https://dapp-01.tontech.io/broadcast"
DAPP_TESTNET_GRAPHQL_URL = "https://dapp-test.tontech.io/graphql"
DAPP_TESTNET_BROADCAST_URL = "https://dapp-test.tontech.io/broadcast"

# wton
KEYSTORE_PASSWORD = os.environ.get('WTON_KEYSTORE_PASSWORD', '')
