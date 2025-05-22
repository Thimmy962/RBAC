import graphene, graphql
from graphene_django import DjangoObjectType
from api import models
from api.permissions import permissions_decorator


class StaffType(DjangoObjectType):
    class Meta:
        model = models.Staff


class GroupType(DjangoObjectType):
    class Meta:
        model = models.Group

    # get the members in this group
    members = graphene.List(lambda: StaffType)
    
    # members are gotten through reverse query of the group
    def resolve_members(self, info):
        return self.user_groups.all()


class PermissionType(DjangoObjectType):
    class Meta:
        model = models.Permission


class GenreType(DjangoObjectType):
    class Meta:
        model = models.Genre


class AuthorType(DjangoObjectType):
    class Meta:
        model = models.Author


class BookType(DjangoObjectType):
    class Meta:
        model = models.Book

class PermissionType(DjangoObjectType):
    class Meta:
        model = models.Permission


class Query(graphene.ObjectType):
    # Staff resolvers
    staffs = graphene.List(StaffType)
    staff = graphene.Field(StaffType, id = graphene.Int(required = True))

    @permissions_decorator(models.Staff)
    def resolve_staffs(self, info):
        res = models.Staff.objects.all()
    

    @permissions_decorator(models.Staff)
    def resolve_staff(self, info, id):
        return models.Staff.objects.get(id = id)
    

    # Group resolvers
    groups = graphene.List(GroupType)
    group = graphene.Field(GroupType, id = graphene.Int(required = True))

    @permissions_decorator(models.Group)
    def resolve_groups(self, info, **kwargs):
        return models.Group.objects.all()

    @permissions_decorator(models.Group)
    def resolve_group(self, info, id):
        return models.Group.objects.get(id = id)


    # Genre resolvers
    genres = graphene.List(GenreType)
    genre = graphene.Field(GenreType, id = graphene.Int(required = True))

    @permissions_decorator(models.Genre)
    def resolve_genres(self, info, **kwargs):
        return models.Genre.objects.all()

    @permissions_decorator(models.Genre)
    def resolve_genre(self, info, id):
        return models.Genre.objects.get(id = id)


    # Author resolvers
    authors = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, id = graphene.Int(required = True))
    
    @permissions_decorator(models.Author)
    def resolve_authors(self, info, **kwargs):
        return models.Staff.objects.all()

    @permissions_decorator(models.Author)
    def resolve_author(self, info, id):
        return models.Staff.objects.get(id = id)

    
    # Permission resolvers
    permissions = graphene.List(PermissionType)
    permission = graphene.Field(PermissionType, id = graphene.Int(required = True))

    @permissions_decorator(models.Permission)
    def resolve_permissions(self, info):
        return models.Permission.objects.all()


    @permissions_decorator(models.Permission)
    def resolve_permission(self, info, id):
        return models.Permission.objects.get(id = id)

    

    # Book resolvers
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id = graphene.String(required = True))

    @permissions_decorator(models.Book)
    def resolve_books(self, info):
        return models.Book.objects.all()


    @permissions_decorator(models.Book)
    def resolve_book(self, info, id):
        return models.Book.objects.get(id = id)

    
schema = graphene.Schema(query = Query)