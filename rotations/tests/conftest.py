from pytest_factoryboy import register

from rotations.tests.factories import MemberFactory, RotationFactory


register(MemberFactory)
register(RotationFactory)
