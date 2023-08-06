from datetime import datetime
import json
from typing import Optional
import requests
from urllib.parse import ParseResult, quote, urlencode, urlparse

from cexpay.api.security import SignatureCalculator

class OrderDepositTransaction:
	@staticmethod
	def from_json(json_dict: dict):
		assert isinstance(json_dict, dict)
		# Parse json dict according to https://developers.cexpay.io/processing-api/#fetch-order
		deposit_id = json_dict["depositId"]
		status = json_dict["status"]
		confirmations = json_dict["confirmations"]
		amount = json_dict["amount"]
		tx_hash = json_dict["txHash"]
		tx_explorer_url = json_dict["txExplorerUrl"]
		created_at = json_dict["createdAt"]
		updated_at = json_dict["updatedAt"]
		return OrderDepositTransaction(
			deposit_id = deposit_id, status = status,
			confirmations = confirmations, amount = amount,
			tx_hash = tx_hash, tx_explorer_url = tx_explorer_url,
			created_at = created_at, updated_at = updated_at
		)

	def __init__(self, deposit_id: str, status: str, confirmations: int, amount: str, tx_hash: str, tx_explorer_url: str, created_at: str, updated_at: str) -> None:
		self.deposit_id = deposit_id
		self.status = status
		self.confirmations = confirmations
		self.amount = amount
		self.tx_hash = tx_hash
		self.tx_explorer_url = tx_explorer_url
		self.created_at = created_at
		self.updated_at = updated_at

class OrderDeposit:
	@staticmethod
	def from_json(json_dict: dict):
		assert isinstance(json_dict, dict)
		# Parse json dict according to https://developers.cexpay.io/processing-api/#fetch-order
		kind = json_dict["kind"]
		network = json_dict["network"]
		address = json_dict["address"]
		address_explorer_url = json_dict["addressExplorerUrl"]
		paid_amount = json_dict["paidAmount"]
		remain_amount = json_dict["remainAmount"]
		payment_uri = json_dict["paymentUri"]
		transactions_raw = json_dict["transactions"]
		transactions = [OrderDepositTransaction.from_json(x) for x in transactions_raw]
		return OrderDeposit(
			kind = kind, network = network,
			address = address, address_explorer_url = address_explorer_url,
			paid_amount = paid_amount, remain_amount = remain_amount,
			payment_uri = payment_uri, transactions = transactions
		)

	def __init__(
		self, kind: str, network: str, address: str, address_explorer_url: str,
		paid_amount: str, remain_amount: str, payment_uri: str,
		transactions: list[OrderDepositTransaction]
	) -> None:
		self.kind = kind
		self.network = network
		self.address = address
		self.address_explorer_url = address_explorer_url
		self.paid_amount = paid_amount
		self.remain_amount = remain_amount
		self.payment_uri = payment_uri
		self.transactions = transactions

class OrderAccount:
	@staticmethod
	def from_json(json_dict: dict):
		assert isinstance(json_dict, dict)
		# Parse json dict according to https://developers.cexpay.io/processing-api/#fetch-order
		currency = json_dict["currency"]
		amount = json_dict["amount"]
		account_id = json_dict["accountId"]
		return OrderAccount(currency, amount, account_id)

	def __init__(self, currency: str, amount: str, account_id: str) -> None:
		self.currency = currency
		self.amount = amount
		self.accountId = account_id

