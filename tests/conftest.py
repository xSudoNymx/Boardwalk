from brownie import (
    Monopoly,
    Boardwalk,
    MonopolyStaking,
    StakeMap,
    TestStakeMap,
    BoardwalkCapitalDAO,
)
from scripts.helper import get_account, get_accounts
import pytest


@pytest.fixture(autouse=True, scope="module")
def account():
    return get_account()


@pytest.fixture(autouse=True, scope="module")
def accounts():
    return get_accounts()


@pytest.fixture(autouse=True, scope="module")
def Map(account):
    StakeMap.deploy({"from": account})


@pytest.fixture(scope="module")
def BWCToken(account):
    return Boardwalk.deploy({"from": account})


@pytest.fixture(scope="module")
def MonopolyToken(account):
    return Monopoly.deploy({"from": account})


@pytest.fixture(scope="module")
def stakeContract(account, BWCToken, MonopolyToken):
    return MonopolyStaking.deploy(BWCToken, MonopolyToken, {"from": account})


@pytest.fixture(scope="module")
def transfer(account, MonopolyToken, BWCToken, stakeContract):
    MonopolyToken.transferOwnership(stakeContract, {"from": account})
    MonopolyToken.mint(stakeContract, 1e27, {"from": stakeContract})
    BWCToken.mint(account, 10e18, {"from": account})


@pytest.fixture(scope="module")
def approve(account, BWCToken, MonopolyToken, stakeContract):
    BWCToken.approve(stakeContract, 2 ** 255, {"from": account})
    MonopolyToken.approve(stakeContract, 2 ** 255, {"from": account})


@pytest.fixture(scope="module")
def TestStakeFixture(account):
    return TestStakeMap.deploy({"from": account})


@pytest.fixture(scope="module")
def dao(account, stakeContract):
    BWCDao = BoardwalkCapitalDAO.deploy(stakeContract, {"from": account})
    stakeContract.transferOwnership(BWCDao, {"from": account})
    return BWCDao
