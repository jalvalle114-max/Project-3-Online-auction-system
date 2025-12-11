from modules.user import User

def test_user_init():
    u = User("Bob", 150)
    assert u.balance == 150
    assert u.name == "Bob"
