import datetime

from django.test.testcases import TestCase

from companieshouse.sources.api.matcher import CHMatcher


class APIMatcherTestCase(TestCase):
    def test_without_findings(self):
        pass

    def test_with_one_finding(self):
        """
        name = 'SOPRANO BELLA LIMITED'
        postcode = 'CM21 0LR'

        matcher = CHMatcher(name, postcode)
        best_match = matcher.find()
        """

    def test_with_more_findings(self):
        pass
