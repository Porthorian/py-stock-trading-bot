import logging
import alpaca_trade_api as tradeapi
import json

class Scanner:
	def __init__(self):
		file = open('keys.json')
		attributes = json.load(file)
		file.close()

		self.api = tradeapi.REST(
			key_id=attributes['ApiKey'],
			secret_key=attributes['ApiSecret'],
			base_url=tradeapi.common.URL(attributes['BaseURL'])
		)
		self.__set_account()

	def __set_account(self):
		self.account = self.api.get_account()
		logging.debug(self.account)

	def get_potentials(self):
		active_assets = self.api.list_assets(status='active')
		for asset in active_assets:
			if asset.exchange not in ['NASDAQ', 'NYSE']: continue
			logging.debug(asset)
