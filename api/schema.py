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
    staffs = graphene.List(StaffType, offset=graphene.Int(), limit=graphene.Int())
    staff = graphene.Field(StaffType, id = graphene.Int(required = True))

    @permissions_decorator(models.Staff)
    def resolve_staffs(self, info, offset=0, limit=10):
        return models.Staff.objects.all()[offset : offset + limit]

    @permissions_decorator(models.Staff)
    def resolve_staff(self, info, id):
        return models.Staff.objects.get(id = id)
    

    # Group resolvers
    groups = graphene.List(GroupType, offset=graphene.Int(), limit=graphene.Int())
    group = graphene.Field(GroupType, id = graphene.Int(required = True))

    @permissions_decorator(models.Group)
    def resolve_groups(self, info, offset=0, limit=5):
        return models.Group.objects.prefetch_related('members', 'permissions').all()[offset : offset + limit]

    @permissions_decorator(models.Group)
    def resolve_group(self, info, id):
        return models.Group.objects.prefetch_related('members', 'permissions').get(id=id)



    # Genre resolvers
    genres = graphene.List(GenreType, offset=graphene.Int(), limit=graphene.Int())
    genre = graphene.Field(GenreType, id = graphene.Int(required = True))

    @permissions_decorator(models.Genre)
    def resolve_genres(self, info, offset = 0, limit = 10):
        return models.Genre.objects.prefetch_related('genre_books').all()[offset: offset + limit]

    @permissions_decorator(models.Genre)
    def resolve_genre(self, info, id):
        return models.Genre.objects.prefetch_related('genre_books').get(id = id)


    # Author resolvers
    authors = graphene.List(AuthorType, offset = graphene.Int(), limit = graphene.Int())
    author = graphene.Field(AuthorType, id = graphene.Int(required = True))
    
    @permissions_decorator(models.Author)
    def resolve_authors(self, info, offset = 0, limit = 40):
        return models.Author.objects.prefetch_related('author_books').all()[offset:offset+limit]

    @permissions_decorator(models.Author)
    def resolve_author(self, info, id):
        return models.Author.objects.prefetch_related('author_books').get(id = id)

    
    # Permission resolvers
    permissions = graphene.List(PermissionType, offset = graphene.Int(), limit = graphene.Int())
    permission = graphene.Field(PermissionType, id = graphene.Int(required = True))

    @permissions_decorator(models.Permission)
    def resolve_permissions(self, info, offset = 0, limit = 10):
        return models.Permission.objects.all()[offset:offset+limit]


    @permissions_decorator(models.Permission)
    def resolve_permission(self, info, id):
        return models.Permission.objects.get(id = id)

    

    # Book resolvers
    books = graphene.List(BookType, offset= graphene.Int(), limit = graphene.Int())
    book = graphene.Field(BookType, id = graphene.String(required = True))

    @permissions_decorator(models.Book)
    def resolve_books(self, info, offset = 0, limit = 50):
        return models.Book.objects.prefetch_related('author', 'genre').all()[offset : limit + offset]


    @permissions_decorator(models.Book)
    def resolve_book(self, info, id):
        return models.Book.objects.prefetch_related('author', 'genre').get(id = id)

    
schema = graphene.Schema(query = Query)