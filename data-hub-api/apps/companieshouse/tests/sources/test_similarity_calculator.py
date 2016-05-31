from django.test.testcases import TestCase

from companieshouse.sources.matcher import SimilarityCalculator, clean_postcode, clean_name


class CleanPostcodeTestCase(TestCase):
    def test_empty(self):
        self.assertEqual(
            clean_postcode(''),
            ''
        )

    def test_None(self):
        self.assertEqual(
            clean_postcode(None),
            None
        )

    def test_correct(self):
        self.assertEqual(
            clean_postcode('SW1A 1AA'),
            'sw1a1aa'
        )

    def test_with_extra_spaces(self):
        self.assertEqual(
            clean_postcode(' SW1A    1 A A    '),
            'sw1a1aa'
        )


class CleanNameTestCase(TestCase):
    def test_empty(self):
        self.assertEqual(
            clean_name(''),
            ''
        )

    def test_None(self):
        self.assertEqual(
            clean_name(None),
            None
        )

    def test_correct(self):
        self.assertEqual(
            clean_name('My company'),
            'my company'
        )

    def test_with_common_parts_and_extra_spaces(self):
        self.assertEqual(
            clean_name('   The CompaNy.    lTd   '),
            'company'
        )


class SimilarityCalculatorTestCase(TestCase):
    def setUp(self):
        self.calc = SimilarityCalculator()

    def test_exact_names(self):
        """
            1. exact names
            2. no postcode
            =>  proximity == 0.5
        """
        self.calc.analyse_names('test', 'test')
        self.assertEqual(
            self.calc.get_proximity(),
            0.5
        )

    def test_similar_names(self):
        """
            1. similar names (not exact)
            2. no postcode
            =>  proximity == 0.25
        """
        self.calc.analyse_names('another test', 'some test something')
        self.assertEqual(
            self.calc.get_proximity(),
            0.25
        )

    def test_different_names(self):
        """
            1. different names
            2. no postcode
            =>  proximity == 0
        """
        self.calc.analyse_names('name1 part1', 'part2 name2')
        self.assertEqual(
            self.calc.get_proximity(),
            0
        )

    def test_raises_exception_if_not_bound(self):
        """
            You have to specify at least one proximity step (name and/or postcode) otherwise you
            won't be able to use get any proximity value back
        """
        self.assertRaises(
            AssertionError, self.calc.get_proximity
        )

    def test_exact_postcodes(self):
        """
            1. no names
            2. exact postcodes
            =>  proximity == 0.5
        """
        self.calc.analyse_postcodes('SW1A 1AA', 'sw1a1aa')
        self.assertEqual(
            self.calc.get_proximity(),
            0.5
        )

    def test_similar_postcodes(self):
        """
            1. no names
            2. similar postcodes
            =>  proximity == 0.25
        """
        self.calc.analyse_postcodes('SW1A 1AA', 'sw1a5ab')
        self.assertEqual(
            self.calc.get_proximity(),
            0.25
        )

    def test_different_postcodes(self):
        """
            1. no names
            2. different postcodes
            =>  proximity == 0
        """
        self.calc.analyse_postcodes('SW1A 1AA', 'w1a5ab')
        self.assertEqual(
            self.calc.get_proximity(),
            0
        )

    def test_exact_names_and_postcodes(self):
        """
            1. exact names
            2. exact postcodes
            =>  proximity == 1
        """
        self.calc.analyse_names('test', 'test')
        self.calc.analyse_postcodes('SW1A 1AA', 'sw1a1aa')
        self.assertEqual(
            self.calc.get_proximity(),
            1
        )

    def test_similar_names_and_postcodes(self):
        """
            1. similar names
            2. similar postcodes
            =>  proximity == 0.5
        """
        self.calc.analyse_names('another test', 'some test something')
        self.calc.analyse_postcodes('SW1A 1AA', 'sw1a5ab')
        self.assertEqual(
            self.calc.get_proximity(),
            0.5
        )

    def test_different_names_and_postcodes(self):
        """
            1. different names
            2. different postcodes
            =>  proximity == 0
        """
        self.calc.analyse_names('name1 part1', 'part2 name2')
        self.calc.analyse_postcodes('SW1A 1AA', 'w1a5ab')
        self.assertEqual(
            self.calc.get_proximity(),
            0
        )
