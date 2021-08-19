from rest_framework import serializers

from .models import Ads, CodeImage, Reply, Rating, Likes, RealVacation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image',)

    #
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation["reviews"] = ReviewSerializer(instance.reviews.all(), many=True).data
    #     representation["rating"] = self.get_rating(instance)
    #     representation["images"] = ImageSerializer(instance.posters.all(), many=True).data
    #     return representation


class AdsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Ads
        fields = ('id', 'title', 'description', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images.all(),
                                                   many=True).data
        representation['likes'] = Likes.objects.filter(liked_ads=instance).count()
        representation['rating'] = Rating.objects.filter(ads=instance).count()

        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
        elif action == 'retrieve':
            representation['replies'] = ReplySerializer(instance.replies.all(),
                                                        many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
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


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        ads = validated_data.get('liked_ads')

        if Likes.objects.filter(author=user, liked_ads=ads):
            return Likes.objects.get(author=user, liked_ads=ads)
        else:
            return Likes.objects.create(author=user, liked_ads=ads)


class RealVacationSerializer(serializers.ModelSerializer):

    class Meta:
        model = RealVacation
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        vacation = validated_data.get('company')
        if RealVacation.objects.filter(company=vacation):
            return RealVacation.objects.get(company=vacation)
        else:
            return RealVacation.objects.create(compnay=vacation)

