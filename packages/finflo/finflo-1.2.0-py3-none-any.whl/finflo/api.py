from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .transition import FinFlotransition

class TransitionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        qs = FinFlotransition()
        type = request.GET.get("type","")
        action = request.GET.get("action","")
        stage = request.GET.get("stage","")
        t_id = request.GET.get("t_id","")
        if (type , action , stage ) is not None:
            qs.transition(type = type , action = action , stage = stage , id = t_id)
            return Response({"status" : "Transition success"},status = status.HTTP_200_OK)
        return Response({"status" : "Transition failure"},status = status.HTTP_204_NO_CONTENT)

