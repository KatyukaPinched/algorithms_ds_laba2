from time import *
import numpy as np
import matplotlib.pyplot as plt
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height
    def get_balance(self, key):
        if not key:
            return 0
        return self.get_height(key.left) - self.get_height(key.right)

    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        node.left = node.left

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        left_child.height = 1 + max(self.get_height(left_child.left), self.get_height(left_child.right))

        return left_child
    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        node.right = node.right

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        right_child.height = 1 + max(self.get_height(right_child.left), self.get_height(right_child.right))

        return right_child

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)
    def _insert_recursive(self, node, key):
        if not node:
            return Node(key)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)
    def _delete_recursive(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self._find_min(node.right)
            node.key = temp.key
            node.right = self._delete_recursive(node.right, temp.key)

        if node is None:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0:
            return self._rotate_right(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self._rotate_left(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def search(self, key):
        return self._search_recursive(self.root, key)
    def _search_recursive(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    def print_search(self, search_result, n):
        if search_result is not None:
            print("\nКлюч", n, "найден!")
        else:
            print("\nКлюч", n, "отсутствует!")

    def return_height(self): return self.get_height(self.root)

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
        print("Обход в глубину:")
        print("Pre-order — прямой обход: ")
        self._pre_order(self.root)
        print("\nIn-order — симметричный обход: ")
        self._in_order(self.root)
        print("\nPost-order — обратный обход: ")
        self._post_order(self.root)
        print()
    def print_width(self):
        print("\nОбход в ширину:")
        if self.root is None:
            print("Дерево пустое")
            return

        queue = [self.root]
        while queue:
            node = queue.pop(0)
            print(node.key, end=" ")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        print()

# основная программа — вставка/поиск/удаление + проходы в ширину и глубину
N = 100
avl = AVLTree()

#arr = [random.randint(0, 20000) for _ in range(N)]
arr = [42, 7, 19, 86, 33, 58, 14, 91, 27, 65, 3, 74, 12, 50, 88, 88, 88]
for i in arr:
    avl.insert(i)

avl.print_depth()
avl.print_width()

search_data = 7
search_result = avl.search(search_data)
avl.print_search(search_result, search_data)

delete_data = 7
avl.delete(delete_data)
print(f"\nЭлемент {delete_data} удален из дерева.")

search_result = avl.search(search_data)
avl.print_search(search_result, search_data)

print("\nВысота дерева —", avl.return_height())
avl.print_depth()
avl.print_width()

#вывод графиков — регрессионная кривая
y_height = []
x_col_vo = []

for i in range(1, 50001, 500):
    avl = AVLTree()
    arr = list(range(1, i + 1))
    save_arr = arr

    for j in arr:
      avl.insert(j)

    y_height.append(avl.return_height())
    x_col_vo.append(i)

coeffs = np.polyfit(np.log(x_col_vo), y_height, 1)
a, b = coeffs
log_func = lambda x: a * np.log(x) + b

print("Уравнение регрессионной кривой (логарифмическая) для AVL — ", f"y = {a:.2f} * log(x) + {b:.2f}")


plt.scatter(x_col_vo, y_height)

plt.xlabel('n — количество элементов в дереве')
plt.ylabel('h — высота дерева')
plt.legend()
plt.grid()

x_fit = np.linspace(min(x_col_vo), max(x_col_vo), 100)
y_fit = log_func(x_fit)
plt.plot(x_fit, y_fit, label='Регрессионная кривая', color='red')
plt.tight_layout()
plt.legend()
plt.show()

#вывод графиков — асимптотика
x = np.linspace(1, 100, 100)

y1 = 1.45 * np.log(x) + 0.41
y2 = np.log(x)
y3 = 1.44 * np.log2(x + 2) - 0.32

plt.plot(x, y1, label='y = 1.45 * log(x) + 0.41 — \nрегрессионная кривая, полученная практически')
plt.plot(x, y2, label='y = log(x) — \nассимптотическая оценка для лучшего случая')
plt.plot(x, y3, label='y = 1,44 * lg⁡(x+2) - 0,32 — \nассимптотическая оценка для худшего случая')

plt.xlabel('n — количество элементов в дереве')
plt.ylabel('h — высота дерева')
plt.legend()
plt.grid(True)
plt.show()