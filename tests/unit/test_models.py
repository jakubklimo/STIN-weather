from datetime import datetime, timedelta

def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.name == 'testUser'
    assert new_user.password != 'Password'

def test_set_password(new_user):
    new_user.set_password('Heslo')
    assert new_user.password != 'Heslo'
    assert new_user.check_password('Heslo')
    assert not new_user.check_password('Heslo1')

def test_chech_password(new_user):
    assert new_user.check_password('Heslo')

def test_set_premium(new_user):
    new_user.set_premium(1)
    assert new_user.premium_ex == datetime.today() + timedelta(days=30)

def test_is_subscriber(new_user):
    assert new_user.is_subscriber() == True

def test_new_location(new_location):
    assert new_location.location == 'Praha'

