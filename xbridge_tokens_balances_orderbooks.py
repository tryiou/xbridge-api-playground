from utils import dxbottools  # https://api.blocknet.co/#xbridge-api for more info
from utils import dxsettings
import json


class Market:
    MarketCount = 0

    def __init__(self, pair, m_ask=[], m_bid=[]):
        self.pair = pair
        self.ask = m_ask
        self.bid = m_bid
        if self.ask or self.bid:
            Market.MarketCount += 1


# FUNCTIONS>>
def dx_get_tokens_balance():
    balances = dxbottools.rpc_connection.dxGetTokenBalances()
    print("\nXbridge coins & balances:")
    if "Wallet" in balances:
        print("Local_Blocknet:", balances["Wallet"])
    # list each token in the sorted dict,
    for token in sorted(balances.keys()):
        if token != "Wallet":
            print(token, balances[token])
    print("")
    return balances  # Dict


def dx_get_my_markets(tokens_balances, preferred_token2="LTC"):  # Prioritize this preferred_token2 as coin2 if possible
    # Create a list of Market objects
    buffer_markets = []
    final_markets = []
    print("Listing DX markets and retrieving orderbook:")
    # WE LOOP ALL OUR TOKENS TO PRODUCE TOKEN1
    for token1 in sorted(tokens_balances.keys()):
        # WE LOOP ALL OUR TOKENS AGAIN TO PRODUCE TOKEN2
        for token2 in sorted(tokens_balances.keys()):
            if token1 != token2:
                # TEST IF PAIR(OR ITS REVERSE) IS ALREADY PRESENT IN OUR BUFFER LIST
                pairing_exist = any(
                    x for x in buffer_markets if x.pair == token1 + "/" + token2 or x.pair == token2 + "/" + token1)
                if not pairing_exist:
                    buffer_markets.append(Market(token1 + "/" + token2))
                    if token1 != "Wallet" and token2 != "Wallet":
                        if token1 == preferred_token2:  # REVERSE THE PAIR IF NEEDED TO SELECT PREFERRED TOKEN2
                            t1 = token2
                            t2 = token1
                        else:
                            t1 = token1
                            t2 = token2
                        f_ask, f_bid = dxbottools.getorderbook(t1, t2)
                        print(t1 + "/" + t2, ":")
                        if f_ask or f_bid:
                            # STORE DATA IN LIST
                            print("Got orderbook")
                            final_markets.append(Market(t1 + "/" + t2, f_ask, f_bid))
                        else:
                            print("Orderbook empty")
    print("")
    return final_markets  # List of Market objects


# FUNCTIONS<<

# MAIN>>
if __name__ == "__main__":
    # List local tokens names and balances
    my_tokens_balances = dx_get_tokens_balance()  # DICT
    # print(my_tokens_balances)

    # List active markets from my_tokens_balances
    my_markets = dx_get_my_markets(my_tokens_balances)
    my_markets.sort(key=lambda x: x.pair)  # Sort object list by object.pair

    print("DISPLAY FIRST ORDERS AROUND CENTER PRICE ASK/BID:\n")
    for market in my_markets:

        print(market.pair, "FIRST SELL ORDER:")
        if market.ask:
            print("PRICE:", market.ask[-1][0], "QUANTITY:", market.ask[-1][1], "ID:", market.ask[-1][2])
        else:
            print("NONE")

        print(market.pair, "FIRST BUY ORDER:")
        if market.bid:
            print("PRICE:", market.bid[0][0], "QUANTITY:", market.bid[0][1], "ID:", market.bid[0][2])
        else:
            print("NONE")
        if market.ask and market.bid and float(market.ask[-1][0]) < float(market.bid[0][0]):
            print("POSSIBLE ARBITRAGE PROFIT ON", market.pair)
            # DO MAGIC !
        print("")

    print(Market.MarketCount, "active markets with available tokens")

# MAIN<<
