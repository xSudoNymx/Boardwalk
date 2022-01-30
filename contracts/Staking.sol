// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/presets/ERC20PresetMinterPauser.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {StakeMap} from "../contracts/Libraries/StakeMap.sol";

contract MonopolyStaking is Ownable {
    using StakeMap for StakeMap.Map;

    StakeMap.Map private map;

    ERC20PresetMinterPauser public immutable BWC;
    ERC20PresetMinterPauser public immutable Monopoly;

    event LogStake(address indexed recipient, uint256 amount);
    event LogUnstake(address indexed recipient, uint256 amount);
    event ClaimRewards(address indexed recipient, uint256 amount);

    constructor(address _BWC, address _Monopoly) {
        require(_Monopoly != address(0));
        BWC = ERC20PresetMinterPauser(_BWC);
        Monopoly = ERC20PresetMinterPauser(_Monopoly);
    }

    /**
     * @notice A method to check if an address is a stakeholder.
     * @param _address The address to verify.
     * @return bool, uint256 Whether the address is a stakeholder
     */
    function isStakeholder(address _address) internal view returns (bool) {
        return map.contains(_address);
    }

    /**
     * @notice A method to check if an address is a stakeholder.
     * @return bool, uint256 Whether the address is a stakeholder
     */
    function isStakeholder() external view returns (bool) {
        return map.contains(msg.sender);
    }

    /**
     * @notice A method to retrieve the stake for a stakeholder.
     * @param _stakeholder The stakeholder to retrieve the stake for.
     * @return uint256 The amount of wei staked.
     */
    function stakeOf(address _stakeholder) public view returns (uint256) {
        return map.get(_stakeholder);
    }

    /**
     * @notice A method to the aggregated stakes from all stakeholders.
     * @return uint256 The aggregated stakes from all stakeholders.
     */
    function totalStakes() public view returns (uint256) {
        uint256 _totalStakes = 0;
        for (uint256 s = 0; s < map.size(); s += 1) {
            _totalStakes += map.get(map.getKeyAtIndex(s));
        }
        return _totalStakes;
    }

    /**
     * @notice A method to check if stakeholder has unclaimed rewards.
     * @return bool if rewards exist.
     */
    function hasRewards(address _stakeholder) internal returns (bool) {
        return map.getRewards(_stakeholder) > 0;
    }

    /**
     * @notice A method to check stakeholder unclaimed rewards.
     * @return uint256 The rewards of the stakeholder.
     */
    function checkRewards() external view returns (uint256) {
        return map.getRewards(msg.sender);
    }

    /**
     * @notice A method to add a stakeholder.
     * @param _stakeholder The stakeholder to add.
     */
    function addStakeholder(address _stakeholder, uint256 _amount) internal {
        map.add(_stakeholder, _amount);
    }

    /**
     * @notice A method to remove a stakeholder.
     * @param _stakeholder The stakeholder to remove.
     */
    function removeStakeholder(address _stakeholder, uint256 _amount)
        internal
        returns (uint256)
    {
        uint256 total = map.get(_stakeholder);
        total -= _amount;

        map.remove(_stakeholder);

        if (total > 0) {
            map.set(_stakeholder, total);
        }
        return total;
    }

    /**
     * @notice A method to remove a stakeholder.
     * @param _stakeholder The stakeholder to remove.
     */
    function claimStakeholderRewards(address _stakeholder)
        internal
        returns (uint256)
    {
        return map.claimRewards(_stakeholder);
    }

    /**
     * @notice redeem _Monopoly for _BWC
     * @param _amount uint
     */
    function stake(uint256 _amount) external {
        BWC.transferFrom(msg.sender, address(this), _amount);
        Monopoly.mint(address(this), _amount);
        addStakeholder(msg.sender, _amount);
        Monopoly.transfer(msg.sender, _amount);

        emit LogStake(msg.sender, _amount);
    }

    /**
     *   @notice redeem _BWC for _Monopoly
     *   @param _amount uint
     */
    function unstake(uint256 _amount) external {
        require(!hasRewards(msg.sender), "Must Claim Rewards");
        Monopoly.transferFrom(msg.sender, address(this), _amount);
        removeStakeholder(msg.sender, _amount);
        BWC.transfer(msg.sender, _amount);

        emit LogUnstake(msg.sender, _amount);
    }

    /**
     * @notice A method to redeem rewards
     */
    function claim() external {
        require(hasRewards(msg.sender), "No rewards to claim");
        uint256 rewards = claimStakeholderRewards(msg.sender);
        BWC.transfer(msg.sender, rewards);

        emit ClaimRewards(msg.sender, rewards);
    }

    /**
     * @notice A method that calculates the rewards for each stakeholder.
     * @param _stakeholder The stakeholder to calculate rewards for.
     */
    function calculateReward(address _stakeholder) internal returns (uint256) {
        return 1e18;
    }

    /**
     * @notice A method that calculates the rewards for each stakeholder.
     */
    function calculateReward() public view returns (uint256) {
        if (isStakeholder(msg.sender)) return 1e18;
        else return 0;
    }

    /**
     * @notice A method to distribute rewards to all stakeholders.
     */
    function distributeRewards() public onlyOwner {
        for (uint256 s = 0; s < map.size(); s += 1) {
            address stakeholder = map.getKeyAtIndex(s);
            map.addRewards(stakeholder, calculateReward(stakeholder));
        }
    }
}
