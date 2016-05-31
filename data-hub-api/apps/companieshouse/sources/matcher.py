import re
from collections import namedtuple

EXCLUDE_NAME_PARTS = re.compile(r"(?i)\bltd\b|\blimited\b|\binc\b|\bllc\b|\bthe\b|\.")


def clean_postcode(postcode):
    """
    Returns `postcode` lowercase without spaces so that it can be used for comparisons.
    """
    if not postcode:
        return postcode
    return postcode.lower().replace(' ', '').strip()


def clean_name(name):
    """
    Returns `name` lowercase without common parts and extra spaces so that it can be used for comparisons.
    """
    if not name:
        return name

    cleaned_name = name.lower()  # lowercase
    cleaned_name = EXCLUDE_NAME_PARTS.sub('', cleaned_name)  # remove words
    return ' '.join(cleaned_name.split())  # remove unnecessary spaces


class SimilarityCalculator(object):
    """
    Used to calculate the similarity proximity between 2 records.
    e.g.

        calc = SimilarityCalculator()
        calc.analyse_names(name1, name2)
        calc.analyse_postcodes(postcode1, postcode2)

        proximity = calc.get_proximity()

    To have an accurate value, it's always better to analyse both names and postcodes.
    """
    STEPS = 2  # tot number of steps supported atm. 2 == name and postcode

    def __init__(self):
        self.steps = 0
        self.is_bound = False  # True if at leasat one analyse_ has been called

    def analyse_names(self, name1, name2):
        """
        Analysing names helps determine a more accurate proximity contributing 0.5 at most to the final value.
        Note, this is a very naive approach but could be enough. TBD
        """
        self.is_bound = True
        cleaned_name1 = clean_name(name1)
        cleaned_name2 = clean_name(name2)

        if cleaned_name1 == cleaned_name2:
            self.steps += 1
            return

        # if at least one of the parts between the 2 strings are the same...
        if set(cleaned_name1.split()).intersection(set(cleaned_name2.split())):
            self.steps += 0.5

    def analyse_postcodes(self, postcode1, postcode2):
        """
        Analysing postcodes helps determine a more accurate proximity contributing 0.5 at most to the final value.
        Note, this is a very naive approach but could be enough. TBD
        """
        self.is_bound = True
        cleaned_postcode1 = clean_postcode(postcode1) or ''
        cleaned_postcode2 = clean_postcode(postcode2) or ''

        if cleaned_postcode1 == cleaned_postcode2:
            self.steps += 1
            return

        if cleaned_postcode1 and cleaned_postcode1[:3] == cleaned_postcode2[:3]:
            self.steps += 0.5

    def get_proximity(self):
        """
        Returns a value x so that
            0 <= x <= 1

        When considering possible values:
            - 0: the objects are not similar at all
            - 0.25: the objects are just slightly similar. It's probably not wise considering them similar at all.
            - 0.5: the objects are somewhat similar. It might be OK to consider them similar.
            - 0.75: the objects are similar.
            - 1: the objects are basically the same.
        """
        assert self.is_bound
        return self.steps / self.STEPS


FindingResult = namedtuple(
    'FindingResult',
    ['company_number', 'name', 'postcode', 'proximity', 'raw']
)


class BaseMatcher(object):
    """
    Base Matcher class to be subclassed to add actual logic.

    e.g.
        matcher = MyMatcher(name, postcode)
        best_match = matcher.find()  # returns the best match, an instance of FindingResult
        matcher.findings  # if you want the full list considered internally for debug purposes
    """
    def __init__(self, name, postcode):
        super(BaseMatcher, self).__init__()
        self.name = name
        self.postcode = postcode
        self.findings = None

    def _get_similarity_proximity(self, other_name, other_postcode):
        similarity_calc = SimilarityCalculator()
        similarity_calc.analyse_names(self.name, other_name)
        similarity_calc.analyse_postcodes(self.postcode, other_postcode)
        return similarity_calc.get_proximity()

    def _choose_best_finding(self):
        assert self.findings != None  # noqa

        if not self.findings:
            return None

        return max(self.findings, key=lambda x: x.proximity)

    def _get_ch_address(self, ch_data):
        for prop in ['address', 'registered_office_address']:
            if prop in ch_data:
                return ch_data.get(prop, {}).get('postal_code')
        return None

    def _build_findings(self):
        """
        To be overridden when subclassing.
        """
        pass

    def find(self):
        """
        Builds the findings and returns the best match which is an instance of FindingResult.
        """
        self._build_findings()
        return self._choose_best_finding()
