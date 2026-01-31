from django.shortcuts import render,get_object_or_404
from .models import *
from .serializers import *
from rest_framework.views import APIView
from .encryption import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class CreateView(APIView):
    def post(self,request):
        context = VaultCreateSerializer(data = request.data)
        if not context.is_valid():
            return Response({"Status":401,"message":"Invalid input"})
        plain_password = context.validated_data.pop("password")
        encrypted_password = encrypt_pass(plain_password)
        entry = VaultEntry.objects.create(
            owner=request.user,
            encrypted_password=encrypted_password,
            **context.validated_data
        )
        response_serializer = VaultReadSerializer(entry)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

class ListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        entries = VaultEntry.objects.filter(owner = request.user)
        serializer=VaultReadSerializer(entries,many=True)
        return Response(serializer.data)

class UpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        entry = get_object_or_404(
            VaultEntry,
            id=id,
            owner=request.user
        )
        serializer = VaultCreateSerializer(
            entry,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if "password" in serializer.validated_data:
            plain_password = serializer.validated_data.pop("password")
            entry.encrypted_password = encrypt_pass(plain_password)
        for attr, value in serializer.validated_data.items():
            setattr(entry, attr, value)

        entry.save()
        return Response(
            VaultReadSerializer(entry).data,
            status=status.HTTP_200_OK
        )


class DeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        entry = get_object_or_404(
            VaultEntry,
            id=id,
            owner=request.user
        )
        entry.delete()
        return Response(
            {"message": "Vault entry deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

class DetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        entry = get_object_or_404(VaultEntry, id=id ,owner=request.user)
        decrypted_password = decrypt_pass(entry.encrypted_password)
        return Response({"status":200,
            "id": entry.id,
            "service_name": entry.service_name,
            "login_identifier": entry.login_identifier,
            "password": decrypted_password,
            "notes":entry.notes})