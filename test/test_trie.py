import pytest

from src.trie import Trie


@pytest.fixture
def trie():
    """Sets up a prefix tree with words 'test' and 'words'"""
    trie = Trie()
    trie.insert("test")
    trie.insert("words")
    return trie


def test_size(trie):
    """Test for checking size of trie after insert"""
    assert trie.size() == 10

    new_trie = Trie()
    # all tries have a root element so their size is always greater than 1
    assert new_trie.size() == 1


def test_count(trie):
    """Test for checking word count after insert"""
    assert trie.count() == 2

    new_trie = Trie()
    assert new_trie.count() == 0


def test_find(trie):
    """Test for checking whether or not word is found in the Trie"""
    assert trie.find("test") is not None
    assert trie.find("test") == "test"
    assert trie.find("notintrie") is None


def test_insert(trie):
    """Tests that inserting a word into trie does not change above tests"""
    trie.insert("word_new")
    # this should not have no effect on the trie
    trie.insert("word_new")
    assert trie.size() == 14  # only adds 4 new suffixes
    assert trie.count() == 3
    assert trie.find("word_new") == "word_new"


def test_insert_all(trie):
    """Tests that inserting all words in a list works"""
    trie.insert_all(["wordz", "test2", "trie"])
    assert trie.size() == 15
    assert trie.count() == 5


def test_starts_with(trie):
    """Tests that starts_with function gives correct suffixes"""
    trie.insert("wordz")
    assert trie.starts_with("te") == ["test"]
    assert trie.starts_with("word") == ["wordz", "words"]


def test_fuzzy_match(trie):
    """Test that fuzzy matching gives correct possible words"""
    trie.insert_all(["this_is_a_test_sentence"])
    assert trie.fuzzy_match("dis_is_a_test_sentence")[1] == "this_is_a_test_sentence"
    assert trie.fuzzy_match("low_ratio") is None
