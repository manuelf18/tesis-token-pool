pragma solidity >=0.4.21 <0.6.0;
pragma experimental ABIEncoderV2;

contract Nickname{
    event Setter(string nickname);
    event Deleter(address sender);
    address owner = msg.sender;
    uint index; 

    // bidirectional mapping
    mapping(address => string) userNickname;
    mapping(string => address) nicknameUser;

    string[] nicknames;
    string[] deleted;


    modifier nickExists(string memory _nickname){
        require(nicknameUser[_nickname] == address(0x0000000000000000000000000000000000000000), "The nickname exists");
        _;
    }
    modifier nickIsValid(string memory _nickname){
        require(nicknameUser[_nickname] != address(0x0000000000000000000000000000000000000000), "The nickname is not Valid");
        _;
    }
    modifier userIsOwner(address user){
        require(user == owner, "User is not owner");
        _;
    }
    modifier userHasNickname(){
        bytes memory nickname = bytes(userNickname[msg.sender]);
        require(nickname.length > 0, "The user doenst have a nickname");
        _;
    }

    function setNicknameByUser(string memory _nickname) public nickExists(_nickname){
        bytes memory nickname = bytes(userNickname[msg.sender]);
        if(nickname.length > 0){
            deleted.push(userNickname[msg.sender]);
        }
        userNickname[msg.sender] = _nickname;
        nicknameUser[_nickname] = msg.sender;
        nicknames.push(_nickname);
        emit Setter(_nickname);
    }

    function getNicknameByUser() public view userHasNickname returns (string memory){
        return userNickname[msg.sender];
    }

    function getValidNicknames() public view userIsOwner(msg.sender) returns (string[] memory){
        return nicknames;
    }

    function getDeletedNicknames() public view userIsOwner(msg.sender) returns (string[] memory){
        return deleted;
    }

    function deleteNicknameByUser() public userHasNickname{
        string memory nickname = userNickname[msg.sender];
        delete userNickname[msg.sender];
        delete nicknameUser[nickname];
        deleted.push(nickname);
        emit Deleter(msg.sender);
    }
}