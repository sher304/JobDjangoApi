from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from main.models import Ads, Reply, Rating, Likes, RealVacation
from main.permissions import IsAuthorPermission
from main.serializers import ReplySerializer, AdsSerializer, CreateRatingSerializer, LikeSerializer, \
    RealVacationSerializer

from parser import main

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class AdsViewSet(PermissionMixin, ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def my(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = AdsSerializer(queryset, many=True,
                                    context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(author__icontains=q))
        serializers = AdsSerializer(queryset, many=True,
                                    context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class AddStarRatingView(PermissionMixin, ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)


class LikesView(PermissionMixin, ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikeSerializer

    @action(detail=False, methods=['get'])
    def favorite(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = LikeSerializer(queryset, many=True,
                                    context={'request': request})
        return Response(serializer.data, status=200)


class ParserModelView(ModelViewSet):
    queryset = RealVacation.objects.all()
    serializer_class = RealVacationSerializer

    def create_vacation_view(self, request):
        vacations = main()
        company = vacations.get('company')
        position = vacations.get('position')
        price = vacations.get('price')
        image = vacations.get('image')
        work_type = vacations.get('work_type')
        RealVacation.objects.create(company=company, position=position,
                                price=price, image=image, work_type=work_type)
