pragma solidity >=0.4.21 <0.6.0;

contract Nickname{
    event Setter(string nickname);
    address owner = msg.sender;

    // bidirectional mapping
    mapping(address => string) userNickname;
    mapping(string => address) nicknameUser;


    modifier nickExists(string memory _nickname){
        require(nicknameUser[_nickname] == address(0x0000000000000000000000000000000000000000), "The nickname exists");
        _;
    }

    function setNicknameByUser(string memory _nickname) public nickExists(_nickname){
        userNickname[msg.sender] = _nickname;
        nicknameUser[_nickname] = msg.sender;
        emit Setter(_nickname);
    }

    function getNicknameByUser() public view returns (string memory){
        return userNickname[msg.sender];
    }

    // function deleteNicknameByUser(){

    // }
    // function getListOfNicknames(){

    // }

}