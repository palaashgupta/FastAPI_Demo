import pytest

def test_equal_or_not_equal():
    assert 1 == 1

def test_is_instance():
    assert isinstance("1", str)

def test_boolean():
    validate = True
    assert validate is True
    assert ('hello' == 'world') is False

def test_type():
    assert type(1) is int
    assert type("1") is str
    assert type(1.0) is float
    assert type([]) is list
    assert type(()) is tuple
    assert type({}) is dict
    assert type(set()) is set

class Student:
    def __init__(self, first_name: str,last_name:str, major:str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
    
@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 3)

def test_person_initialization(default_student):
    
    assert default_student.first_name == "John", "First name should be John"
    assert default_student.last_name == "Doe", "Last name should be Doe"
    assert default_student.major == "Computer Science", "Major should be Computer Science"
    assert default_student.years == 3