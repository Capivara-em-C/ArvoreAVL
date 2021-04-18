

class Leaf:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.father = None

    def __str__(self):
        return self.describe_pre_order()

    def describe_pre_order(self):
        description = str(self.data)

        if self.left is not None:
            description += f"|{self.left.describe_pre_order()}"

        if self.right is not None:
            description += f"|{self.right.describe_pre_order()}"

        return description

    def find(self, data):
        if data == self.data:
            return self

        if data < self.data:
            if self.left is None:
                raise Exception("Not found")

            return self.left.find(data)

        if self.right is None:
            raise Exception("Not found")

        return self.right.find(data)

    def set_children(self, left=None, right=None):
        self.left = left
        self.right = right

    def normalize_number(self):
        left_deep = 0
        if self.left:
            left_deep = self.left.find_deep()

        right_deep = 0
        if self.right:
            right_deep = self.right.find_deep()

        return left_deep - right_deep

    def find_deep(self):
        left_deep = 0
        right_deep = 0

        if self.left:
            left_deep = self.left.find_deep()

        if self.right:
            right_deep = self.right.find_deep()

        return 1 + max(left_deep, right_deep)

    def rotate_to_left(self):
        self.data, self.right.data = self.right.data, self.data

        old_left = self.left
        if old_left is not None:
            old_left.father = self.right

        self.set_children(self.right, self.right.right)
        self.left.set_children(old_left, self.left.left)

        if self.right is not None:
            self.right.father = self

    def rotate_to_right(self):
        self.data, self.left.data = self.left.data, self.data

        old_right = self.right
        if old_right is not None:
            old_right.father = self.left

        self.set_children(self.left.left, self.left)
        self.right.set_children(self.right.right, old_right)

        if self.left is not None:
            self.left.father = self

    def rotate_to_left_right(self):
        self.left.rotate_to_left()
        self.rotate_to_right()

    def rotate_to_right_left(self):
        self.right.rotate_to_right()
        self.rotate_to_left()

    def normalize(self):
        normalize_number = self.normalize_number()
        if normalize_number > 1:
            if self.left.normalize_number() > 0:
                self.rotate_to_right()
                return True

            self.rotate_to_left_right()
            return True

        if normalize_number < -1:
            if self.right.normalize_number() < 0:
                self.rotate_to_left()
                return True

            self.rotate_to_right_left()
            return True

        return False

    def insert(self, data: int):
        try:
            self.find(data)
        except Exception:
            self.__insert(data)

    def __insert(self, data: int):
        if data == self.data:
            return

        if data < self.data:
            if not self.left:
                self.left = Leaf(data)
                self.left.father = self
                self.normalize()
                return

            self.left.insert(data)
            self.normalize()
            return

        if not self.right:
            self.right = Leaf(data)
            self.right.father = self
            self.normalize()
            return

        self.right.insert(data)
        self.normalize()

    def heir(self):
        if self.right is not None:
            heir = self.right
            while heir.left is not None:
                heir = heir.left

            return heir

        heir = self.left
        while heir.right is not None:
            heir = heir.right

        return heir

    def remove(self, data: int):
        self.removeLeaf(self.find(data))

    def removeLeaf(self, leaf_to_remove):
        has_left = leaf_to_remove.left is not None
        has_right = leaf_to_remove.right is not None

        if not has_left and not has_right:
            if leaf_to_remove.father is None:
                del leaf_to_remove
                return

            if leaf_to_remove.father.data == leaf_to_remove.data:
                if leaf_to_remove.father.tmp < leaf_to_remove.data:
                    leaf_to_remove.father.right = None
                    return

                leaf_to_remove.father.left = None
                return

            if leaf_to_remove.father.data < leaf_to_remove.data:
                leaf_to_remove.father.right = None
                return

            leaf_to_remove.father.left = None
            return

        heir = leaf_to_remove.heir()
        leaf_to_remove.tmp = leaf_to_remove.data
        leaf_to_remove.data = heir.data
        self.removeLeaf(heir)
        leaf_to_remove.tmp = None

    def get_displayed_tree(self):
        lines, *_ = self.display_aux()
        return lines
    
    def display_tree(self):
        lines, *_ = self.display_aux()
        for line in lines:
            print(line)

    def display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.data
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left.display_aux()
            s = '%s' % self.data
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right.display_aux()
            s = '%s' % self.data
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left.display_aux()
        right, m, q, y = self.right.display_aux()
        s = '%s' % self.data
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '

        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)

        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2