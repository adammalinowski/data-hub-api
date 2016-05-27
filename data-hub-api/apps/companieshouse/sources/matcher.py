import re
from collections import namedtuple

EXCLUDE_NAME_PARTS = re.compile(r"(?i)\bltd\b|\blimited\b|\binc\b|\bllc\b|\bthe\b|\.")


def clean_postcode(postcode):
    if not postcode:
        return postcode
    return postcode.lower().replace(' ', '').strip()


def clean_name(name):
    cleaned_name = name.lower()  # lowercase
    cleaned_name = EXCLUDE_NAME_PARTS.sub('', cleaned_name)  # remove words
    return ''.join(cleaned_name.split())  # remove unnecessary spaces


class AccuracyCalculator(object):
    def __init__(self):
        self.accuracy_steps = 0

    def analyse_names(self, name1, name2):
        cleaned_name1 = clean_name(name1)
        cleaned_name2 = clean_name(name2)

        if cleaned_name1 == cleaned_name2:
            self.accuracy_steps += 1
        else:
            self.accuracy_steps += 0.5

    def analyse_postcodes(self, postcode1, postcode2):
        cleaned_postcode1 = clean_postcode(postcode1) or ''
        cleaned_postcode2 = clean_postcode(postcode2) or ''

        if cleaned_postcode1 == cleaned_postcode2:
            self.accuracy_steps += 1
        elif cleaned_postcode1 and cleaned_postcode1[:3] == cleaned_postcode2[:3]:
            self.accuracy_steps += 0.5

    def get_accuracy(self):
        assert self.accuracy_steps > 0
        return self.accuracy_steps / 2


FindingResult = namedtuple(
    'FindingResult',
    ['company_number', 'name', 'postcode', 'accuracy', 'raw', 'source']
)


class BaseMatcher(object):
    def __init__(self, name, postcode):
        super(BaseMatcher, self).__init__()
        self.name = name
        self.postcode = postcode
        self.findings = None

    def _get_accuracy(self, other_name, other_postcode):
        accuracy_calc = AccuracyCalculator()
        accuracy_calc.analyse_names(self.name, other_name)
        accuracy_calc.analyse_postcodes(self.postcode, other_postcode)
        return accuracy_calc.get_accuracy()

    def _choose_best_finding(self):
        assert self.findings != None  # noqa

        finding = None
        if len(self.findings) >= 1:
            finding = max(self.findings, key=lambda x: x.accuracy)

        return finding

    def _get_ch_address(self, ch_data):
        for prop in ['address', 'registered_office_address']:
            if prop in ch_data:
                return ch_data.get(prop, {}).get('postal_code')
        return None

    def _build_findings(self):
        pass

    def find(self):
        self._build_findings()
        return self._choose_best_finding()
