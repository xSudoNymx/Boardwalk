import brownie
import pytest


@pytest.fixture(autouse=True)
def shared_setup(fn_isolation):
    pass


def test_dao_distribute(account, stakeContract, transfer, approve, dao):
    assert stakeContract.calculateReward() == 0
    stakeContract.stake(5e18, {"from": account})
    assert stakeContract.calculateReward() == 1e18
    dao.distributeRewards({"from": account})
    assert stakeContract.checkRewards() == 1e18
