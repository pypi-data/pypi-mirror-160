# xamino

**xamino** is a very simple aminoapps library.

```python
>>> import xamino
>>> client = xamino.Client()
>>> client.login(email=email, password=password)
#NOTE: To access subclient
subclient = subclient.SubClient(ndcId=ndcId, accountInfo=client.accountInfo)
```