# xbridge-api-playground
Blocknet xbridge usage examples

need python3+,pip,git

usage:
<pre>
clone repo with:
  git clone https://github.com/tryiou/xbridge-api-playground.git
or download/extract repo from web, then:
  cd xbridge-api-playground
install requirements with:
  pip install -r requirements.txt   #(pip3 on ubuntu20)
edit settings:
  utils/dxsettings.py and set your blocknet rpcport/rpcuser/rpcpassword,
  (optionnal) infura endpoint/info,
  (optionnal) and/or ccxt supported exchange data.
run one of the scripts with:
  python list_tokens_balances_orderbooks.py   #(python3 on ubuntu20)
  or
  python xbridge_to_uniswap.py 
</pre>
