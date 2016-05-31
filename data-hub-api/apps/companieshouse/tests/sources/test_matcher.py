from django.test.testcases import TestCase

from companieshouse.sources.matcher import BaseMatcher, FindingResult


class MyMatcher(BaseMatcher):
    def _set_findings(self, findings):
        self.findings = findings


class BaseMatcherTestCase(TestCase):
    NAME = 'some company'
    POSTCODE = 'SW1A 1AA'

    def setUp(self):
        self.matcher = MyMatcher(
            name=self.NAME, postcode=self.POSTCODE
        )

    def test_without_findings(self):
        pass

    def test_with_one_finding(self):
        pass

    def test_with_some_findings(self):
        pass
