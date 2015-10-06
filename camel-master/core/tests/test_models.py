from model_mommy import mommy
import pytest
import string
import random

from core.models import Book, BookNode, Module


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_node(parent=None, **kwargs):
    random_params = {
        "node_class": id_generator(10),
        "node_type": id_generator(10),
        "number": random.randint(1, 100),
        "title": id_generator(20),
        "is_readonly": False,
        "node_id": random.randint(1, 100),
        "mpath": id_generator(20),
        "label": id_generator(20)
    }
    for kwarg in kwargs:
        random_params[kwarg] = kwargs[kwarg]
    node = BookNode(parent=parent, **random_params)
    node.save()
    return node

@pytest.mark.django_db
def test_node_get_book_from_leaf():
    root = get_node()
    leaf = get_node(parent=root)
    book = mommy.make(Book, tree=root)
    assert leaf.get_book() == book

@pytest.mark.django_db
def test_node_get_book_from_root():
    root = get_node()
    book = mommy.make(Book, tree=root)
    assert root.get_book() == book


@pytest.mark.django_db
def test_get_parent_by_type_on_self():
    """
    Calling get_parent_by_type on a root node should return None
    as root has no parent
    """
    book = get_node(node_type="book")
    assert book.get_parent_by_type("book") is None


@pytest.mark.django_db
def test_get_parent_by_type_direct_parent():
    """
    Calling get_parent_by_type on a node with a direct
    parent of this type should return that object
    """
    book = get_node(node_type="book")
    leaf = get_node(parent=book)
    assert leaf.get_parent_by_type("book") == book

@pytest.mark.django_db
def test_get_parent_by_type_multiple_steps():
    """
    Calling get_parent_by_type on a node with a parent of
    this type several steps up the tree should return that object
    """
    book = get_node(node_type="book")
    mid = get_node(parent=book)
    leaf = get_node(parent=mid)
    assert leaf.get_parent_by_type("book") == book

@pytest.mark.django_db
def test_get_parent_by_type_multiple_parents():
    """
    Calling get_parent_by_type on a node with multiple parents of
    this type should return the closest on the tree
    """
    book = get_node(node_type="book")
    inner_book = get_node(node_type="book", parent=book)
    leaf = get_node(parent=inner_book)
    assert leaf.get_parent_by_type("book") == inner_book

@pytest.mark.django_db
def test_get_parent_by_type_no_parents():
    """
    Calling get parent by type on a node with no parents
    of the specified type should return the root of the tree
    """
    book = get_node(node_type="book")
    mid = get_node(parent=book)
    leaf = get_node(parent=mid)
    assert leaf.get_parent_by_type("chapter") == book

@pytest.mark.django_db
def test_book_get_next_none():
    module = mommy.make(Module)
    first = mommy.make(Book, number=0, module=module)
    assert first.get_next() is None

@pytest.mark.django_db
def test_book_get_next():
    module = mommy.make(Module)
    first = mommy.make(Book, number=0, module=module)
    last = mommy.make(Book, number=1, module=module)
    assert first.get_next() == last

@pytest.mark.django_db
def test_book_get_prev_none():
    module = mommy.make(Module)
    first = mommy.make(Book, number=0, module=module)
    assert first.get_prev() is None

@pytest.mark.django_db
def test_book_get_prev():
    module = mommy.make(Module)
    first = mommy.make(Book, number=0, module=module)
    last = mommy.make(Book, number=1, module=module)
    assert last.get_prev() == first
