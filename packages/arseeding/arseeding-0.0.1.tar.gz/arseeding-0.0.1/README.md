# everpay.py

Python sdk for [arseeding] (https://github.com/everFinance/arseeding).

Install with

```
pip install arseeding
```


- Quick start

upload python.pdf to arweave using arseeding

```python

# ar account
signer = everpay.ARSigner('ar_wallet.json')
data = open('go.pdf', 'rb').read()
o = send_and_pay(signer, 'usdc', data)
print(o)

```