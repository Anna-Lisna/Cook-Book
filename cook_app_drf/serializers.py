from rest_framework import serializers
from users.models import CustomUser
from recipes.models import Recipes, Images
from comment.models import Comment
from .models import EmailForLetters


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'city', 'short_description']


class UserSerializer(serializers.ModelSerializer):
    creator_recipe = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'description', 'city', 'creator_recipe']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'description', 'city']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.description = validated_data.get('description', instance.description)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance


class UserRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ['title', 'short_description', 'image_url']


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ['title', 'short_description', 'image_url', 'total_likes', 'total_comments']
        read_only_fields = [
            'creator',
            'total_likes',
            'total_comments',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']

    def create(self, validated_data):
        creator = self.context['request'].user
        recipe_id = self.context['pk'].pk
        body = validated_data['body']
        comment = Comment(creator=creator, recipe_id=recipe_id, body=body)
        comment.save()
        return validated_data


class CreateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ['title', 'description', 'image']


class UpdateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        exclude = ['creator', 'likes']


class LoadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['images']


class ReceiveLettersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailForLetters
        fields = '__all__'


