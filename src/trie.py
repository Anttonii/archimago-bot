from difflib import SequenceMatcher as SM
from typing import List


class Node():
    """
    A prefix tree node.
    """

    def __init__(self, word=""):
        self.word = word
        self.children = dict()
        self.word_node = False


class Trie():
    """
    A prefix tree.
    """

    def __init__(self):
        self.root = Node()
        self.word_list = []

    def insert_all(self, words):
        """
        Shorthand for inserting all words of a list into the Trie
        """
        for word in words:
            self.insert(word)

    def insert(self, word):
        """
        Inserts a new word into the prefix tree.
        """
        current = self.root
        for (i, ch) in enumerate(word):
            if ch not in current.children:
                prefix = word[0:i + 1]
                current.children[ch] = Node(prefix)
            current = current.children[ch]
        current.word_node = True
        self.word_list.append(word)

    def find(self, word):
        """
        Checks if a given word is in the prefix tree.
        """
        current = self.root
        for ch in word:
            if ch not in current.children:
                return None
            current = current.children[ch]

        return current.word if current.word_node else None

    def size(self):
        """
        Returns the size of the trie.
        """
        stack = [self.root]
        count = 0

        while stack:
            curr = stack.pop()
            count += 1

            for ch in curr.children:
                stack.append(curr.children[ch])

        return count

    def count(self):
        """
        Returns the count of whole words in trie
        """
        stack = [self.root]
        count = 0

        while stack:
            curr = stack.pop()
            if curr.word_node:
                count += 1

            for ch in curr.children:
                stack.append(curr.children[ch])

        return count

    def starts_with(self, prefix: str) -> List[str]:
        """
        Checks the prefix tree for words starting with given prefix.
        """
        current = self.root
        for ch in prefix:
            if ch not in current.children:
                return None
            current = current.children[ch]

        # Iteratively check all children to find all complete words in the tree.
        stack = [current]
        words = list()
        while stack:
            curr = stack.pop()

            if curr.word_node:
                words.append(curr.word)

            for ch in curr.children:
                stack.append(curr.children[ch])

        return words

    def fuzzy_match(self, card_name: str) -> tuple[float, str]:
        """
        Returns the best rating fuzzy word match from trie.
        """
        def filter_func(s1, s2):
            """
            Filter based on first four characters when possible
            """
            s1_len = min(4, len(s1))
            s2_len = min(s1_len, len(s2))

            for i in range(s1_len):
                if s1[i] in s2[:s2_len]:
                    return True

            return False

        # Simple pruning where we only evalute the words with the same starting letter.
        pruned_list = list(
            filter(lambda x: filter_func(card_name, x), self.word_list)
        )

        matched_words = [
            (SM(None, card_name, word).ratio(), word)
            for word in pruned_list
        ]

        if len(matched_words) == 0:
            return None

        best_match = max(matched_words)

        # Return best match if ratio is higher than 0.5
        return best_match if best_match[0] > 0.5 else None
