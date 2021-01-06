from xbridge_tokens_balances_orderbooks import *
from web3 import Web3
import web3
from uniswap import Uniswap  # https://github.com/shanefontaine/uniswap-python for more info
from utils import dxsettings
import json

EIP20_ABI = json.loads(
    '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501


# functions >>
def init_uniswap_wrapper():
    uni_wrapper = Uniswap(dxsettings.uni_address, dxsettings.uni_private_key,
                          provider=dxsettings.infura_url,
                          version=2)  # pass version=2 to use Uniswap v2
    return uni_wrapper


def init_web3():
    return Web3(Web3.HTTPProvider(dxsettings.infura_url))


def uni_conversion(rate1, rate2, decimal1, decimal2=10 ** 6):  # default decimal2 on usdt dec
    conv = ((1 / rate1) * (rate2 / decimal2)) * decimal1
    return conv


def uni_eth_to_token_input(eth_amount, to_token):
    return uniswap_wrapper.get_eth_token_input_price(to_token, eth_amount * 10 ** 18)


def calc_eth_to_token_from_input(amount, token, token_dec):
    contract = w3.eth.contract(abi=EIP20_ABI, address=token)
    print("calc swap", amount, "ETH to", contract.functions.symbol().call(), ":")
    return uni_eth_to_token_input(amount, token) / token_dec


# functions <<

# MAIN>>
if __name__ == "__main__":
    print("\nUNISWAP SIDE:\n")
    uniswap_wrapper = init_uniswap_wrapper()
    w3 = init_web3()

    usdt = Web3.toChecksumAddress("0xdac17f958d2ee523a2206206994597c13d831ec7")
    usdt_contract = w3.eth.contract(abi=EIP20_ABI, address=usdt)
    usdt_dec = 10 ** usdt_contract.functions.decimals().call()
    usdt_rate = uni_eth_to_token_input(1, usdt)
    usd_eth_rate = usdt_rate / usdt_dec
    print("1 ETH =", usd_eth_rate, "USD")

    wbtc = Web3.toChecksumAddress("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")
    wbtc_contract = w3.eth.contract(abi=EIP20_ABI, address=wbtc)
    wbtc_dec = 10 ** wbtc_contract.functions.decimals().call()
    wbtc_rate = uni_eth_to_token_input(1, wbtc)
    print("1 WBTC =", uni_conversion(wbtc_rate, usdt_rate, wbtc_dec), "USDT")

    usdc = Web3.toChecksumAddress("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
    usdc_contract = w3.eth.contract(abi=EIP20_ABI, address=usdc)
    usdc_dec = 10 ** usdc_contract.functions.decimals().call()
    usdc_rate = uni_eth_to_token_input(1, usdc)
    print("1 USDC =", uni_conversion(usdc_rate, usdt_rate, usdc_dec), "USDT")

    ablock = Web3.toChecksumAddress("0xe692c8d72bd4ac7764090d54842a305546dd1de5")
    ablock_contract = w3.eth.contract(abi=EIP20_ABI, address=ablock)
    ablock_dec = 10 ** ablock_contract.functions.decimals().call()
    ablock_rate = uni_eth_to_token_input(1, ablock)
    print("1 aBLOCK =", uni_conversion(ablock_rate, usdt_rate, ablock_dec), "USDT")

    print("\npublic price for ETH to Token trades with an exact input.")

    # Swaping 1 ETH to aBlock
    amount = 1
    eth_to_token = calc_eth_to_token_from_input(amount, ablock, ablock_dec)
    print(eth_to_token, "aBlock,", amount / eth_to_token, "ETH/aBlock,", (amount / eth_to_token) * usd_eth_rate,
          "USDT/aBlock")

    # Swaping 2 ETH to aBlock
    amount = 2
    eth_to_token = calc_eth_to_token_from_input(amount, ablock, ablock_dec)
    print(eth_to_token, "aBlock,", amount / eth_to_token, "ETH/aBlock,", (amount / eth_to_token) * usd_eth_rate,
          "USDT/aBlock")

    print("\nXBRIDGE SIDE:")
    my_tokens_balances = dx_get_tokens_balance()  # DICT
    if my_tokens_balances["BLOCK"] and my_tokens_balances["LTC"]:
        dex_orderbook_ask, dex_orderbook_bid = dxbottools.getorderbook("BLOCK", "LTC")
        print("BLOCK/LTC FIRST ORDERS FROM CENTER")
        print("SELL")
        print(dex_orderbook_ask[-1])
        print("BUY")
        print(dex_orderbook_bid[0])
        # DO MAGIC !
# MAIN<<
