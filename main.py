// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ThiisSantaToken
 * @dev A simplified ERC-20 token deployed on the Base ecosystem
 */
contract ThiisSantaToken {
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    address public contractOwner;

    mapping(address => uint256) private balances;
    mapping(address => mapping(address => uint256)) private allowances;

    /**
     * @dev Modifier to restrict access to the owner.
     */
    modifier onlyOwner() {
        require(msg.sender == contractOwner, "Not the owner");
        _;
    }

    /**
     * @dev Event emitted on token transfers.
     */
    event Transfer(address indexed from, address indexed to, uint256 value);

    /**
     * @dev Event emitted on approvals of token allowances.
     */
    event Approval(address indexed tokenOwner, address indexed spender, uint256 value);

    /**
     * @dev Constructor to initialize the token.
     * @param _name The name of the token (e.g., "ThiisSantaToken")
     * @param _symbol The token symbol (e.g., "SANTA")
     * @param _initialSupply The initial token supply (in wei)
     */
    constructor(string memory _name, string memory _symbol, uint256 _initialSupply) {
        name = _name;
        symbol = _symbol;
        totalSupply = _initialSupply * (10 ** uint256(decimals));
        contractOwner = msg.sender;
        balances[contractOwner] = totalSupply;
        emit Transfer(address(0), contractOwner, totalSupply);
    }

    /**
     * @dev Returns the token balance of a specific address.
     * @param account The address to query the balance of.
     * @return The token balance.
     */
    function balanceOf(address account) public view returns (uint256) {
        return balances[account];
    }

    /**
     * @dev Transfers tokens to a specified address.
     * @param recipient The address to transfer to.
     * @param amount The amount to be transferred.
     * @return success True if the transfer was successful.
     */
    function transfer(address recipient, uint256 amount) public returns (bool success) {
        require(recipient != address(0), "Transfer to the zero address");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        balances[recipient] += amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    /**
     * @dev Approves an address to spend tokens on behalf of the caller.
     * @param spender The address to approve.
     * @param amount The amount to approve.
     * @return success True if the approval was successful.
     */
    function approve(address spender, uint256 amount) public returns (bool success) {
        require(spender != address(0), "Approve to the zero address");

        allowances[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    /**
     * @dev Returns the amount of tokens that a spender is allowed to spend on behalf of an owner.
     * @param tokenOwner The owner of the tokens.
     * @param spender The address approved to spend tokens.
     * @return The remaining allowance.
     */
    function allowance(address tokenOwner, address spender) public view returns (uint256) {
        return allowances[tokenOwner][spender];
    }

    /**
     * @dev Transfers tokens on behalf of the owner to a specified address.
     * @param sender The address sending the tokens.
     * @param recipient The address receiving the tokens.
     * @param amount The amount to transfer.
     * @return success True if the transfer was successful.
     */
    function transferFrom(address sender, address recipient, uint256 amount) public returns (bool success) {
        require(sender != address(0), "Transfer from the zero address");
        require(recipient != address(0), "Transfer to the zero address");
        require(balances[sender] >= amount, "Insufficient balance");
        require(allowances[sender][msg.sender] >= amount, "Allowance exceeded");

        balances[sender] -= amount;
        balances[recipient] += amount;
        allowances[sender][msg.sender] -= amount;
        emit Transfer(sender, recipient, amount);
        return true;
    }

    /**
     * @dev Mints new tokens to a specified address. Can only be called by the owner.
     * @param account The address to receive the minted tokens.
     * @param amount The number of tokens to mint.
     */
    function mint(address account, uint256 amount) public onlyOwner {
        require(account != address(0), "Mint to the zero address");

        totalSupply += amount;
        balances[account] += amount;
        emit Transfer(address(0), account, amount);
    }

    /**
     * @dev Burns tokens from a specified address. Can only be called by the owner.
     * @param account The address to burn tokens from.
     * @param amount The number of tokens to burn.
     */
    function burn(address account, uint256 amount) public onlyOwner {
        require(account != address(0), "Burn from the zero address");
        require(balances[account] >= amount, "Insufficient balance to burn");

        totalSupply -= amount;
        balances[account] -= amount;
        emit Transfer(account, address(0), amount);
    }
}
