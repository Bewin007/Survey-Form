from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import generics, status

import base64
from django.core.files.base import ContentFile



class FormView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datas = Forms.objects.all()
        serializer = FormListSerializer(datas, many=True)  # Add many=True
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = FormCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign user here
            return Response(serializer.data)
        return Response(serializer.errors)
    







# class QuestionCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         data = request.data

#         # Extract form ID
#         form_id = data.get("form_id")
#         form = Forms.objects.filter(id=form_id, user=user).first()
#         if not form:
#             return Response({"error": "Form not found or unauthorized"}, status=403)

#         # Extract question type
#         question_type = data.get("question_type")
#         valid_types = {
#             "radio": RadioButton,
#             "checkbox": CheckBox,
#             "dropdown": DropDown,
#             "short_text": ShortChoice,
#             "long_text": LongChoice,
#             "range": RangeField,
#             "file": FileUpload,
#             "special": SpecialField,
#         }

#         if question_type not in valid_types:
#             return Response({"error": "Invalid question type"}, status=400)

#         # Serialize and create question
#         serializer = QuestionCreateSerializer(data=data)
#         if serializer.is_valid():
#             question_model = valid_types[question_type]
#             question = question_model.objects.create(
#                 form=form,
#                 question_text=serializer.validated_data["question_text"],
#                 required=serializer.validated_data["required"],
#                 order=serializer.validated_data["order"],
#             )

#             if question_type in ["radio", "checkbox", "dropdown"]:
#                 choices = data.get("choices", [])
#                 for choice_text in choices:
#                     choice, _ = Choice.objects.get_or_create(choice_text=choice_text)
#                     question.options.add(choice)

#             if question_type == "range":
#                 question.start = serializer.validated_data["start"]
#                 question.end = serializer.validated_data["end"]
#                 question.save()

#             return Response({"message": "Question created successfully", "question_id": question.id}, status=201)
        
#         return Response(serializer.errors, status=400)
class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Extract form ID
        form_id = data.get("form_id")
        form = Forms.objects.filter(id=form_id, user=user).first()
        if not form:
            return Response({"error": "Form not found or unauthorized"}, status=403)

        # Extract question type
        question_type = data.get("question_type")
        valid_types = {
            "radio": RadioButton,
            "checkbox": CheckBox,
            "dropdown": DropDown,
            "short_text": ShortChoice,
            "long_text": LongChoice,
            "range": RangeField,
            "file": FileUpload,
            "special": SpecialField,
        }

        if question_type not in valid_types:
            return Response({"error": "Invalid question type"}, status=400)

        # Serialize and create question
        serializer = QuestionCreateSerializer(data=data)
        if serializer.is_valid():
            question_model = valid_types[question_type]
            question = question_model.objects.create(
                form=form,
                question_text=serializer.validated_data["question_text"],
                required=serializer.validated_data["required"],
                order=serializer.validated_data["order"],
            )

            # Handle multiple choice questions
            if question_type in ["radio", "checkbox", "dropdown"]:
                choices = data.get("choices", [])
                for choice_text in choices:
                    choice, _ = Choice.objects.get_or_create(choice_text=choice_text)
                    question.options.add(choice)

            # Handle range field
            if question_type == "range":
                question.start = serializer.validated_data.get("start", 1)
                question.end = serializer.validated_data.get("end", 10)
                question.save()

            # Handle file upload
            if question_type == "file":
                uploaded_file = request.FILES.get("file_upload")
                if not uploaded_file:
                    return Response({"error": "File is required for file upload question"}, status=400)
                question.file_upload = uploaded_file
                question.save()

            # Handle special field
            if question_type == "special":
                question.special_field = serializer.validated_data.get("special_field", "")
                question.save()

            return Response({"message": "Question created successfully", "question_id": question.id}, status=201)

        return Response(serializer.errors, status=400)





class FormQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        form = get_object_or_404(Forms, id=pk, user=request.user)

        question_models = [RadioButton, CheckBox, DropDown, ShortChoice, LongChoice, RangeField, FileUpload, SpecialField]
        all_questions = []

        for model in question_models:
            questions = model.objects.filter(form=form)
            serialized_questions = QuestionRetrieveSerializer(questions, many=True).data
            all_questions.extend(serialized_questions)

        return Response({"questions": all_questions})



class SubmitFormView(generics.CreateAPIView):
    serializer_class = FormSubmissionSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request, *args, **kwargs):
        user = request.user  # Get authenticated user
        form_id = kwargs.get('pk')  # Extract form ID from URL
        form = get_object_or_404(Forms, id=form_id)  # Ensure form exists

        # Merge user & form into request data
        data = request.data.copy()
        data['user'] = user.id  # Add user ID
        data['form'] = form.id  # Add form ID

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            submission = serializer.save()
            return Response(
                {"message": "Form submitted successfully", "submission_id": submission.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
