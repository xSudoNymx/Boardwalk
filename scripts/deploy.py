from brownie import (
    accounts,
    Monopoly,
    Boardwalk,
    MonopolyStaking,
    TestIterableMap,
)
from scripts.helper import get_account
from web3 import Web3


def deployTests():
    account = get_account()
    return TestIterableMap.deploy({"from": account})


def deploy():
    account = get_account()
    mAddress = Boardwalk.deploy({"from": account})
    sAddress = Monopoly.deploy({"from": account})
    stake = MonopolyStaking.deploy(mAddress, sAddress, {"from": account})

    mAddress.mint(account, 1e18, {"from": account})
    sAddress.transferOwnership(stake, {"from": account})

    mAddress.approve(stake, 2 ** 255, {"from": account})
    sAddress.approve(stake, 2 ** 255, {"from": account})
    staked = stake.stake(1e18, {"from": account})
    print(stake.isStakeholder({"from": account}))
    stake.unstake(1e18, {"from": account})


def main():
    deployLibraries()
    deploy()
