import brownie
import pytest


@pytest.fixture(autouse=True)
def shared_setup(fn_isolation):
    pass


def test_stake_unstake(
    account, BWCToken, MonopolyToken, stakeContract, transfer, approve
):
    stakeContract.stake(5e18, {"from": account})
    assert stakeContract.isStakeholder({"from": account}) == True
    assert stakeContract.stakeOf(account) == 5e18
    assert stakeContract.totalStakes() == 5e18
    assert MonopolyToken.balanceOf(account) == 5e18
    assert BWCToken.balanceOf(account) == 5e18

    stakeContract.unstake(1e18, {"from": account})
    assert stakeContract.isStakeholder({"from": account}) == True
    assert stakeContract.stakeOf(account) == 4e18
    assert stakeContract.totalStakes() == 4e18
    assert MonopolyToken.balanceOf(account) == 4e18
    assert BWCToken.balanceOf(account) == 6e18

    stakeContract.unstake(4e18, {"from": account})
    assert stakeContract.isStakeholder({"from": account}) == False
    assert stakeContract.stakeOf(account) == 0
    assert stakeContract.totalStakes() == 0
    assert MonopolyToken.balanceOf(account) == 0
    assert BWCToken.balanceOf(account) == 10e18


def test_stake_not_enough(
    account, BWCToken, MonopolyToken, stakeContract, transfer, approve
):
    with brownie.reverts("ERC20: transfer amount exceeds balance"):
        stakeContract.stake(
            15e18, {"from": account, "gas_limit": 100000, "allow_revert": True}
        )
    assert stakeContract.isStakeholder({"from": account}) == False
    assert BWCToken.balanceOf(account) == 10e18


def test_unstake_with_rewards(
    account, BWCToken, MonopolyToken, stakeContract, transfer, approve
):
    stakeContract.stake(5e18, {"from": account})
    stakeContract.distributeRewards({"from": account})
    with brownie.reverts("Must Claim Rewards"):
        stakeContract.unstake(
            5e18, {"from": account, "gas_limit": 100000, "allow_revert": True}
        )


def test_unstake_not_enough(
    account, BWCToken, MonopolyToken, stakeContract, transfer, approve
):
    stakeContract.stake(5e18, {"from": account})
    with brownie.reverts("ERC20: transfer amount exceeds balance"):
        stakeContract.unstake(
            10e18, {"from": account, "gas_limit": 100000, "allow_revert": True}
        )
    assert stakeContract.isStakeholder({"from": account}) == True
    assert BWCToken.balanceOf(account) == 5e18
    assert MonopolyToken.balanceOf(account) == 5e18


def test_reward_distro(account, stakeContract, transfer, approve):
    assert stakeContract.calculateReward() == 0
    stakeContract.stake(5e18, {"from": account})
    assert stakeContract.calculateReward() == 1e18
    stakeContract.distributeRewards({"from": account})
    assert stakeContract.checkRewards() == 1e18


def test_reward_claim(account, BWCToken, stakeContract, transfer, approve):
    stakeContract.stake(5e18, {"from": account})
    stakeContract.distributeRewards({"from": account})
    stakeContract.claim({"from": account})
    assert BWCToken.balanceOf(account) == 6e18


def test_reward_claim_no_reward(account, stakeContract, transfer, approve):
    with brownie.reverts("No rewards to claim"):
        stakeContract.claim(
            {"from": account, "gas_limit": 100000, "allow_revert": True}
        )
