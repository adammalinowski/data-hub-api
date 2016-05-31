from slumber.exceptions import HttpNotFoundError

from ..api import api as companieshouse_api

from ..matcher import BaseMatcher, FindingResult
from . import api


class DueDilSource(BaseMatcher):
    """
    DueDil API Matcher which uses the DueDil Api to find the best match.

    e.g.
        matcher = CHMatcher(name, postcode)
        best_match = matcher.find()  # returns the best match, an instance of FindingResult
        matcher.findings  # if you want the full list considered internally for debug purposes
    """

    def _get_ch_postcode(self, company_number):
        try:
            result = companieshouse_api.company.get(company_number)
        except HttpNotFoundError:
            return (None, None)
        return (result, self._get_ch_address(result))

    def _build_findings(self):
        self.findings = []

        try:
            results = api.search(q=self.name)
        except HttpNotFoundError:
            return

        for result in results:
            dd_name = result['name']
            company_number = result['company_number']
            ch_result, ch_postcode = self._get_ch_postcode(company_number)
            proximity = self.get_similarity_proximity(dd_name, ch_postcode)

            if ch_result:
                raw = ch_result
            else:
                raw = result

            self.findings.append(
                FindingResult(
                    name=dd_name, postcode=ch_postcode,
                    proximity=proximity, company_number=company_number,
                    raw=raw
                )
            )