class Order:
	@staticmethod
	def from_json(json_dict: dict):
		assert isinstance(json_dict, dict)

		# Parse json dict according to https://developers.cexpay.io/processing-api/#fetch-order

		order_id = json_dict["orderId"]
		client_order_id = json_dict["clientOrderId"]
		client_order_tag = json_dict["clientOrderTag"]

		return Order(
			order_id = order_id,
			client_order_id = client_order_id,
			client_order_tag = client_order_tag,
			status = json_dict["status"],
			state = json_dict["state"],
			instrument = json_dict["instrument"],
			from_ = OrderAccount.from_json(json_dict["from"]),
			to_ = OrderAccount.from_json(json_dict["to"]),
			deposit = OrderDeposit.from_json(json_dict["deposit"]),
			paid_status = json_dict["paidStatus"],
			created_at = json_dict["createdAt"],
			updated_at = json_dict["updatedAt"],
			expired_at = json_dict["expiredAt"]
		)

	def __init__(self,
		order_id: str,
		client_order_id: str,
		status, state, paid_status,
		from_: OrderAccount, to_: OrderAccount,
		deposit: OrderDeposit,
		instrument: str, client_order_tag: Optional[str],
		created_at: str, updated_at: str, expired_at: str
	) -> None:
		self.order_id = order_id
		self.client_order_id = client_order_id
		self.client_order_tag = client_order_tag
		self.status = status
		self.state = state
		self.paid_status = paid_status
		self.instrument = instrument
		setattr(self, "from", from_)
		self.to = to_
		self.deposit = deposit
		self.created_at = created_at
		self.updated_at = updated_at
		self.expired_at = expired_at


class BaseException(Exception):
	pass

class BusinessException(BaseException):
	pass

class NotFoundException(BusinessException):
	pass

