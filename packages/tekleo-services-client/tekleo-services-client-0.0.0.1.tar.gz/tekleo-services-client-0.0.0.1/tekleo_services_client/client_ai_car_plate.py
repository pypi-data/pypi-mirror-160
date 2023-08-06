from pydantic import parse_obj_as
import requests
from injectable import injectable, Autowired, autowired
from tekleo_common_message_protocol import PingOutput, ImageUrl, ImageBase64, OdOutput
from tekleo_common_utils import UtilsMethod



@injectable
class ClientAiCarPlate:
    @autowired
    def __init__(self, utils_method: Autowired(UtilsMethod)):
        self.utils_method = utils_method
        self.base_url = ''

    def ping(self, base_url: str = '-', timeout_in_seconds: int = 10) -> PingOutput:
        return self.utils_method.execute_with_retries(self._ping_call, [], {'base_url': base_url, 'timeout_in_seconds': timeout_in_seconds}, max_number_of_tries=1)

    def _ping_call(self, base_url: str = '-', timeout_in_seconds: int = 10) -> PingOutput:
        if base_url == '-':
            base_url = self.base_url
        url = base_url + "/ping"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers, timeout=timeout_in_seconds)
        response.raise_for_status()
        response_json = response.json()
        return PingOutput.parse_obj(response_json)

    def predict_url(self, input: ImageUrl, base_url: str = '-', timeout_in_seconds: int = 90) -> OdOutput:
        return self.utils_method.execute_with_retries(self._predict_url_call, [input], {'base_url': base_url, 'timeout_in_seconds': timeout_in_seconds}, max_number_of_tries=1)

    def _predict_url_call(self, input: ImageUrl, base_url: str = '-', timeout_in_seconds: int = 60) -> OdOutput:
        if base_url == '-':
            base_url = self.base_url
        url = base_url + "/predict/url"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=input.json(), headers=headers, timeout=timeout_in_seconds)
        response.raise_for_status()
        response_json = response.json()
        return OdOutput.parse_obj(response_json)

    def predict_base64(self, input: ImageBase64, base_url: str = '-', timeout_in_seconds: int = 90) -> OdOutput:
        return self.utils_method.execute_with_retries(self._predict_base64_call, [input], {'base_url': base_url, 'timeout_in_seconds': timeout_in_seconds}, max_number_of_tries=1)

    def _predict_base64_call(self, input: ImageBase64, base_url: str = '-', timeout_in_seconds: int = 60) -> OdOutput:
        if base_url == '-':
            base_url = self.base_url
        url = base_url + "/predict/base64"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=input.json(), headers=headers, timeout=timeout_in_seconds)
        response.raise_for_status()
        response_json = response.json()
        return OdOutput.parse_obj(response_json)
