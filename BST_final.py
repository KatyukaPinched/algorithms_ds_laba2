from random import randint

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)
    def _insert_recursive(self, node, key):
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)

        self._update_height(node)
        return node

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)
        print(f"\nЭлемент {key} удален из дерева.")
    def _delete_recursive(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            successor = self._min_value_node(node.right)

            node.key = successor.key

            node.right = self._delete_recursive(node.right, successor.key)

        self._update_height(node)
        return node

    def search(self, key):
        return self._search_recursive(self.root, key)
    def _search_recursive(self, node, key):
        if node is None or key == node.key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    def print_search(self, search_result, n):
        if search_result is not None:
            print("\nКлюч", n, "найден!")
        else:
            print("\nКлюч", n, "отсутствует!")

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _get_height(self, node):
        if node:
            return node.height
        return -1

    def return_height(self):
        return self._get_height(self.root)

    def _pre_order(self, node): # корень-левое-правое — прямой обход
        if node:
            print(node.key, end=" ")
            self._pre_order(node.left)
            self._pre_order(node.right)
    def _in_order(self, node): # левое-корень-правое — симметричный обход
        if node:
            self._in_order(node.left)
            print(node.key, end=" ")
            self._in_order(node.right)
    def _post_order(self, node): # левое-правое-корень — обратный обход
        if node:
            self._post_order(node.left)
            self._post_order(node.right)
            print(node.key, end=" ")

    def print_depth(self):
        if self.root is None:
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
        if self.root is None:
            return
        print("\nОбход в ширину:")
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            print(node.key, end=" ")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        print()

N = 100
bst = BST()

#arr = [randint(1, 20000) for i in range(N)]
arr = [42, 7, 19, 86, 33, 58, 14, 91, 27, 65, 3, 74, 12, 50, 88]
for i in arr:
    bst.insert(i)

bst.print_depth()
bst.print_width()

search_data = 42
search_result = bst.search(search_data)
bst.print_search(search_result, search_data)

delete_data = 42
bst.delete(delete_data)

search_result = bst.search(search_data)
bst.print_search(search_result, search_data)

bst.print_depth()
bst.print_width()