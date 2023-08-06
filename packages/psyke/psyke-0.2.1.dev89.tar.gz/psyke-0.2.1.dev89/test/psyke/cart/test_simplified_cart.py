from parameterized import parameterized_class
from sklearn.model_selection import train_test_split
from psyke import Extractor
from psyke.cart import CartPredictor
from test import get_dataset, get_model
import unittest


# TODO: should be refactored using the a .csv file
@parameterized_class([{"dataset": "iris", "predictor": "DTC", "task": "classification"},
                      {"dataset": "house", "predictor": "DTR", "task": "regression"}])
class TestSimplifiedCart(unittest.TestCase):

    def test_equality(self):
        dataset = get_dataset(self.dataset)
        dataset = dataset.reindex(sorted(dataset.columns[:-1]) + [dataset.columns[-1]], axis=1)
        train, test = train_test_split(dataset, test_size=0.5)
        tree = get_model(self.predictor, {})
        tree.fit(train.iloc[:, :-1], train.iloc[:, -1])
        extractor = Extractor.cart(CartPredictor(tree), simplify=False, task=self.task)
        _ = extractor.extract(train)
        simplified_extractor = Extractor.cart(CartPredictor(tree), task=self.task)
        _ = simplified_extractor.extract(train)
        self.assertEqual(
            list(extractor.predict(test.iloc[:, :-1])),
            list(simplified_extractor.predict(test.iloc[:, :-1]))
        )


if __name__ == '__main__':
    unittest.main()
