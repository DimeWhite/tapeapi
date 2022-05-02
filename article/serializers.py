from rest_framework import serializers
from article.models import Article
from user.models import User
from user.serializers import UserSerializer
from rest_framework import permissions


class ArticleSerializers(serializers.ModelSerializer):
    author = UserSerializer(source='get_author')

    class Meta:
        model = Article
        fields = '__all__'

    def create(self, validated_data, author=None):
        if self.context['request'].user.role == 'AUTHOR':
            return Article.objects.create(author=self.context['request'].user, **validated_data)
        else:
            return Article.objects.create(**validated_data)

    def __init__(self, *args, **kwargs):
        super(ArticleSerializers, self).__init__(*args, **kwargs)
        try:
            if self.context['request'].method in ['POST']:
                if self.context['request'].user.is_authenticated:
                    if self.context['request'].user.is_superuser:
                        self.fields['author'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role="AUTHOR"))
                    elif self.context['request'].user.role == "AUTHOR":
                        self.fields.pop('author')
                    else:
                        self.fields.clear()
                else:
                    self.fields.clear()
            elif self.context['request'].method in ['PUT', 'DESTROY']:
                self.fields.pop('author')
            elif self.context['request'].method in ['GET']:
                pass
        except KeyError:
            pass