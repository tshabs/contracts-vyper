from tests.constants import (
    ETH_RESERVE,
    HAY_RESERVE,
    ZERO_ADDR,
)

def test_deploy(w3, NOB_token, NOB_exchange, factory, pad_bytes32, assert_tx_fail):
    a0, a1 = w3.eth.accounts[:2]
    # Can't call setup after add liquidity
    assert_tx_fail(lambda: NOB_exchange.setup(NOB_token.address, a0, transact={}))
    # Asser NOB token NOT registered to factory
    assert factory.getExchange(NOB_token.address) == None
    assert factory.getToken(NOB_exchange.address) == None
    # Exchange initial state
    assert NOB_exchange.name() == pad_bytes32('Uniswap Custom')
    assert NOB_exchange.symbol() == pad_bytes32('UNI-V1')
    assert NOB_exchange.decimals() == 18
    assert NOB_exchange.totalSupply() == ETH_RESERVE
    assert NOB_exchange.tokenAddress() == NOB_token.address
    assert NOB_exchange.factoryAddress() == factory.address
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE
