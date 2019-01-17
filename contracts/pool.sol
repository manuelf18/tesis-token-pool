contract EthereumContract{
    // TODO
}

contract BitcoinContract{
    // TODO
}

contract PoolContract {
    uint[] id;
    mapping(id => address[]) participants;
    mapping(id => string) poolName;
    mapping(id => address) tokenContract;

    event LogSetPoolParticipant(bytes32 address);

    function getPoolParticipants(uint _id) external returns(address[], string, address) {
        return (participants[_id], poolName[_id], tokenContract[_id]);
    }

    function setPoolParticipant(uint _id) external {

    }
}