

class Leaf:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def set_children(self, left=None, right=None):
        self.left = left
        self.right = right

    def equalize_number(self):
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
        self.set_children(self.right, self.right.right)
        self.left.set_children(old_left, self.left.left)

    def rotate_to_right(self):
        self.data, self.left.data = self.left.data, self.data
        old_right = self.right
        self.set_children(self.left.left, self.left)
        self.right.set_children(self.right.right, old_right)

    def rotate_to_left_right(self):
        self.left.rotate_to_left()
        self.rotate_to_right()

    def rotate_to_right_left(self):
        self.right.rotate_to_right()
        self.rotate_to_left()

    def equalize(self):
        equalizer_number = self.equalize_number()
        if equalizer_number > 1:
            if self.left.equalize_number() > 0:
                self.rotate_to_right()
                return True

            self.rotate_to_left_right()
        elif equalizer_number < -1:
            if self.right.equalize_number() < 0:
                self.rotate_to_left()
                return True

            self.rotate_to_right_left()

        return False

    def insert(self, data):
        if data == self.data:
            return

        if data <= self.data:
            if not self.left:
                self.left = Leaf(data)
                self.equalize()
                return

            self.left.insert(data)
            self.equalize()
            return

        if not self.right:
            self.right = Leaf(data)
            self.equalize()
            return

        self.right.insert(data)
        self.equalize()

    def get_displayed_three(self):
        lines, *_ = self.display_aux()
        return lines
    
    def display_three(self):
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
