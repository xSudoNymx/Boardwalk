import brownie
import pytest


@pytest.fixture(autouse=True)
def shared_setup(fn_isolation):
    pass


def test_add_stakeholder(account, itrMap):
    tx = itrMap.add(account, 10, {"from": account})
    tx.wait(1)
    assert itrMap.contains(account) == True
    assert itrMap.get(account) == 10
    assert itrMap.getKeyAtIndex(0) == account
    tx = itrMap.add(account, 5, {"from": account})
    tx.wait(1)
    assert itrMap.contains(account) == True
    assert itrMap.get(account) == 15
    assert itrMap.getKeyAtIndex(0) == account


def test_add_multiple_stakeholders(accounts, itrMap):
    tx = itrMap.add(accounts[0], 10, {"from": accounts[0]})
    tx.wait(1)
    assert itrMap.contains(accounts[0]) == True
    assert itrMap.get(accounts[0]) == 10
    assert itrMap.getKeyAtIndex(0) == accounts[0]
    tx = itrMap.add(accounts[0], 5, {"from": accounts[0]})
    tx.wait(1)
    assert itrMap.contains(accounts[0]) == True
    assert itrMap.get(accounts[0]) == 15
    assert itrMap.getKeyAtIndex(0) == accounts[0]
    tx = itrMap.add(accounts[1], 10, {"from": accounts[1]})
    tx.wait(1)
    assert itrMap.contains(accounts[1]) == True
    assert itrMap.get(accounts[1]) == 10
    assert itrMap.getKeyAtIndex(1) == accounts[1]
    tx = itrMap.add(accounts[1], 10, {"from": accounts[1]})
    tx.wait(1)
    assert itrMap.contains(accounts[1]) == True
    assert itrMap.get(accounts[1]) == 20
    assert itrMap.getKeyAtIndex(1) == accounts[1]


def test_set_stakeholder(account, itrMap):
    tx = itrMap.set(account, 10, {"from": account})
    tx.wait(1)
    assert itrMap.contains(account) == True
    assert itrMap.get(account) == 10
    assert itrMap.getKeyAtIndex(0) == account
    tx = itrMap.set(account, 5, {"from": account})
    tx.wait(1)
    assert itrMap.contains(account) == True
    assert itrMap.get(account) == 5
    assert itrMap.getKeyAtIndex(0) == account


def test_set_multiple_stakeholders(accounts, itrMap):
    tx = itrMap.set(accounts[0], 10, {"from": accounts[0]})
    tx.wait(1)
    assert itrMap.contains(accounts[0]) == True
    assert itrMap.get(accounts[0]) == 10
    assert itrMap.getKeyAtIndex(0) == accounts[0]
    tx = itrMap.set(accounts[0], 5, {"from": accounts[0]})
    tx.wait(1)
    assert itrMap.contains(accounts[0]) == True
    assert itrMap.get(accounts[0]) == 5
    assert itrMap.getKeyAtIndex(0) == accounts[0]

    tx = itrMap.set(accounts[1], 10, {"from": accounts[1]})
    tx.wait(1)
    assert itrMap.contains(accounts[1]) == True
    assert itrMap.get(accounts[1]) == 10
    assert itrMap.getKeyAtIndex(1) == accounts[1]
    tx = itrMap.set(accounts[1], 20, {"from": accounts[1]})
    tx.wait(1)
    assert itrMap.contains(accounts[1]) == True
    assert itrMap.get(accounts[1]) == 20
    assert itrMap.getKeyAtIndex(1) == accounts[1]


def test_remove(account, itrMap):
    tx = itrMap.add(account, 10, {"from": account})
    tx.wait(1)
    assert itrMap.contains(account) == True
    assert itrMap.get(account) == 10

    tx = itrMap.remove(account, {"from": account})
    tx.wait(1)
    assert itrMap.contains(account) == False
    assert itrMap.get(account) == 0


def test_remove_multiple(accounts, itrMap):
    tx = itrMap.add(accounts[0], 10, {"from": accounts[0]})
    tx.wait(1)
    assert itrMap.contains(accounts[0]) == True
    assert itrMap.get(accounts[0]) == 10

    tx = itrMap.add(accounts[1], 20, {"from": accounts[1]})
    tx.wait(1)
    assert itrMap.contains(accounts[1]) == True
    assert itrMap.get(accounts[1]) == 20

    tx = itrMap.remove(accounts[0], {"from": accounts[0]})
    tx.wait(1)
    assert itrMap.contains(accounts[0]) == False
    assert itrMap.get(accounts[0]) == 0

    tx = itrMap.remove(accounts[1], {"from": accounts[1]})
    tx.wait(1)
    assert itrMap.contains(accounts[1]) == False
    assert itrMap.get(accounts[1]) == 0
