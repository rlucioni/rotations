import factory
from faker import Faker

from rotations.models import Member, Rotation


faker = Faker()


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    name = factory.LazyAttribute(lambda x: faker.name())
    email = factory.LazyAttribute(lambda x: faker.email())


class RotationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rotation

    name = factory.LazyAttribute(lambda x: faker.name())
    description = factory.LazyAttribute(lambda x: faker.sentence())
    message = factory.LazyAttribute(lambda x: faker.paragraph())

    on_call = factory.SubFactory(MemberFactory)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)

    @factory.post_generation
    def watchers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for watcher in extracted:
                self.watchers.add(watcher)
