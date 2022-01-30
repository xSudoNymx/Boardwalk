// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.0;

library StakeMap {
    struct Map {
        address[] keys;
        mapping(address => uint256) values;
        mapping(address => uint256) indexOf;
        mapping(address => bool) inserted;
        mapping(address => uint256) rewards;
    }

    function get(Map storage map, address key) public view returns (uint256) {
        return map.values[key];
    }

    function getRewards(Map storage map, address key)
        public
        view
        returns (uint256)
    {
        return map.rewards[key];
    }

    function getKeyAtIndex(Map storage map, uint256 index)
        public
        view
        returns (address)
    {
        return map.keys[index];
    }

    function size(Map storage map) public view returns (uint256) {
        return map.keys.length;
    }

    function set(
        Map storage map,
        address key,
        uint256 val
    ) public {
        if (map.inserted[key]) {
            map.values[key] = val;
        } else {
            map.inserted[key] = true;
            map.values[key] = val;
            map.indexOf[key] = map.keys.length;
            map.rewards[key] = 0;
            map.keys.push(key);
        }
    }

    function add(
        Map storage map,
        address key,
        uint256 val
    ) public {
        if (map.inserted[key]) {
            map.values[key] += val;
        } else {
            map.inserted[key] = true;
            map.values[key] = val;
            map.indexOf[key] = map.keys.length;
            map.rewards[key] = 0;
            map.keys.push(key);
        }
    }

    function remove(Map storage map, address key) public {
        if (!map.inserted[key]) {
            return;
        }

        delete map.inserted[key];
        delete map.values[key];
        delete map.rewards[key];

        uint256 index = map.indexOf[key];
        uint256 lastIndex = map.keys.length - 1;
        address lastKey = map.keys[lastIndex];

        map.indexOf[lastKey] = index;
        delete map.indexOf[key];

        map.keys[index] = lastKey;
        map.keys.pop();
    }

    function claimRewards(Map storage map, address key)
        public
        returns (uint256)
    {
        if (!map.inserted[key]) return 0;

        uint256 rewards = map.rewards[key];
        map.rewards[key] = 0;
        return rewards;
    }

    function addRewards(
        Map storage map,
        address key,
        uint256 amount
    ) public {
        if (!map.inserted[key]) return;

        map.rewards[key] += amount;
    }

    function contains(Map storage map, address key) public view returns (bool) {
        if (map.inserted[key]) return true;
        else return false;
    }
}
