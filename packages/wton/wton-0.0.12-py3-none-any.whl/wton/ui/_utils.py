import dataclasses
from typing import Optional
from xmlrpc.client import Boolean
from prettytable import MARKDOWN, PrettyTable

from wton.tonclient.utils import KeyStores, Whitelist, KeyStore
from wton.tonclient import TonClient, DAppTonClient
from wton.config import init_config, Config, TonProviderEnum
from wton.utils import storage


@dataclasses.dataclass
class SharedObject:
    config: Config
    ton_client: TonClient
    specific_config_path: Optional[str]
    keystores: Optional[KeyStores] = None
    keystore: Optional[KeyStore] = None
    keystore_password: Optional[str] = None
    whitelist: Optional[Whitelist] = None
    debug_mode: Boolean = False


def init_shared_object(specific_config_path: str = None) -> SharedObject:
    config = init_config(
        specific_config_path) if specific_config_path is not None else init_config()
    ton_client = __get_ton_client(config)

    return SharedObject(
        config=config, specific_config_path=specific_config_path, ton_client=ton_client)


def setup_app(config: Config):
    for default_dir_path in [config.wton.workdir,
                             config.wton.keystores_path]:
        storage.ensure_dir_exists(default_dir_path)


def md_table() -> PrettyTable:
    table = PrettyTable()
    table.set_style(MARKDOWN)
    return table

def __get_ton_client(config: Config):
    if config.wton.provider == TonProviderEnum.dapp:
        return DAppTonClient(config)
    else:
        raise NotImplementedError



def new_keystore_password_is_valid(password: str):
    if len(password) < 6:
        return False

    return True
