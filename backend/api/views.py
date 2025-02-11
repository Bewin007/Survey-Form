from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import (
    Forms, RadioButton, CheckBox, DropDown, ShortChoice, LongChoice, RangeField, FileUpload, SpecialField, 
    Response as ResponseModel, TextAnswer, ChoiceAnswer, RangeAnswer, FileAnswer
)
from .serializers import (
    FormsSerializer, RadioButtonSerializer, CheckBoxSerializer, DropDownSerializer, ShortChoiceSerializer, 
    LongChoiceSerializer, RangeFieldSerializer, FileUploadSerializer, SpecialFieldSerializer,
    ResponseSerializer, TextAnswerSerializer, ChoiceAnswerSerializer, RangeAnswerSerializer, FileAnswerSerializer,
    FormCreateSerializer
)

class FormCreateView(APIView):
    def post(self, request):
        serializer = FormCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign user here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        
# ---- FORM VIEWS ----
class FormListView(generics.ListCreateAPIView):
    """ View to list all forms or create a new form """
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

class FormRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """ View to retrieve, update, or delete a specific form """
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer
    permission_classes = [permissions.IsAuthenticated]

# ---- QUESTION VIEWS ----
class RadioButtonListCreateView(generics.ListCreateAPIView):
    queryset = RadioButton.objects.all()
    serializer_class = RadioButtonSerializer
    permission_classes = [permissions.IsAuthenticated]

class CheckBoxListCreateView(generics.ListCreateAPIView):
    queryset = CheckBox.objects.all()
    serializer_class = CheckBoxSerializer
    permission_classes = [permissions.IsAuthenticated]

class DropDownListCreateView(generics.ListCreateAPIView):
    queryset = DropDown.objects.all()
    serializer_class = DropDownSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShortChoiceListCreateView(generics.ListCreateAPIView):
    queryset = ShortChoice.objects.all()
    serializer_class = ShortChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class LongChoiceListCreateView(generics.ListCreateAPIView):
    queryset = LongChoice.objects.all()
    serializer_class = LongChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class RangeFieldListCreateView(generics.ListCreateAPIView):
    queryset = RangeField.objects.all()
    serializer_class = RangeFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

class FileUploadListCreateView(generics.ListCreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

class SpecialFieldListCreateView(generics.ListCreateAPIView):
    queryset = SpecialField.objects.all()
    serializer_class = SpecialFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

# ---- RESPONSE VIEWS ----
class ResponseListCreateView(generics.ListCreateAPIView):
    """ View to list or create responses to a form """
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResponseRetrieveView(generics.RetrieveAPIView):
    """ View to retrieve a specific response """
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

# ---- ANSWER VIEWS ----
class TextAnswerListCreateView(generics.ListCreateAPIView):
    queryset = TextAnswer.objects.all()
    serializer_class = TextAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChoiceAnswerListCreateView(generics.ListCreateAPIView):
    queryset = ChoiceAnswer.objects.all()
    serializer_class = ChoiceAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

class RangeAnswerListCreateView(generics.ListCreateAPIView):
    queryset = RangeAnswer.objects.all()
    serializer_class = RangeAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

class FileAnswerListCreateView(generics.ListCreateAPIView):
    queryset = FileAnswer.objects.all()
    serializer_class = FileAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
