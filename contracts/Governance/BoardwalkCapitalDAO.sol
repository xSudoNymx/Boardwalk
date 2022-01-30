// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import {MonopolyStaking} from "../Staking.sol";

contract BoardwalkCapitalDAO is Ownable {
    MonopolyStaking private stakeContract;

    constructor(address _stakeContract) {
        require(_stakeContract != address(0));
        stakeContract = MonopolyStaking(_stakeContract);
    }

    function distributeRewards() public onlyOwner {
        stakeContract.distributeRewards();
    }
}
