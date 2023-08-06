from isHex import isHex

def test_isHex_valid_lowercase_chars():
    assert isHex("abcdef") == True

def test_isHex_valid_uppercase_chars():
    assert isHex("ABCDEF") == True

def test_isHex_valid_mixed_chars():
    assert isHex("aBcDeF") == True

def test_isHex_valid_numbers():
    assert isHex("1234567890") == True

def test_isHex_mixed_numbers_and_chars():
    assert isHex("1234567890aBcDeF") == True

def test_isHex_invalid_chars():
    assert isHex("abcdefg") == False

def test_isHex_invalid_mixed_numbers_and_chars():
    assert isHex("97863hgfe347") == False