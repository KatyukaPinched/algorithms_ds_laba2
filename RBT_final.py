import random

class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = "RED" # Все новые узлы красные

class RBTree:
    def __init__(self):
        self.nil = Node(None)
        self.nil.color = "BLACK"
        self.root = self.nil

    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.nil:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent == self.nil:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child
    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.nil:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent == self.nil:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def insert(self, key):
        new_node = Node(key)
        new_node.left = self.nil
        new_node.right = self.nil
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                if x.key == key: return
                x = x.right
        new_node.parent = y
        if y == self.nil:
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node
        self._balance_insert(new_node)
    def _balance_insert(self, key):
        while key.parent.color == "RED":
            if key.parent == key.parent.parent.left:
                y = key.parent.parent.right
                if y.color == "RED":
                    key.parent.color = "BLACK"
                    y.color = "BLACK"
                    key.parent.parent.color = "RED"
                    key = key.parent.parent
                else:
                    if key == key.parent.right:
                        key = key.parent
                        self._rotate_left(key)
                    key.parent.color = "BLACK"
                    key.parent.parent.color = "RED"
                    self._rotate_right(key.parent.parent)
            else:
                y = key.parent.parent.left
                if y.color == "RED":
                    key.parent.color = "BLACK"
                    y.color = "BLACK"
                    key.parent.parent.color = "RED"
                    key = key.parent.parent
                else:
                    if key == key.parent.left:
                        key = key.parent
                        self._rotate_right(key)
                    key.parent.color = "BLACK"
                    key.parent.parent.color = "RED"
                    self._rotate_left(key.parent.parent)
        self.root.color = "BLACK"

    def _transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, key):
        node = self.search(key)
        if node == self.nil:
            return

        y = node
        y_original_color = y.color
        if node.left == self.nil:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.nil:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == "BLACK":
            self._balance_delete(x)
        print(f"\nЭлемент {key} удален из дерева.")
    def _balance_delete(self, node):
        while node != self.root and node.color == "BLACK":
            if node == node.parent.left:
                w = node.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    node.parent.color = "RED"
                    self._rotate_left(node.parent)
                    w = node.parent.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    node = node.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self._rotate_right(w)
                        w = node.parent.right
                    w.color = node.parent.color
                    node.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self._rotate_left(node.parent)
                    node = self.root
            else:
                w = node.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    node.parent.color = "RED"
                    self._rotate_right(node.parent)
                    w = node.parent.left
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    node = node.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self._rotate_left(w)
                        w = node.parent.left
                    w.color = node.parent.color
                    node.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self._rotate_right(node.parent)
                    node = self.root
        node.color = "BLACK"

    def minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    def search(self, key):
        node = self.root
        while node != self.nil:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return self.nil
    def print_search(self, result, n):
        if result is not None and result != self.nil:
            print(f"\nКлюч {n} найден в дереве.")
        else:
            print(f"\nКлюч {n} не найден в дереве.")

    def return_height(self, node=None):
        if node is None:
            node = self.root
        if node == self.nil:
            return 0
        else:
            left_height = self.return_height(node.left)
            right_height = self.return_height(node.right)
            return max(left_height, right_height) + 1

    def _pre_order(self, node): # корень-левое-правое — прямой обход
        if node:
            if node.key != None: print(node.key, end=" ")
            self._pre_order(node.left)
            self._pre_order(node.right)
    def _in_order(self, node): # левое-корень-правое — симметричный обход
        if node:
            self._in_order(node.left)
            if node.key != None: print(node.key, end=" ")
            self._in_order(node.right)
    def _post_order(self, node): # левое-правое-корень — обратный обход
        if node:
            self._post_order(node.left)
            self._post_order(node.right)
            if node.key != None: print(node.key, end=" ")

    def print_depth(self):
        if self.return_height() <= 0:
            print("Дерево пустое!")
            return
        print("Обход в глубину:")
        print("Pre-order — прямой обход: ")
        self._pre_order(self.root)
        print("\nIn-order — симметричный обход: ")
        self._in_order(self.root)
        print("\nPost-order — обратный обход: ")
        self._post_order(self.root)
        print()
    def print_width(self):
        if self.return_height() <= 0:
            return
        print("\nОбход в ширину:")
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if node.key != None: print(node.key, end=" ")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        print()


N = 100
rbt = RBTree()

#arr = [random.randint(0, 20000) for _ in range(N)]
arr = [42, 7, 19, 86, 33, 58, 14, 91, 27, 65, 3, 74, 12, 50, 88]
for i in arr:
    rbt.insert(i)

rbt.print_depth()
rbt.print_width()

search_data = 7
search_result = rbt.search(search_data)
rbt.print_search(search_result, search_data)

delete_data = 7
rbt.delete(delete_data)

search_result = rbt.search(search_data)
rbt.print_search(search_result, search_data)

rbt.print_depth()
rbt.print_width()