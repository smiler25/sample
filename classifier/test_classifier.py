import unittest
from classifier import Classifier


class ClassifierTest(unittest.TestCase):

    def test_all(self):
        classifier = Classifier(["рецепт борща", "рецепт супа", "рецепт салата",
                                 "рецепт ещё чего-то", "яблочный пирог",
                                 "макароны по флотски", "макароны по-флотски"])
        cases = (
            ("как приготовить яблочный пирог", True),
            ("борща любимого рецепт", True),
            ("борщика любимого рецепт", False),
            ("макароны", False),
            ("макароны по-флотски", True),
        )

        for phrase, compare in cases:
            self.assertEqual(compare, classifier(phrase))
