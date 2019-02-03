pragma solidity >=0.4.21 <0.6.0;

contract HelloWorld {
    event Setter(string x);
    string public myString = "Hello World";

    function set(string memory x) public {
        myString = x;
        emit Setter(myString);
    }
}