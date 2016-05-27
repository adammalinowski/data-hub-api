from ..matcher import BaseMatcher, FindingResult


class DueDilSource(BaseMatcher):
    NAME = constants.CH_SOURCES.DUEDIL.display
    DUEL_SEARCH_URL = 'http://api.duedil.com/open/search?q={}&api_key={}'
    CH_COMPANY_URL = 'https://api.companieshouse.gov.uk/company/{}'

    def get_ch_postcode(self, company_number):
        url = self.CH_COMPANY_URL.format(company_number)
        response = requests.get(url, auth=(settings.CH_KEY, ''))
        time.sleep(0.5)
        if not response.ok:
            return (None, None)
        result = response.json()
        return (result, self._get_ch_address(result))

    def _build_findings(self):
        self.findings = []

        url = self.DUEL_SEARCH_URL.format(self.name, settings.DUEDIL_KEY)
        response = requests.get(url)
        if not response.ok:
            return

        results = response.json()['response']['data']

        for result in results:
            dd_name = result['name']
            company_number = result['company_number']
            ch_result, ch_postcode = self.get_ch_postcode(company_number)
            accuracy = self.get_accuracy(dd_name, ch_postcode)

            if ch_result:
                raw = ch_result
                source = constants.CH_SOURCES.CH
            else:
                raw = result
                source = constants.CH_SOURCES.DUEDIL

            self.findings.append(
                FindingResult(
                    name=dd_name, postcode=ch_postcode,
                    accuracy=accuracy, company_number=company_number,
                    raw=raw, source=source
                )
            )
