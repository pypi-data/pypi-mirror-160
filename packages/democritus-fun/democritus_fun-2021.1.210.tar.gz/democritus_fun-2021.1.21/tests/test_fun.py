from democritus_fun import password_create


def test_password_create_1():
    assert len(password_create()) == 15
    assert len(password_create(length=20)) == 20

    new_pwd = password_create(length=21, character_set='ab')
    assert len(new_pwd) == 21
    new_pwd_has_only_a_b = new_pwd.count('a') + new_pwd.count('b') == 21
    assert new_pwd_has_only_a_b
