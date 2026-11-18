from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from TripMaster.serializers import UserSerializers, TripSerializers,TripMemberSerializers
from TripMaster.models import TripDb,TripMemberDb
from rest_framework import authentication, permissions,serializers
from TripMaster.permissions import OwnerOnly

from rest_framework.exceptions import PermissionDenied

# Create your views here.
class SignUpView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializers(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message":"User Created Successfully"},status=201)
        else:
            return Response({"message":"Invalid data provided"},status=400)

class userlistview(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer_instance = UserSerializers(users,many=True)
        return Response(serializer_instance.data,status=200)

class TripListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        qs = TripDb.objects.filter(created_by=request.user)
        serializer_instance = TripSerializers(qs,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data =request.data
        serializer_instance = TripSerializers(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={
                "message" : "Trips created successfully",
                "Trip_Details" : serializer_instance.data
                           })           
        else:
            return Response(data=serializer_instance.errors)


class TripRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [OwnerOnly]

    def get(self,request,pk):
        trip_object = get_object_or_404(TripDb,id=pk)
        if trip_object.created_by == request.user:
            serializer_instance = TripSerializers(trip_object)
            return Response(data=serializer_instance.data,status=200)
        else:
            return Response(data={
                "Message" : "access denied"
            })


    def put(self,request,pk):
        trip_object = get_object_or_404(TripDb,id=pk)

        if trip_object.created_by != request.user:
            raise serializers.ValidationError("Access Denied")
        
        form_data = request.data
        # if trip_object.created_by == request.user:
        serializer_instance = TripSerializers(data=form_data, instance=trip_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                    "message" :"trip details updated successfully",
                    "trip_details" : serializer_instance.data
                })
        else:
            return Response(data=serializer_instance.errors)
        # else:
        #     return Response(data={
        #         "Message" : "access denied"
        #     })


    def delete(self,request,pk):
        trip_object =get_object_or_404(TripDb,id=pk)
        if trip_object.created_by == request.user:
            trip_object.delete()
            return Response(data = {
                "message" :"trip deleted succesfully"
            })
        else:
            return Response(data={
                "Message" : "access denied"
            })

#TRIP MEMBER FUNCTIONALITIES
class TripMemberListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [OwnerOnly]


    def get(self,request,trip_id):

        #Get the trip
        trip_object = get_object_or_404(TripDb,id=trip_id)

        is_owner = trip_object.created_by == request.user
        is_member = TripMemberDb.objects.filter(trip = trip_object ,user = request.user).exists()

        if not(is_owner or is_member):
            raise PermissionDenied("you are not alloweed to access this trip..!")

        # GET ALL THE TRIP MEMBERS
        members = TripMemberDb.objects.filter(trip=trip_object)

        serializer_instance = TripMemberSerializers(members ,many=True)

        return Response(data=serializer_instance.data ,status=200)

    def post(self,request,trip_id):

        trip_object = get_object_or_404(TripDb, id=trip_id)

        if trip_object.created_by != request.user:
            raise PermissionDenied("only trip owner can add members..!")

        form_data = request.data

        serializer_instance = TripMemberSerializers(data=form_data, context ={'trip':trip_object})

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "message": "trip member added successfully..!"
            })

        else:
            return Response(data=serializer_instance.errors,status=400)


class MemberDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [OwnerOnly]

    def delete(self,request,trip_id,member_id):
        trip_object = get_object_or_404(TripDb,id=trip_id)

        #check ownership
        if trip_object.created_by != request.user:
            raise PermissionDenied("only the trip owner can remove members...!")
        member_object = get_object_or_404(TripMemberDb,id=member_id,trip=trip_object)

        member_object.delete()

        return Response(data={
            "message": "member deleted successfully..!!!"
        })

        