// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.0;

import {StakeMap} from "../Libraries/StakeMap.sol";

contract TestStakeMap {
    using StakeMap for StakeMap.Map;

    StakeMap.Map private map;

    function get(address _address) public view returns (uint256) {
        return map.get(_address);
    }

    function getKeyAtIndex(uint256 _index) public view returns (address) {
        return map.getKeyAtIndex(_index);
    }

    function size() public view returns (uint256) {
        return map.size();
    }

    function set(address _key, uint256 _val) public {
        map.set(_key, _val);
    }

    function add(address _key, uint256 _val) public {
        map.add(_key, _val);
    }

    function remove(address _key) public {
        map.remove(_key);
    }

    function contains(address _key) public view returns (bool) {
        return map.contains(_key);
    }
}
