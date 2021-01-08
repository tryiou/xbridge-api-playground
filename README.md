# xbridge-api-playground
Blocknet xbridge api usage examples

More information here:
https://docs.blocknet.co/
<br />
https://api.blocknet.co/#xbridge-api

uniswap-python wrapper:
https://github.com/shanefontaine/uniswap-python

ccxt:
https://github.com/ccxt/ccxt

need python3+, pip, git

usage:
<pre>
clone repo with:
  git clone https://github.com/tryiou/xbridge-api-playground.git
or download/extract repo from web, then:
  cd xbridge-api-playground
install requirements with:
  pip install -r requirements.txt   #(pip3 on ubuntu20)
edit settings:
  utils/dxsettings.py	#set your blocknet rpcport/rpcuser/rpcpassword,
  			#(optionnal) infura endpoint/address/privatekey,
  			#(optionnal) ccxt supported exchange name/api/secret.
run one of the scripts with:
  python xbridge_tokens_balances_orderbooks.py   #(python3 on ubuntu20)
  or
  python xbridge_to_uniswap.py 
  or
  python xbridge_to_ccxt.py
</pre>
