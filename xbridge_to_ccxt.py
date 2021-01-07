from xbridge_tokens_balances_orderbooks import *
import ccxt  # https://github.com/ccxt/ccxt/wiki/Manual for more info


def init_ccxt_instance(exchange, hostname=None):
    if exchange in ccxt.exchanges:
        exchange_class = getattr(ccxt, exchange)
        if hostname:
            instance = exchange_class({
                'apiKey': dxsettings.ccxt_cex_api,
                'secret': dxsettings.ccxt_cex_secret,
                'enableRateLimit': True,
                'rateLimit': 1000,
                'hostname': hostname,  # 'global.bittrex.com',
            })
        else:
            instance = exchange_class({
                'apiKey': dxsettings.ccxt_cex_api,
                'secret': dxsettings.ccxt_cex_secret,
                'enableRateLimit': True,
                'rateLimit': 1000,
            })
        instance.load_markets()
        return instance


def cex_calc_price_from_ticker(ticker):
    if ticker['ask'] > ticker['bid']:
        return ticker['ask'] - (ticker['ask'] - ticker['bid']) / 2
    elif ticker['ask'] < ticker['bid']:
        return ticker['bid'] - ticker['bid'] - ticker['ask'] / 2
    elif ticker['bid'] == ticker['ask']:
        return ticker['bid']


def dex_calc_price_from_orderbook(ask, bid):
    return float(ask[0][0]) - (float(ask[0][0]) - float(bid[0][0])) / 2


if __name__ == "__main__":
    # CEX SIDE>>
    cex_ccxt = init_ccxt_instance("bittrex", 'global.bittrex.com')
    cex_balances = cex_ccxt.fetch_free_balance()
    cex_block_ticker = cex_ccxt.fetch_ticker("BLOCK/BTC")
    cex_ltc_ticker = cex_ccxt.fetch_ticker("LTC/BTC")
    print("\nCEX side: ", cex_ccxt.name, "\n")
    print("BALANCES", cex_balances)
    print("BLOCK/BTC middle price is ", cex_calc_price_from_ticker(cex_block_ticker))
    print("BLOCK/LTC middle price is ", cex_calc_price_from_ticker(cex_ltc_ticker))
    # CEX SIDE<<

    # DEX SIDE>>
    print("\nDEX side: Xbridge")
    dex_balances = dx_get_tokens_balance()
    if "BTC" in dex_balances and "BLOCK" in dex_balances:
        dex_markets = dx_get_my_markets(dex_balances, "BTC")
        dex_blockbtc = [item for item in dex_markets if item.pair == "BLOCK/BTC"]
        print(len(dex_blockbtc))
        if dex_blockbtc:
            dex_blockbtc[0].ask.reverse()
            print(dex_blockbtc[0].ask)
            print(dex_blockbtc[0].bid)
            print("BLOCK/BTC middle price is", float(dex_blockbtc[0].ask[0][0]) - float(dex_blockbtc[0].bid[0][0]))
            print("")
    if "LTC" in dex_balances and "BLOCK" in dex_balances:
        dex_markets = dx_get_my_markets(dex_balances, "LTC")
        dex_blockltc = [item for item in dex_markets if item.pair == "BLOCK/LTC"]
        print(len(dex_blockltc))
        if dex_blockltc:
            dex_blockltc[0].ask.reverse()
            print(dex_blockltc[0].ask)
            print(dex_blockltc[0].bid)
            dex_block_ltc = dex_calc_price_from_orderbook(dex_blockltc[0].ask, dex_blockltc[0].bid)
            print("BLOCK/LTC middle price is", dex_block_ltc, "\nconverted to BLOCK/BTC =",
                  dex_block_ltc * cex_calc_price_from_ticker(cex_ltc_ticker))
            print("")
            # DO MAGIC!
    # DEX SIDE<<
