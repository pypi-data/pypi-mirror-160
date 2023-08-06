import unittest
import numpy as np

from stse import Binarizer


class TestBinarize(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_values = [
            55,
            4,
            7,
            100,
            2000
        ]
        cls.qualifiers = [
            '<',
            '>',
            '<',
            '=',
            '='
        ]
        
        cls.boundary = 10
        return super().setUpClass()
    
    def test_bin_no_qualifiers(self):
        out = []
        for op in zip(Binarizer.active_operators):
            out.append(Binarizer.bin_no_qualifiers(self.test_values, self.boundary, op).tolist())
            
        self.assertEqual(
            out,
            [
                [tv > self.boundary for tv in self.test_values],
                [tv < self.boundary for tv in self.test_values],
                [tv >= self.boundary for tv in self.test_values],
                [tv <= self.boundary for tv in self.test_values]
            ]
        )
        
    def test_bin_qualifiers(self):
        out = []
        for op in Binarizer.active_operators:
            out.append(Binarizer.bin_qualifiers(self.test_values, self.boundary, self.qualifiers, op)
                       .tolist())
        
        expected = [
                [tv > self.boundary for tv in self.test_values],
                [tv < self.boundary for tv in self.test_values],
                [tv >= self.boundary for tv in self.test_values],
                [tv <= self.boundary for tv in self.test_values]
            ]
        
        expected = [2*[np.nan] + ex[2:] for ex in expected]
        
        self.assertTrue(
            np.allclose(
                out,
                expected,
                equal_nan=True
            )
        )
        
    def test_binarize(self):
        out = []
        for op in Binarizer.active_operators:
            binarizer = Binarizer(values=self.test_values, qualifiers=self.qualifiers, boundary=self.boundary,
                                  active_operator=op)
            out.append(binarizer.binarize().tolist())
            
        expected = [
                [tv > self.boundary for tv in self.test_values],
                [tv < self.boundary for tv in self.test_values],
                [tv >= self.boundary for tv in self.test_values],
                [tv <= self.boundary for tv in self.test_values]
            ]
        
        expected = [2*[np.nan] + ex[2:] for ex in expected]
        
        self.assertTrue(
            np.allclose(
                out,
                expected,
                equal_nan=True
            )
        )
        
    def test_vectorize_float(self):
        values = [5, 10, 15, 20, 25]
        qualifiers = ['=', '<', '<', '<', '<']
        binarizer = Binarizer(values=values, qualifiers=qualifiers, boundary=2, active_operator='>')
        
        self.assertTrue(
            np.allclose(
                binarizer.binarize(),
                [1] + 4*[np.nan],
                equal_nan=True
            )
        )
            

if __name__ == '__main__':
    unittest.main()
