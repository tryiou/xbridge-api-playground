from utils import dxbottools


class Market:
    MarketCount = 0

    def __init__(self, pair, ask, bid):
        self.pair = pair
        self.ask = ask
        self.bid = bid
        Market.MarketCount += 1


# FUNCTIONS>>

def dx_get_tokens_balance():
    balances = dxbottools.rpc_connection.dxGetTokenBalances()
    print("\nXbridge coins & balances:")
    if balances["Wallet"]:
        print("Local_Blocknet:", balances["Wallet"])
    # list each token in the sorted dict,
    for token in sorted(balances.keys()):
        if token != "Wallet":
            print(token, balances[token])
    print("")
    return balances  # Dict


def dx_get_my_markets(tokens_balances):
    # Create a list of Market objects
    markets = []
    print("Listing markets and retrieving orderbook:")
    # WE LOOP ALL OUR TOKENS TO PRODUCE TOKEN1
    for token1 in sorted(tokens_balances.keys()):
        # WE LOOP ALL OUR TOKENS AGAIN IN REVERSE MODE TO PRODUCE TOKEN2
        for token2 in reversed(sorted(tokens_balances.keys())):
            if token1 == token2:  # TESTED EVERY PAIR WITH TOKEN1/TOKEN2
                break
            elif token1 != "Wallet" and token2 != "Wallet":
                ask, bid = dxbottools.getorderbook(token1, token2)
                # ask[::-1] to reverse
                print(token1, token2, ":")
                if ask or bid:
                    print("Got orderbook")
                    markets.append(Market(token1 + "/" + token2, ask, bid))  # STORE DATA IN LIST
                else:
                    print("Orderbook empty")
    print("")
    return markets  # List of Market objects


# FUNCTIONS<<

# MAIN>>

# List local tokens names and balances
my_tokens_balances = dx_get_tokens_balance()  # DICT
# print(my_tokens_balances)

# List active markets from my_tokens_balances
my_markets = dx_get_my_markets(my_tokens_balances)
my_markets.sort(key=lambda x: x.pair)  # Sort object list by object.pair
for market in my_markets:
    # DISPLAY FIRST ORDERS AROUND CENTER PRICE ASK/BID
    print(market.pair, "FIRST SELL ORDER:")
    print("PRICE:", market.ask[-1][0], "QUANTITY:", market.ask[-1][1], "ID:", market.ask[-1][2])
    print(market.pair, "FIRST BUY ORDER:")
    print("PRICE:", market.bid[0][0], "QUANTITY:", market.bid[0][1], "ID:", market.bid[0][2])
    if float(market.ask[-1][0]) < float(market.bid[0][0]):
        print("POSSIBLE ARBITRAGE PROFIT ON", market.pair)
    print("")
print(Market.MarketCount, "active markets with available tokens")

# MAIN<<
