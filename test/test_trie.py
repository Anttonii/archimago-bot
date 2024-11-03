import unittest

from src.trie import Trie


class TrieTests(unittest.TestCase):
    def setUp(self):
        """Sets up a prefix tree with words 'test' and 'words'"""
        self.trie = Trie()
        self.trie.insert("test")
        self.trie.insert("words")

    def test_size(self):
        """Test for checking size of trie after insert"""
        self.assertEqual(self.trie.size(), 10)

        new_trie = Trie()
        # all tries have a root element so their size is always greater than 1
        self.assertEqual(new_trie.size(), 1)

    def test_count(self):
        """Test for checking word count after insert"""
        self.assertEqual(self.trie.count(), 2)

        new_trie = Trie()
        self.assertEqual(new_trie.count(), 0)

    def test_find(self):
        """Test for checking whether or not word is found in the Trie"""
        self.assertIsNotNone(self.trie.find("test"))
        self.assertEqual(self.trie.find("test"), "test")
        self.assertIsNone(self.trie.find("notintrie"))

    def test_insert(self):
        """Tests that inserting a word into trie does not change above tests"""
        self.trie.insert("word_new")
        # this should not have no effect on the trie
        self.trie.insert("word_new")
        self.assertEqual(self.trie.size(), 14)  # only adds 4 new suffixes
        self.assertEqual(self.trie.count(), 3)
        self.assertEqual(self.trie.find("word_new"), "word_new")

    def test_insert_all(self):
        """Tests that inserting all words in a list works"""
        self.trie.insert_all(["wordz", "test2", "trie"])
        self.assertEqual(self.trie.size(), 15)
        self.assertEqual(self.trie.count(), 5)

    def test_starts_with(self):
        """Tests that starts_with function gives correct suffixes"""
        self.trie.insert("wordz")
        self.assertEqual(self.trie.starts_with("te"), ["test"])
        self.assertEqual(self.trie.starts_with(
            "word"), ["wordz", "words"])

    def test_fuzzy_match(self):
        """Test that fuzzy matching gives correct possible words"""
        self.trie.insert_all(["this_is_a_test_sentence"])
        self.assertEqual(self.trie.fuzzy_match(
            "dis_is_a_test_sentence")[1], "this_is_a_test_sentence")
        self.assertIsNone(self.trie.fuzzy_match("low_ratio"))


if __name__ == "__main__":
    unittest.main()
