import unittest
from leaf import Leaf


class TestTreeAVL(unittest.TestCase):
    def test_creation(self):
        tree = Leaf(1)
        self.assertEqual('1', str(tree), 'Creation of Leaf, string cast and describe in pre order')

    def test_simple_insert(self):
        tree = Leaf(1)
        tree.insert(2)
        self.assertEqual('1|2', str(tree), 'Insertion of second leaf in right')

        tree.insert(0)
        self.assertEqual('1|0|2', str(tree), 'Insertion of third leaf in left of root')

        tree.insert(1)
        self.assertEqual('1|0|2', str(tree), 'Insertion of element that already exist in tree (root)')

        tree.insert(2)
        self.assertEqual('1|0|2', str(tree), 'Insertion of element that already exist in tree (right leaf)')

        tree.insert(0)
        self.assertEqual('1|0|2', str(tree), 'Insertion of element that already exist in tree (left leaf)')

        tree.insert(3)
        self.assertEqual('1|0|2|3', str(tree), 'Insertion of leaf in left of left leaf of root')

        tree.insert(4)
        self.assertEqual('1|0|3|2|4', str(tree), 'Insertion of element that will execute normalization in tree')

    def test_mass_insertion(self) -> None:
        expected, tree = TestTreeAVL.create_mass_scenario()

        self.assertEqual(
            expected,
            str(tree),
            'Mass insertion in order from 0-99'
        )

        expected, _ = TestTreeAVL.create_mass_scenario()

        for i in range(99, 0, -1):
            tree.insert(i)

        self.assertEqual(
            expected,
            str(tree),
            'Mass insertion in order from 99-0'
        )

    def test_simple_remove(self) -> None:
        _, tree = TestTreeAVL.create_mass_scenario(n_results=5)
        expected = '2|0|3|4'
        tree.remove(1)
        self.assertEqual(expected, str(tree), TestTreeAVL.create_error_message('Removing root'))

        _, tree = TestTreeAVL.create_mass_scenario(n_results=5)
        expected = '1|0|3|2'
        tree.remove(4)
        self.assertEqual(expected, str(tree), 'Removing Leaf')

        _, tree = TestTreeAVL.create_mass_scenario(n_results=5)
        expected = '1|0|4|2'
        tree.remove(3)
        self.assertEqual(expected, str(tree), 'Removing middle root with heir on left')

        expected = '1|0|2'
        tree.remove(4)
        self.assertEqual(expected, str(tree), 'Removing middle root with heir on right')

    def test_remove_in_mass_scenario(self) -> None:
        expected, tree = TestTreeAVL.create_mass_scenario()

        expected = expected.replace('44|', '').replace('43', '44')
        tree.remove(43)
        self.assertEqual(expected, str(tree), 'Remove a root with root as children')

        expected, tree = TestTreeAVL.create_mass_scenario()

        expected = expected.replace('64|', '').replace('63', '64')
        tree.remove(63)
        self.assertEqual(expected, str(tree), 'Remove a root with root as children')

    @staticmethod
    def create_mass_scenario(n_results: int = 100, root_starter: int = 1) -> [str, Leaf]:
        tree = Leaf(root_starter)

        for i in range(n_results):
            tree.insert(i)

        expected = '63|31|15|7|3|1|0|2|5|4|6|11|9|8|10|13|12|14|23|19|17|16|18|21|20|22|27|25|24|26|29|28|30|47|39|35|'
        expected += '33|32|34|37|36|38|43|41|40|42|45|44|46|55|51|49|48|50|53|52|54|59|57|56|58|61|60|62|79|71|67|65|'
        expected += '64|66|69|68|70|75|73|72|74|77|76|78|87|83|81|80|82|85|84|86|95|91|89|88|90|93|92|94|97|96|98|99'

        return [expected, tree]

    @staticmethod
    def create_error_message(msg: str = '', leaf_before: Leaf = None, leaf_after: Leaf = None):
        message = ''

        if msg:
            message += msg

        if leaf_before and leaf_after:
            if message != '':
                message += '\n\n'
            message += 'Before:\n'

            tree_before = leaf_before.get_displayed_tree()
            for line in tree_before:
                message += line + '\n'

            message += '\n\nAfter:\n'

            tree_after = leaf_after.get_displayed_tree()
            for line in tree_after:
                message += line + '\n'

        return message


if __name__ == '__main__':
    unittest.main()
