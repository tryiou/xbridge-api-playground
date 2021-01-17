from utils import dxbottools  # https://api.blocknet.co/#xbridge-api for more info
import time
import datetime


class Market:
    MarketCount = 0

    def __init__(self, pair, m_ask=[], m_bid=[]):
        self.pair = pair
        self.ask = m_ask
        self.bid = m_bid
        if self.ask or self.bid:
            Market.MarketCount += 1


global rpc_call_count


# FUNCTIONS>>
def dx_get_tokens_balance():
    global rpc_call_count
    balances = dxbottools.rpc_connection.dxGetTokenBalances()
    rpc_call_count += 1
    return balances  # Dict


def dx_get_my_markets(tokens_balances, preferred_token2="LTC"):  # Prioritize this preferred_token2 as coin2 if possible
    global rpc_call_count
    # Create a list of Market objects
    buffer_markets = []
    final_markets = []
    # WE LOOP ALL OUR TOKENS TO PRODUCE TOKEN1
    for token1 in sorted(tokens_balances.keys()):
        # WE LOOP ALL OUR TOKENS AGAIN TO PRODUCE TOKEN2
        for token2 in sorted(tokens_balances.keys()):
            if token1 != token2:
                # test IF PAIR(OR ITS REVERSE) IS ALREADY PRESENT IN OUR BUFFER LIST
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
                        rpc_call_count += 1
                        if f_ask or f_bid:
                            final_markets.append(Market(t1 + "/" + t2, f_ask, f_bid))
    return final_markets  # List of Market objects
# FUNCTIONS<<



# MAIN>>
if __name__ == "__main__":
    list_tokens_balances = []
    err_count = 0
    count = 0
    print("DATE , WALLETS , XBRIDGE_CALLS, EXEC_TIMER")
    while 1:
        try:
            rpc_call_count = 0
            timer = time.time()
            my_tokens_balances = dx_get_tokens_balance()  # DICT
            my_markets = dx_get_my_markets(my_tokens_balances)
            exec_time = time.time() - timer
            count += 1
            my_tokens_balances = sorted(my_tokens_balances)
            list_tokens_balances.append(
                [datetime.datetime.utcnow().strftime("%H:%M:%S"), my_tokens_balances, rpc_call_count, exec_time])
            print(list_tokens_balances[-1])
        except Exception as error:
            print(type(error), error)
            err_count += 1
            time.sleep(5)
            if err_count == 50:
                exit()
        else:
            time.sleep(5)
# MAIN<<
