import pytest


@pytest.mark.django_db
def test_rotation(member_factory, rotation_factory):
    members = (member_factory(), member_factory())

    rotation = rotation_factory(members=members, on_call=members[0])

    for member in members:
        assert rotation.on_call == member
        rotation.advance()

    # Verify the rotation wraps around.
    assert rotation.on_call == members[0]
