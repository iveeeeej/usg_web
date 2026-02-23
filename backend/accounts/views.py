from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsOfficer


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsOfficer]

    def get(self, request):
        return Response({"message": "Welcome Officer"})