import brownie
import pytest


@pytest.fixture(autouse=True)
def shared_setup(fn_isolation):
    pass


def test_add_stakeholder(account, TestStakeFixture):
    tx = TestStakeFixture.add(account, 10, {"from": account})
    tx.wait(1)
    assert TestStakeFixture.contains(account) == True
    assert TestStakeFixture.get(account) == 10
    assert TestStakeFixture.getKeyAtIndex(0) == account
    tx = TestStakeFixture.add(account, 5, {"from": account})
    tx.wait(1)
    assert TestStakeFixture.contains(account) == True
    assert TestStakeFixture.get(account) == 15
    assert TestStakeFixture.getKeyAtIndex(0) == account


def test_add_multiple_stakeholders(accounts, TestStakeFixture):
    tx = TestStakeFixture.add(accounts[0], 10, {"from": accounts[0]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[0]) == True
    assert TestStakeFixture.get(accounts[0]) == 10
    assert TestStakeFixture.getKeyAtIndex(0) == accounts[0]
    tx = TestStakeFixture.add(accounts[0], 5, {"from": accounts[0]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[0]) == True
    assert TestStakeFixture.get(accounts[0]) == 15
    assert TestStakeFixture.getKeyAtIndex(0) == accounts[0]
    tx = TestStakeFixture.add(accounts[1], 10, {"from": accounts[1]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[1]) == True
    assert TestStakeFixture.get(accounts[1]) == 10
    assert TestStakeFixture.getKeyAtIndex(1) == accounts[1]
    tx = TestStakeFixture.add(accounts[1], 10, {"from": accounts[1]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[1]) == True
    assert TestStakeFixture.get(accounts[1]) == 20
    assert TestStakeFixture.getKeyAtIndex(1) == accounts[1]


def test_set_stakeholder(account, TestStakeFixture):
    tx = TestStakeFixture.set(account, 10, {"from": account})
    tx.wait(1)
    assert TestStakeFixture.contains(account) == True
    assert TestStakeFixture.get(account) == 10
    assert TestStakeFixture.getKeyAtIndex(0) == account
    tx = TestStakeFixture.set(account, 5, {"from": account})
    tx.wait(1)
    assert TestStakeFixture.contains(account) == True
    assert TestStakeFixture.get(account) == 5
    assert TestStakeFixture.getKeyAtIndex(0) == account


def test_set_multiple_stakeholders(accounts, TestStakeFixture):
    tx = TestStakeFixture.set(accounts[0], 10, {"from": accounts[0]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[0]) == True
    assert TestStakeFixture.get(accounts[0]) == 10
    assert TestStakeFixture.getKeyAtIndex(0) == accounts[0]
    tx = TestStakeFixture.set(accounts[0], 5, {"from": accounts[0]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[0]) == True
    assert TestStakeFixture.get(accounts[0]) == 5
    assert TestStakeFixture.getKeyAtIndex(0) == accounts[0]

    tx = TestStakeFixture.set(accounts[1], 10, {"from": accounts[1]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[1]) == True
    assert TestStakeFixture.get(accounts[1]) == 10
    assert TestStakeFixture.getKeyAtIndex(1) == accounts[1]
    tx = TestStakeFixture.set(accounts[1], 20, {"from": accounts[1]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[1]) == True
    assert TestStakeFixture.get(accounts[1]) == 20
    assert TestStakeFixture.getKeyAtIndex(1) == accounts[1]


def test_remove(account, TestStakeFixture):
    tx = TestStakeFixture.add(account, 10, {"from": account})
    tx.wait(1)
    assert TestStakeFixture.contains(account) == True
    assert TestStakeFixture.get(account) == 10

    tx = TestStakeFixture.remove(account, {"from": account})
    tx.wait(1)
    assert TestStakeFixture.contains(account) == False
    assert TestStakeFixture.get(account) == 0


def test_remove_multiple(accounts, TestStakeFixture):
    tx = TestStakeFixture.add(accounts[0], 10, {"from": accounts[0]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[0]) == True
    assert TestStakeFixture.get(accounts[0]) == 10

    tx = TestStakeFixture.add(accounts[1], 20, {"from": accounts[1]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[1]) == True
    assert TestStakeFixture.get(accounts[1]) == 20

    tx = TestStakeFixture.remove(accounts[0], {"from": accounts[0]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[0]) == False
    assert TestStakeFixture.get(accounts[0]) == 0

    tx = TestStakeFixture.remove(accounts[1], {"from": accounts[1]})
    tx.wait(1)
    assert TestStakeFixture.contains(accounts[1]) == False
    assert TestStakeFixture.get(accounts[1]) == 0
