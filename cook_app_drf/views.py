from django.db.models import Prefetch
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GetAuthToken(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            data['response'] = 'success'
            data['email'] = user.email
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)


class AllUsers(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AllUsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name']


class UserProfile(ModelViewSet):
    queryset = CustomUser.objects.prefetch_related(Prefetch(
        'creator_recipe',
        queryset=Recipes.active.filter(access='public')))
    serializer_class = UserSerializer


class UpdateUser(RetrieveUpdateAPIView, ModelViewSet):
    serializer_class = UpdateUserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def put(self, request, id=None):
        return self.update(request, id)

    def get_queryset(self):
        return CustomUser.objects.all()


class UserRecipe(ModelViewSet):
    serializer_class = UserRecipesSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['access']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Recipes.active.filter(creator=self.request.user.id)


class RecipesPublic(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Recipes.active.filter(access='public', creator__status='a')
    serializer_class = RecipesSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['creator']
    search_fields = ['title', 'description']

    @action(methods=['post'], detail=True)
    def make_like(self, request, pk=None):
        recipe = self.get_object()
        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)
            recipe.save()
        serializer = self.get_serializer(recipe)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def make_comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data, context={'request': request, 'pk': self.get_object()})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class CreateRecipe(CreateModelMixin, GenericViewSet):
    serializer_class = CreateRecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(**{'creator': self.request.user})

    def get_queryset(self):
        return Recipes.active.filter(image_creator=self.request.user.id)


class UpdateRecipe(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UpdateRecipeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def put(self, request, id=None):
        return self.update(request, id)

    def get_queryset(self):
        return Recipes.active.filter(creator=self.request.user.id, creator__status='a')


class LoadImage(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = LoadImageSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Images.objects.filter(creator=self.request.user.id)

    # def perform_create(self, serializer):
    #     serializer.save(**{'creator': self.request.user})

    def perform_create(self, serializer):
        serializer.save(**{'creator': CustomUser.objects.get(id=43)})


class ReceiveLetters(CreateModelMixin, GenericViewSet):
    serializer_class = ReceiveLettersSerializer


