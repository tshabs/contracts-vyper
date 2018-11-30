from tests.constants import (
    ETH_RESERVE,
    HAY_RESERVE,
    ETH_SOLD,
    MIN_HAY_BOUGHT,
    HAY_BOUGHT,
    MAX_ETH_SOLD,
    INITIAL_ETH,
    DEADLINE,
    ZERO_ADDR,
)

def test_swap_default(w3, NOB_token, NOB_exchange, swap_input, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    HAY_PURCHASED = swap_input(ETH_SOLD, ETH_RESERVE, HAY_RESERVE)
    # msg.value == 0
    assert_tx_fail(lambda: w3.eth.sendTransaction({'to': NOB_exchange.address, 'value': 0, 'from': a1}))
    # BUYER converts ETH to UNI
    w3.eth.sendTransaction({'to': NOB_exchange.address, 'value': ETH_SOLD, 'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE + ETH_SOLD
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE - HAY_PURCHASED
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == HAY_PURCHASED
    assert w3.eth.getBalance(a1) == INITIAL_ETH - ETH_SOLD

def test_swap_input(w3, NOB_token, NOB_exchange, swap_input, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    HAY_PURCHASED = swap_input(ETH_SOLD, ETH_RESERVE, HAY_RESERVE)
    assert NOB_exchange.getEthToTokenInputPrice(ETH_SOLD) == HAY_PURCHASED
    # eth sold == 0
    assert_tx_fail(lambda: NOB_exchange.ethToTokenSwapInput(MIN_HAY_BOUGHT, DEADLINE, transact={'value': 0, 'from': a1}))
    # min tokens == 0
    assert_tx_fail(lambda: NOB_exchange.ethToTokenSwapInput(0, DEADLINE, transact={'value': ETH_SOLD, 'from': a1}))
    # min tokens > tokens purchased
    assert_tx_fail(lambda: NOB_exchange.ethToTokenSwapInput(HAY_PURCHASED + 1, DEADLINE, transact={'value': ETH_SOLD, 'from': a1}))
    # deadline < block.timestamp
    assert_tx_fail(lambda: NOB_exchange.ethToTokenSwapInput(MIN_HAY_BOUGHT, 1, transact={'value': ETH_SOLD, 'from': a1}))
    # BUYER converts ETH to UNI
    NOB_exchange.ethToTokenSwapInput(MIN_HAY_BOUGHT, DEADLINE, transact={'value': ETH_SOLD, 'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE + ETH_SOLD
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE - HAY_PURCHASED
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == HAY_PURCHASED
    assert w3.eth.getBalance(a1) == INITIAL_ETH - ETH_SOLD

def test_transfer_input(w3, NOB_token, NOB_exchange, swap_input, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    HAY_PURCHASED = swap_input(ETH_SOLD, ETH_RESERVE, HAY_RESERVE)
    # recipient == ZERO_ADDR
    assert_tx_fail(lambda: NOB_exchange.ethToTokenTransferInput(MIN_HAY_BOUGHT, DEADLINE, ZERO_ADDR, transact={'value': ETH_SOLD, 'from': a1}))
    # recipient == exchange
    assert_tx_fail(lambda: NOB_exchange.ethToTokenTransferInput(MIN_HAY_BOUGHT, DEADLINE, NOB_exchange.address, transact={'value': ETH_SOLD, 'from': a1}))
    # BUYER converts ETH to UNI
    NOB_exchange.ethToTokenTransferInput(MIN_HAY_BOUGHT, DEADLINE, a2, transact={'value': ETH_SOLD, 'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE + ETH_SOLD
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE - HAY_PURCHASED
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == 0
    assert w3.eth.getBalance(a1) == INITIAL_ETH - ETH_SOLD
    # Updated balances of RECIPIENT
    assert NOB_token.balanceOf(a2) == HAY_PURCHASED
    assert w3.eth.getBalance(a2) == INITIAL_ETH


def test_swap_output(w3, NOB_token, NOB_exchange, swap_output, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    ETH_COST = swap_output(HAY_BOUGHT, ETH_RESERVE, HAY_RESERVE)
    assert NOB_exchange.getEthToTokenOutputPrice(HAY_BOUGHT) == ETH_COST
    # max eth < ETH_COST
    assert_tx_fail(lambda: NOB_exchange.ethToTokenSwapOutput(HAY_BOUGHT, DEADLINE, transact={'value': ETH_COST - 1, 'from': a1}))
    # tokens bought == 0
    assert_tx_fail(lambda: NOB_exchange.ethToTokenSwapOutput(0, DEADLINE, transact={'value': MAX_ETH_SOLD, 'from': a1}))
    # deadline < block.timestamp
    assert_tx_fail(lambda: NOB_exchange.ethToTokenSwapOutput(HAY_BOUGHT, 1, transact={'value': MAX_ETH_SOLD, 'from': a1}))
    # BUYER converts ETH to UNI
    NOB_exchange.ethToTokenSwapOutput(HAY_BOUGHT, DEADLINE, transact={'value': MAX_ETH_SOLD, 'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE + ETH_COST
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE - HAY_BOUGHT
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == HAY_BOUGHT
    assert w3.eth.getBalance(a1) == INITIAL_ETH - ETH_COST

def test_transfer_output(w3, NOB_token, NOB_exchange, swap_output, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    ETH_COST = swap_output(HAY_BOUGHT, ETH_RESERVE, HAY_RESERVE)
    # recipient == ZERO_ADDR
    assert_tx_fail(lambda: NOB_exchange.ethToTokenTransferOutput(HAY_BOUGHT, DEADLINE, ZERO_ADDR, transact={'value': MAX_ETH_SOLD, 'from': a1}))
    # recipient == exchange
    assert_tx_fail(lambda: NOB_exchange.ethToTokenTransferOutput(HAY_BOUGHT, DEADLINE, NOB_exchange.address, transact={'value': MAX_ETH_SOLD, 'from': a1}))
    # BUYER converts ETH to UNI
    NOB_exchange.ethToTokenTransferOutput(HAY_BOUGHT, DEADLINE, a2, transact={'value': MAX_ETH_SOLD, 'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE + ETH_COST
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE - HAY_BOUGHT
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == 0
    assert w3.eth.getBalance(a1) == INITIAL_ETH - ETH_COST
    # Updated balances of RECIPIENT
    assert NOB_token.balanceOf(a2) == HAY_BOUGHT
    assert w3.eth.getBalance(a2) == INITIAL_ETH
