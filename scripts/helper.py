from brownie import accounts, network, config

LOCAL_BC_ENV = ["development", "ganache-local"]
FORK_BC_ENV = ["mainnet-fork"]


def get_account():
    if network.show_active() in LOCAL_BC_ENV or network.show_active() in FORK_BC_ENV:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_accounts():
    return accounts