class ApiV2:
	'''
	See https://developers.cexpay.io/processing-api/
	'''

	def __init__(self, key: str, passphrase: str, secret: str, url: Optional[str] = "https://api.cexpay.io", ssl_ca_cert: Optional[str] = None) -> None:
		assert isinstance(key, str)
		assert isinstance(passphrase, str)
		assert isinstance(secret, str)
		assert url is None or isinstance(url, str)
		assert ssl_ca_cert is None or isinstance(ssl_ca_cert, str)

		self._key = key
		self._access_passphrase = passphrase
		self._signature_calculator = SignatureCalculator(secret)
		if(url is None):
			url = "https://api.cexpay.io"
		self._url = urlparse(url)
		self._ssl_ca_cert = ssl_ca_cert

	def order_create(self, client_order_id: str,
		from_currency: str, to_currency: str,
		from_amount = None, to_amount = None,
		from_account_id = None, to_account_id = None,
		instrument = None, client_order_tag = None
	) -> Order:
		payload = {
			"clientOrderId": client_order_id,
			"from": {"currency": from_currency},
			"to": {"currency": to_currency}
		}

		if instrument is not None:
			payload["instrument"] = instrument
		if client_order_tag is not None:
			payload["client_order_tag"] = client_order_tag
		if from_amount is not None:
			payload["from"]["amount"] = from_amount
		if to_amount is not None:
			payload["to"]["amount"] = to_amount
		if from_account_id is not None:
			payload["from"]["accountId"] = from_account_id
		if to_account_id is not None:
			payload["to"]["accountId"] = to_account_id

		response_data = self._do_post("/v2/order", payload)

		return Order.from_json(response_data)

	def order_fetch(self, order_id: str, use_merchant_family: bool = False) -> Order:
		encoded_order_id = quote(order_id, safe="")

		query_args = {}
		if use_merchant_family:
			query_args["useMerchantFamily"] = "true"

		response_data = self._do_get("/v2/order/" + encoded_order_id, query_args=query_args)

		return Order.from_json(response_data)

	def order_fetch_by_address(self, address: str, use_merchant_family: bool = False) -> Order:
		encoded_address = quote(address, safe="")
		
		query_args = {}
		if use_merchant_family:
			query_args["useMerchantFamily"] = "true"

		response_data = self._do_get("/v2/order/by-address/" + encoded_address, query_args=query_args)
		assert isinstance(response_data, list)

		return response_data

	def order_fetch_by_tx(self, order_tx: str, use_merchant_family: bool = False) -> Order:
		encoded_order_tx = quote(order_tx, safe="")

		query_args = {}
		if use_merchant_family:
			query_args["useMerchantFamily"] = "true"

		response_data = self._do_get("/v2/order/by-tx/" + encoded_order_tx, query_args=query_args)
		assert isinstance(response_data, list)

		return response_data

	def order_fetch_by_client_id(self, client_order_id: str, use_merchant_family: bool = False) -> Order:
		query_args = {
			"clientOrderId": client_order_id
		}
		if use_merchant_family:
			query_args["useMerchantFamily"] = "true"

		response_data = self._do_get("/v2/order", query_args=query_args)
		if isinstance(response_data, list) and len(response_data) == 1:
			return Order.from_json(response_data[0])
		
		raise NotFoundException("No order found by identifier '%s'" % client_order_id)


	def _parse_response(self, response: requests.Response, http_method: str, sign_url_part: str) -> dict:
		response_content_type = response.headers.get("Content-Type")

		if response.status_code >= 400:
			error_reason_phrase = response.headers["CP-REASON-PHRASE"]
			raise NotFoundException("Unexpected response status. Reason: %s" % error_reason_phrase)

		if response_content_type is not None and response_content_type != "application/json":
			raise Exception("Unexpected Content-Type: %s" % response_content_type)

		response_access_key = response.headers["CP-ACCESS-KEY"]
		if response_access_key is None:
			raise Exception("Unexpected response. CP-ACCESS-KEY was not provided. Attack?!")
		if self._key != response_access_key:
			raise Exception("Wrong response access key")

		response_timestamp = response.headers["CP-ACCESS-TIMESTAMP"]
		if response_timestamp is None:
			raise Exception("Unexpected response. CP-ACCESS-TIMESTAMP was not provided. Attack?!")

		response_signature = response.headers["CP-ACCESS-SIGN"]
		if response_signature is None:
			raise Exception("Unexpected response. CP-ACCESS-SIGN was not provided. Attack?!")

		response_data_raw: bytes = response.content

		response_expected_signature = self._signature_calculator.sing(response_timestamp, http_method, sign_url_part, response_data_raw)
		if response_signature != response_expected_signature:
			raise Exception("Wrong response signature")

		response_data = json.loads(response_data_raw)

		return response_data

	def _do_get(self, url_path: str, query_args: Optional[dict] = None, headers: dict[str,str] = None) -> dict:
		query: Optional[str] = None
		if query_args is not None:
			query = urlencode(query_args, doseq=True)
		url: ParseResult = self._url._replace(
			path = url_path,
			query = query
		)
		timestamp: str = str(datetime.utcnow().timestamp()*1000)
		http_method = "GET"
		sign_url_part = url.path
		if url.query is not None and url.query != "":
			sign_url_part = url.path + "?" + url.query

		signature: str = self._signature_calculator.sing(timestamp, http_method, sign_url_part)

		if headers is None:
			headers = {}

		headers = {
			**headers,
			"Content-Type": "application/json",
			"CP-ACCESS-KEY": self._key,
			"CP-ACCESS-TIMESTAMP": timestamp,
			"CP-ACCESS-PASSPHRASE": self._access_passphrase,
			"CP-ACCESS-SIGN": signature
		}

		response: requests.Response = requests.get(
			url.geturl(),
			headers = headers,
			verify = self._ssl_ca_cert
		)

		response_data: dict = self._parse_response(response, http_method, sign_url_part)
		
		return response_data

	def _do_post(self, url_path: str, payload: dict) -> dict:
		payload_raw: bytes = json.dumps(payload).encode("UTF-8")
		url: ParseResult = self._url._replace(
			path = url_path
		)
		timestamp: str = str(datetime.utcnow().timestamp()*1000)
		http_method = "POST"
		sign_url_part = url.path

		signature: str = self._signature_calculator.sing(timestamp, http_method, sign_url_part, payload_raw)

		response: requests.Response = requests.post(
			url.geturl(),
			headers = {
				"Content-Type": "application/json",
				"CP-ACCESS-KEY": self._key,
				"CP-ACCESS-TIMESTAMP": timestamp,
				"CP-ACCESS-PASSPHRASE": self._access_passphrase,
				"CP-ACCESS-SIGN": signature
			},
			data = payload_raw,
			verify = self._ssl_ca_cert
		)

		response_data: dict = self._parse_response(response, http_method, sign_url_part)
		
		return response_data
