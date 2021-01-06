from list_tokens_balances_orderbooks import *
from web3 import Web3
from uniswap import Uniswap
from utils import dxsettings


# functions >>
def init_uniswap_wrapper():
    uni_wrapper = Uniswap(dxsettings.uni_address, dxsettings.uni_private_key,
                          provider=dxsettings.infura_url,
                          version=2)  # pass version=2 to use Uniswap v2
    return uni_wrapper


def conversion(rate1, rate2, decimal1, decimal2=10 ** 6):  # default decimal2 on usdt dec
    conv = ((1 / rate1) * (rate2 / decimal2)) * decimal1
    return conv


def eth_to_token_input(eth_amount, to_token, token_dec):
    return uniswap_wrapper.get_eth_token_input_price(to_token, eth_amount * 10 ** 18) / token_dec


# functions <<

print("\nUNISWAP SIDE:")
uniswap_wrapper = init_uniswap_wrapper()

usdt = Web3.toChecksumAddress("0xdac17f958d2ee523a2206206994597c13d831ec7")
usdt_rate = uniswap_wrapper.get_eth_token_input_price(usdt, 10 ** 18)
usdt_dec = 10 ** 6
eth_usd_rate = usdt_rate / usdt_dec
print("1 ETH =", eth_usd_rate, "USD")

wbtc = Web3.toChecksumAddress("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")
wbtc_rate = uniswap_wrapper.get_eth_token_input_price(wbtc, 10 ** 18)
wbtc_dec = 10 ** 8
print("wbtc_rate =", wbtc_rate)
print("1 WBTC =", conversion(wbtc_rate, usdt_rate, wbtc_dec), "USDT")

usdc = Web3.toChecksumAddress("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
usdc_rate = uniswap_wrapper.get_eth_token_input_price(usdc, 10 ** 18)
usdc_dec = 10 ** 6
print("1 USDC =", conversion(usdc_rate, usdt_rate, usdc_dec), "USDT")

ablock = Web3.toChecksumAddress("0xe692c8d72bd4ac7764090d54842a305546dd1de5")
ablock_rate = uniswap_wrapper.get_eth_token_input_price(ablock, 10 ** 18)
ablock_dec = 10 ** 8
print("1 aBLOCK =", conversion(ablock_rate, usdt_rate, ablock_dec), "USDT")

print("")

print("public price for ETH to Token trades with an exact input.")

print("Swaping 1 ETH to aBlock:")
eth_to_token = eth_to_token_input(1, ablock, ablock_dec)
print(eth_to_token, "aBlock,", 1 / eth_to_token, "ETH/aBlock,", (1 / eth_to_token) * eth_usd_rate, "USDT/aBlock")

print("Swapping 2 ETH to aBlock:")
eth_to_token = eth_to_token_input(2, ablock, ablock_dec)
print(eth_to_token, "aBlock,", 2 / eth_to_token, "ETH/aBlock,", (2 / eth_to_token) * eth_usd_rate, "USDT/aBlock")

print("\nXbridge side:")
my_tokens_balances = dx_get_tokens_balance()  # DICT
if my_tokens_balances["BLOCK"] and my_tokens_balances["LTC"]:
    dex_orderbook_ask, dex_orderbook_bid = dxbottools.getorderbook("BLOCK", "LTC")
    print(dex_orderbook_ask[-1])
    print(dex_orderbook_bid[0])
    #DO MAGIC !
