from tests.constants import (
    ETH_RESERVE,
    HAY_RESERVE,
    HAY_SOLD,
    MIN_ETH_BOUGHT,
    ETH_BOUGHT,
    MAX_HAY_SOLD,
    INITIAL_ETH,
    DEADLINE,
    ZERO_ADDR,
)

def test_swap_input(w3, NOB_token, NOB_exchange, swap_input, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    ETH_PURCHASED = swap_input(HAY_SOLD, HAY_RESERVE, ETH_RESERVE)
    # Transfer HAY to BUYER
    NOB_token.transfer(a1, HAY_SOLD, transact={})
    NOB_token.approve(NOB_exchange.address, HAY_SOLD, transact={'from': a1})
    assert NOB_token.balanceOf(a1) == HAY_SOLD
    # tokens sold == 0
    assert_tx_fail(lambda: NOB_exchange.tokenToEthSwapInput(0, MIN_ETH_BOUGHT, DEADLINE, transact={'from': a1}))
    # min eth == 0
    assert_tx_fail(lambda: NOB_exchange.tokenToEthSwapInput(HAY_SOLD, 0, DEADLINE, transact={'from': a1}))
    # min eth > eth purchased
    assert_tx_fail(lambda: NOB_exchange.tokenToEthSwapInput(HAY_SOLD, ETH_PURCHASED + 1, DEADLINE, transact={'from': a1}))
    # deadline < block.timestamp
    assert_tx_fail(lambda: NOB_exchange.tokenToEthSwapInput(HAY_SOLD, MIN_ETH_BOUGHT, 1, transact={'from': a1}))
    # BUYER converts ETH to UNI
    NOB_exchange.tokenToEthSwapInput(HAY_SOLD, MIN_ETH_BOUGHT, DEADLINE, transact={'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE - ETH_PURCHASED
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE + HAY_SOLD
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == 0
    assert w3.eth.getBalance(a1) == INITIAL_ETH + ETH_PURCHASED

def test_transfer_input(w3, NOB_token, NOB_exchange, swap_input, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    ETH_PURCHASED = swap_input(HAY_SOLD, HAY_RESERVE, ETH_RESERVE)
    # Transfer HAY to BUYER
    NOB_token.transfer(a1, HAY_SOLD, transact={})
    NOB_token.approve(NOB_exchange.address, HAY_SOLD, transact={'from': a1})
    assert NOB_token.balanceOf(a1) == HAY_SOLD
    # recipient == ZERO_ADDR
    assert_tx_fail(lambda: NOB_exchange.tokenToEthTransferInput(HAY_SOLD, 1, DEADLINE, ZERO_ADDR, transact={'from': a1}))
    # recipient == exchange
    assert_tx_fail(lambda: NOB_exchange.tokenToEthTransferInput(HAY_SOLD, 1, DEADLINE, NOB_exchange.address, transact={'from': a1}))
    # BUYER converts ETH to UNI
    NOB_exchange.tokenToEthTransferInput(HAY_SOLD, 1, DEADLINE, a2, transact={'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE - ETH_PURCHASED
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE + HAY_SOLD
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == 0
    assert w3.eth.getBalance(a1) == INITIAL_ETH
    # Updated balances of RECIPIENT
    assert NOB_token.balanceOf(a2) == 0
    assert w3.eth.getBalance(a2) == INITIAL_ETH + ETH_PURCHASED

def test_swap_output(w3, NOB_token, NOB_exchange, swap_output, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    HAY_COST = swap_output(ETH_BOUGHT, HAY_RESERVE, ETH_RESERVE)
    # Transfer HAY to BUYER
    NOB_token.transfer(a1, MAX_HAY_SOLD, transact={})
    NOB_token.approve(NOB_exchange.address, MAX_HAY_SOLD, transact={'from': a1})
    assert NOB_token.balanceOf(a1) == MAX_HAY_SOLD
    # tokens bought == 0
    assert_tx_fail(lambda: NOB_exchange.tokenToEthSwapOutput(0, MAX_HAY_SOLD, DEADLINE, transact={'from': a1}))
    # max tokens < token cost
    assert_tx_fail(lambda: NOB_exchange.tokenToEthSwapOutput(ETH_BOUGHT, HAY_COST - 1, DEADLINE, transact={'from': a1}))
    # deadline < block.timestamp
    assert_tx_fail(lambda: NOB_exchange.tokenToEthSwapOutput(ETH_BOUGHT, MAX_HAY_SOLD, 1, transact={'from': a1}))
    # BUYER converts ETH to UNI
    NOB_exchange.tokenToEthSwapOutput(ETH_BOUGHT, MAX_HAY_SOLD, DEADLINE, transact={'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE - ETH_BOUGHT
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE + HAY_COST
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == MAX_HAY_SOLD - HAY_COST
    assert w3.eth.getBalance(a1) == INITIAL_ETH + ETH_BOUGHT

def test_transfer_output(w3, NOB_token, NOB_exchange, swap_output, assert_tx_fail):
    a0, a1, a2 = w3.eth.accounts[:3]
    HAY_COST = swap_output(ETH_BOUGHT, HAY_RESERVE, ETH_RESERVE)
    # Transfer HAY to BUYER
    NOB_token.transfer(a1, MAX_HAY_SOLD, transact={})
    NOB_token.approve(NOB_exchange.address, MAX_HAY_SOLD, transact={'from': a1})
    assert NOB_token.balanceOf(a1) == MAX_HAY_SOLD
    # recipient == ZERO_ADDR
    assert_tx_fail(lambda: NOB_exchange.tokenToEthTransferOutput(ETH_BOUGHT, MAX_HAY_SOLD, DEADLINE, ZERO_ADDR, transact={'from': a1}))
    # recipient == exchange
    assert_tx_fail(lambda: NOB_exchange.tokenToEthTransferOutput(ETH_BOUGHT, MAX_HAY_SOLD, DEADLINE, NOB_exchange.address, transact={'from': a1}))
    # BUYER converts ETH to UNI
    NOB_exchange.tokenToEthTransferOutput(ETH_BOUGHT, MAX_HAY_SOLD, DEADLINE, a2, transact={'from': a1})
    # Updated balances of UNI exchange
    assert w3.eth.getBalance(NOB_exchange.address) == ETH_RESERVE - ETH_BOUGHT
    assert NOB_token.balanceOf(NOB_exchange.address) == HAY_RESERVE + HAY_COST
    # Updated balances of BUYER
    assert NOB_token.balanceOf(a1) == MAX_HAY_SOLD - HAY_COST
    assert w3.eth.getBalance(a1) == INITIAL_ETH
    # Updated balances of RECIPIENT
    assert NOB_token.balanceOf(a2) == 0
    assert w3.eth.getBalance(a2) == INITIAL_ETH + ETH_BOUGHT
