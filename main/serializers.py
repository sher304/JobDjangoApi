from rest_framework import serializers

from .models import Ads, CodeImage, Reply, Rating


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image',)


class AdsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Ads
        fields = ('id', 'title', 'description', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images.all(),
                                                   many=True).data
        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
        elif action == 'retrieve':
            representation['replies'] = ReplySerializer(instance.replies.all(),
                                                        many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        # print(request.user)
        images_data = request.FILES
        # print(images_data)
        problem = Ads.objects.create(
                                    author=request.user,
                                    **validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image,
                                     problem=problem)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value, in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            CodeImage.objects.create(
                image=image,
                problem=instance
            )
        return instance


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Reply
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
        )
        return reply


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'ads')

    def create(self, validated_data):
        request = self.context.get('request')
        rating, user = Rating.objects.update_or_create(
            ads=validated_data.get('ads', None),
            author=request.user,
            star=validated_data.get("star", None)
        )
        return rating


