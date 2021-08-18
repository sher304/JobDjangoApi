from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from account.models import CustomUser


class Ads(models.Model):
    title = models.CharField(max_length=270)
    description = models.TextField()
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='problems')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()


class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    problem = models.ForeignKey(Ads, on_delete=models.CASCADE,
                                related_name='images')


class Reply(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE,
                            related_name='replies')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='replies')
    body = models.TextField()
    image = models.ImageField(upload_to='reply_images', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:15] + '...'

    class Meta:
        ordering = ('-created',)


class RatingStar(models.Model):
    value = models.SmallIntegerField('value', default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Rating Star'
        verbose_name_plural = 'Rating Stars'
        ordering = ['-value']


class Rating(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE,
                            related_name='rating')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='rating')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE,
                             related_name='rating')

    def __str__(self):
        return f'{self.star} - {self.ads}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Likes(models.Model):
    liked_ads = models.ForeignKey(Ads, on_delete=models.CASCADE,
                                  related_name='ads_likes')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='author_likes')
