import graphene
import graphene_django_optimizer as gql_optimizer
from graphene_django import DjangoObjectType
from temporal import models
import uuid


class Foo(DjangoObjectType):
    class Meta:
        model = models.Foo


class FooVersion(DjangoObjectType):
    class Meta:
        model = models.FooVersion


class Bar(DjangoObjectType):
    class Meta:
        model = models.Bar


class Baz(DjangoObjectType):
    class Meta:
        model = models.Baz


class BazVersion(DjangoObjectType):
    class Meta:
        model = models.BazVersion


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    # foos = graphene.List(Foo)
    foos = graphene.List(Foo)

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
        return list(models.Foo.optimized.current())




    # old
    # def resolve_foos(root, info):
    #     return gql_optimizer.query(FooModel.objects.all(), info)

schema = graphene.Schema(query=Query)