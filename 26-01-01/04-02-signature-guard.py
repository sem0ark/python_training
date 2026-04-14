import pytest

"""
Goal: Modify the function signature of `create_user` to strictly 
enforce how arguments are passed using Python's `/` and `*` syntax.

Requirements:
1. 'user_id': Must be POSITIONAL-ONLY.
2. 'username': Can be passed by POSITION or by KEYWORD.
3. 'email': Must be KEYWORD-ONLY.
4. 'role': Must be KEYWORD-ONLY and default to "guest".

Concepts: 
- Arguments before `/` are positional-only.
- Arguments after `*` are keyword-only.
"""


# TODO: Update the parameters of this function to match the requirements
def create_user(user_id, username, email, role="guest"):
    return {"id": user_id, "user": username, "email": email, "role": role}


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_valid_calls():
    """Tests calls that follow the signature rules."""
    # user_id as pos, username as pos, email as kw
    assert create_user(1, "alice", email="a@test.com")["id"] == 1
    # user_id as pos, username as kw, email as kw
    assert create_user(2, username="bob", email="b@test.com")["user"] == "bob"


def test_positional_only_violation():
    """Tests that passing user_id as a keyword raises TypeError."""
    with pytest.raises(TypeError):
        create_user(user_id=1, username="alice", email="a@test.com")


def test_keyword_only_violation():
    """Tests that passing email as positional raises TypeError."""
    with pytest.raises(TypeError):
        create_user(1, "alice", "a@test.com")


def test_default_role():
    """Tests that the default role is applied correctly."""
    user = create_user(1, "alice", email="a@test.com")
    assert user["role"] == "guest"


if __name__ == "__main__":
    pytest.main([__file__])
