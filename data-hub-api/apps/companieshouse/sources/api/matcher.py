import requests

from ..matcher import BaseMatcher, FindingResult


class CHSource(BaseMatcher):
    NAME = constants.CH_SOURCES.CH.display
    CH_SEARCH_URL = 'https://api.companieshouse.gov.uk/search/companies?q={}'

    def _build_findings(self):
        url = self.CH_SEARCH_URL.format(self.name)
        results = requests.get(url, auth=(settings.CH_KEY, '')).json()['items']

        self.findings = []
        for result in results:
            ch_name = result['title']
            ch_postcode = self._get_ch_address(result)
            company_number = result['company_number']
            accuracy = self.get_accuracy(ch_name, ch_postcode)

            self.findings.append(
                FindingResult(
                    name=ch_name, postcode=ch_postcode,
                    accuracy=accuracy, company_number=company_number,
                    raw=result, source=constants.CH_SOURCES.CH
                )
            )
