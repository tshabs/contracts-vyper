var uniswap_factory = artifacts.require("uniswap_factory");
var uniswap_exchange = artifacts.require("uniswap_exchange");
const argv = require('yargs').boolean(['testerc20']).argv

if(argv.testerc20){
  var uniswap_test_erc20 = artifacts.require("test_contracts/ERC20");
}

module.exports = function(deployer) {
  // first deploy exchange template
  deployer.deploy(uniswap_exchange).then(function(){
      return deployer.deploy(uniswap_factory, uniswap_exchange.address)
  });
  if(argv.testerc20){
    deployer.deploy(uniswap_test_erc20, web3.utils.toHex(""), web3.utils.toHex(""), 18, 1000);//web3.utils.BN(18), web3.utils.BN(1000000000000000000000));
  }
};
