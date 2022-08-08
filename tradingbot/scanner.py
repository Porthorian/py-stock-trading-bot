import logging
import time
import alpaca_trade_api as tradeapi

class Scanner:
	def __init__(self, api_key: str, api_secret: str, base_url: str):
		self.api = tradeapi.REST(
			key_id=api_key,
			secret_key=api_secret,
			base_url=tradeapi.common.URL(base_url)
		)
		self.__set_account()

	def __set_account(self):
		self.account = self.api.get_account()
		logging.debug(self.account)

	def get_potentials(self):
		active_assets = self.api.list_assets(status='active')
		iterators = {}
		assets = {}
		for asset in active_assets:
			if asset.exchange not in ['NASDAQ', 'NYSE'] or not asset.tradable: continue
			iterators[asset.symbol] = self.api.get_bars_iter(asset.symbol, tradeapi.TimeFrame.Minute)
			assets[asset.symbol] = asset

		high_volume_stocks = {}

		stop = 0
		for symbol in iterators:
			logging.debug('Checking %s for high volume' % symbol)
			bars = iterators[symbol]
			total_volume = 0
			for bar in bars:
				total_volume += bar.v

			logging.debug('%s total volume %s' % (symbol, str(total_volume)))

			if total_volume >= 5_000_000:
				high_volume_stocks[symbol] = total_volume

			stop += 1
			if stop >= 50:
				logging.debug('Sleeping')
				time.sleep(10)
				stop = 0

		logging.info(high_volume_stocks)
