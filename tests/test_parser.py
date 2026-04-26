import sys
import os
import unittest


sys.path.append(
 os.path.abspath(
   os.path.join(
      os.path.dirname(__file__),
      ".."
   )
 )
)

from src.crossref import normalize
from src.crossref import split_extensions
from src.parsing import group_by_extension


class TestParser(unittest.TestCase):

    def test_normalize(self):

        self.assertEqual(
           normalize("rv64_zkn"),
           "zkn"
        )


    def test_split(self):

        self.assertEqual(
          split_extensions("zabha_zacas"),
          ["zabha","zacas"]
        )


    def test_crossref_logic(self):

        A={"zba","zbb"}
        B={"zba","m"}

        self.assertEqual(
            A & B,
            {"zba"}
        )

    def test_group_by_extension(self):

        sample = {

            "add":{
                "extension":["rv_i"]
            },

            "andn":{
                "extension":["rv_zbb","rv_zkn"]
            }

        }

        grouped, multi = group_by_extension(sample)


        self.assertEqual(
            grouped["rv_i"],
            ["add"]
        )

        self.assertEqual(
            grouped["rv_zbb"],
            ["andn"]
        )

        self.assertIn(
            "andn",
            multi
        )


if __name__=="__main__":
    unittest.main()