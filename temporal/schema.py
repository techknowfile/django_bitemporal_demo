import graphene
import graphene_django_optimizer as gql_optimizer
from graphene_django import DjangoObjectType
from temporal.models import FooVersion as FooVersionModel, FooTimestamp as FooTimestampModel, \
    Foo as FooModel
import uuid


class Foo(DjangoObjectType):
    class Meta:
        model = FooModel


class FooVersion(DjangoObjectType):
    class Meta:
        model = FooVersionModel


# class FooTimestamp(DjangoObjectType):
#     class Meta:
#         model = FooTimestampModel

#
# class BitemporalFooVersion(graphene.ObjectType):
#     id = graphene.ID()
#     timestamp = graphene.Field(FooTimestamp)
#     temporals = graphene.List(FooVersion)


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    foos = graphene.List(Foo)
    # bitemporal_foos = graphene.List(BitemporalFooVersion)

    # def resolve_bitemporal_foos(root, info):
    #     foo = FooModel.objects.first()
    #     versions = []
    #     for version in foo.versions.all():
    #         versions.append({
    #             'id': version.id,
    #             'timestamp': version,
    #             'temporals': foo.temporal.as_of(version.timestamp)
    #         })
    #     return versions


    def resolve_foos(root, info):
        return gql_optimizer.query(FooModel.objects.all(), info)

schema = graphene.Schema(query=Query)