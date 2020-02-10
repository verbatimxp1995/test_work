from datetime import datetime

from rest_framework import viewsets, generics, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CommentSerializer, AuthorSerializer, MarkBaseSerializer, MarkSerializer, \
    MaterialBaseSerializer, MaterialSerializer

from .models import User, Mark, Comment, Material


class AuthorViewSet(generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    serializer_class = AuthorSerializer
    queryset = User.objects.all()
    
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        return queryset.filter(id=user.id)


class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MaterialBaseSerializer
        return self.serializer_class

    @action(methods=['GET', 'POST'], detail=True)
    def comments(self, request, *args, **kwargs):
        user = request.user
        material = self.get_object()  
        if request.method == 'GET':
            comments = Comment.objects.filter(material=material)
            serializer = CommentSerializer(comments, many=True)
            response_status=status.HTTP_200_OK
        else:
            comment = Comment.objects.create(material=material, author=user, **request.data)
            serializer = CommentSerializer(comment)
            response_status=status.HTTP_201_CREATED
            
        return Response(data=serializer.data, status=response_status)

    @action(methods=['POST'], detail=True)
    def mark(self, request, *args, **kwargs):
        material = self.get_object()
        user = request.user

        mark_data = request.data
        mark_data['material'] = material
        mark_data['author'] = user
        if not mark_data.get('mark'):
            raise exceptions.ValidationError('Mark is not emty')
        try:
            mark = Mark.objects.get(author=user, material=material)
            mark.mark = mark_data.get('mark')
            mark.save()
        except Mark.DoesNotExist:
            mark = Mark.objects.create(**mark_data)

        serializer = MarkSerializer(mark)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['PATCH'], detail=True)
    def publish(self, request, *args, **kwargs):
        material = self.get_object()
        material.published = datetime.now()
        material.save()

        serializer = MaterialSerializer(material)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
