var uniswap_factory = artifacts.require("uniswap_factory");
var uniswap_exchange = artifacts.require("uniswap_exchange");
const argv = require('yargs').boolean(['testerc20']).argv

if(argv.testerc20){
  var uniswap_test_erc20 = artifacts.require("test_contracts/ERC20");
}

module.exports = function(deployer) {
  // deploy erc20 if needed
  if(argv.testerc20){
    deployer.deploy(uniswap_test_erc20, web3.utils.toHex(""), web3.utils.toHex(""), 18, 1000);//web3.utils.BN(18), web3.utils.BN(1000000000000000000000));
  }
  // first deploy exchange template

  deployer.deploy(uniswap_exchange);
  deployer.deploy(uniswap_factory);

  uniswap_factory.deployed(uniswap_factory).then(function(instance){
      instance.initializeFactory(uniswap_exchange.address).then(function(tx) {
        console.log("Initialized factory successfully. (set exchange template address to: ", uniswap_exchange.address, ")");
        console.log(tx);
        return deployer;
      }).catch(function(e) {
        console.log(e);
      });
  });
};
