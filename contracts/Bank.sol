// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Bank is Ownable {
    using SafeERC20 for IERC20;
    event Deposit(address indexed token, uint256 amount);
    event Withdrawal(address indexed token, uint256 amount);

    IERC20 public immutable Monopoly;

    address[] public reserveTokens;
    mapping(address => bool) public isReserveToken;

    address[] public reserveDepositors;
    mapping(address => bool) public isReserveDepositor;

    address[] public reserveSpenders;
    mapping(address => bool) public isReserveSpender;

    constructor(
        address _Monopoly,
        address _Tether,
        address _USDC,
        address _DAI
    ) {
        require(_Monopoly != address(0));
        Monopoly = IERC20(_Monopoly);

        isReserveToken[_Tether] = true;
        reserveTokens.push(_Tether);
        isReserveToken[_USDC] = true;
        reserveTokens.push(_USDC);
        isReserveToken[_DAI] = true;
        reserveTokens.push(_DAI);
    }

    /**
        @notice allow approved address to deposit an asset for Monopoly
        @param _amount uint   - Amount of Token to be deposited
        @param _token address - Address of Token to be deposited
     */
    function deposit(uint256 _amount, address _token) external {
        require(isReserveToken[_token], "Not accepted");
        require(isReserveDepositor[msg.sender], "Not approved");

        IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount);
        emit Deposit(_token, _amount);
    }

    /**
        @notice allow approved address to burn Time for reserves
        @param _amount uint   - Amount of Token to be deposited
        @param _token address - Address of Token to be deposited
     */
    function withdraw(uint256 _amount, address _token) external {
        require(isReserveToken[_token], "Not accepted"); // Only reserves can be used for withdraws
        require(isReserveSpender[msg.sender], "Not approved");

        IERC20(_token).safeTransfer(msg.sender, _amount);
        emit Withdrawal(_token, _amount);
    }
}
