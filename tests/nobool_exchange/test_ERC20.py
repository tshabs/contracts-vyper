def test_ERC20(w3, NOB_token, pad_bytes32):
    a0, a1 = w3.eth.accounts[:2]
    assert NOB_token.name() == pad_bytes32('NOB Token')
    assert NOB_token.symbol() == pad_bytes32('NOB')
    assert NOB_token.decimals() == 18
    assert NOB_token.totalSupply() == 100000*10**18
    assert NOB_token.balanceOf(a0) == 100000*10**18
    NOB_token.transfer(a1, 1*10**18, transact={})
    assert NOB_token.balanceOf(a0) == 100000*10**18 - 1*10**18
    assert NOB_token.balanceOf(a1) == 1*10**18
