from rest_framework import serializers
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class FormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = ['user','title','sub_title','description']


# Serializer for Choice model
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text']

# Base serializer for questions
class BaseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = ['id', 'question_text', 'required', 'order']

# Specific serializers for each type of question
class RadioButtonSerializer(BaseQuestionSerializer):
    options = ChoiceSerializer(many=True)

    class Meta(BaseQuestionSerializer.Meta):
        model = RadioButton
        fields = BaseQuestionSerializer.Meta.fields + ['options']

class CheckBoxSerializer(BaseQuestionSerializer):
    options = ChoiceSerializer(many=True)

    class Meta(BaseQuestionSerializer.Meta):
        model = CheckBox
        fields = BaseQuestionSerializer.Meta.fields + ['options']

class DropDownSerializer(BaseQuestionSerializer):
    options = ChoiceSerializer(many=True)

    class Meta(BaseQuestionSerializer.Meta):
        model = DropDown
        fields = BaseQuestionSerializer.Meta.fields + ['options']

class ShortChoiceSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = ShortChoice
        fields = BaseQuestionSerializer.Meta.fields

class LongChoiceSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = LongChoice
        fields = BaseQuestionSerializer.Meta.fields

class RangeFieldSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = RangeField
        fields = BaseQuestionSerializer.Meta.fields + ['start', 'end']

class FileUploadSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = FileUpload
        fields = BaseQuestionSerializer.Meta.fields

class SpecialFieldSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        model = SpecialField
        fields = BaseQuestionSerializer.Meta.fields

class FormListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forms
        fields = '__all__'




class QuestionCreateSerializer(serializers.Serializer):
    form_id = serializers.IntegerField()
    question_text = serializers.CharField()
    required = serializers.BooleanField(default=False)
    order = serializers.IntegerField()
    question_type = serializers.ChoiceField(
        choices=[
            ("radio", "RadioButton"),
            ("checkbox", "CheckBox"),
            ("dropdown", "DropDown"),
            ("short_text", "ShortChoice"),
            ("long_text", "LongChoice"),
            ("range", "RangeField"),
            ("file", "FileUpload"),
            ("special", "SpecialField"),
        ]
    )
    choices = serializers.ListField(
        child=serializers.CharField(), required=False
    )  # Only for radio, checkbox, dropdown
    start = serializers.FloatField(required=False)  # Only for range field
    end = serializers.FloatField(required=False)  # Only for range field
    file_upload = serializers.FileField(required=False)  # Only for file upload
    special_field= serializers.CharField(required=False)  # Only for special field



from rest_framework import serializers
from .models import RadioButton, CheckBox, DropDown, ShortChoice, LongChoice, RangeField, FileUpload, SpecialField

class QuestionRetrieveSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.CharField()
    required = serializers.BooleanField()
    order = serializers.IntegerField()
    question_type = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField(), required=False)
    start = serializers.FloatField(required=False, allow_null=True)
    end = serializers.FloatField(required=False, allow_null=True)
    file_upload = serializers.FileField(required=False, allow_null=True)
    special_field = serializers.CharField(required=False, allow_null=True)

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "question_text": instance.question_text,
            "required": instance.required,
            "order": instance.order,
            "question_type": instance.__class__.__name__,
        }

        if isinstance(instance, (RadioButton, CheckBox, DropDown)):
            data["options"] = [choice.choice_text for choice in instance.options.all()]
        if isinstance(instance, RangeField):
            data["start"] = instance.start
            data["end"] = instance.end
        if isinstance(instance, FileUpload):
            data["file_upload"] = instance.file_upload.url if instance.file_upload else None
        if isinstance(instance, SpecialField):
            data["special_field"] = instance.special_field

        return data





from rest_framework import serializers
from .models import FormSubmission, Choice, RadioButtonResponse, CheckBoxResponse, DropDownResponse, ShortChoiceResponse, LongChoiceResponse, RangeFieldResponse, FileUploadResponse, SpecialFieldResponse
import base64
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

class FormSubmissionSerializer(serializers.ModelSerializer):
    responses = serializers.JSONField(write_only=True)  # Accepts responses as a JSON object

    class Meta:
        model = FormSubmission
        fields = ['user', 'form', 'responses']

    def create(self, validated_data):
        responses_data = validated_data.pop('responses')  # Extract responses
        submission = FormSubmission.objects.create(**validated_data)  # Create submission

        for response in responses_data:
            question_id = response.get('question_id')
            question_type = response.get('question_type')
            answer = response.get('answer')

            if not question_id or not question_type:
                raise serializers.ValidationError("Each response must have 'question_id' and 'question_type'.")

            # Save response based on question type
            if question_type == "RadioButton":
                selected_choice = get_object_or_404(Choice, id=answer)
                RadioButtonResponse.objects.create(submission=submission, question_id=question_id, selected_choice=selected_choice)

            elif question_type == "CheckBox":
                response_obj = CheckBoxResponse.objects.create(submission=submission, question_id=question_id)
                response_obj.selected_choices.set(Choice.objects.filter(id__in=answer))

            elif question_type == "DropDown":
                selected_choice = get_object_or_404(Choice, id=answer)
                DropDownResponse.objects.create(submission=submission, question_id=question_id, selected_choice=selected_choice)

            elif question_type == "ShortChoice":
                ShortChoiceResponse.objects.create(submission=submission, question_id=question_id, answer_text=answer)

            elif question_type == "LongChoice":
                LongChoiceResponse.objects.create(submission=submission, question_id=question_id, answer_text=answer)

            elif question_type == "RangeField":
                RangeFieldResponse.objects.create(submission=submission, question_id=question_id, value=answer)

            elif question_type == "FileUpload":
                file_data = base64.b64decode(answer)  # Assuming file is sent as base64
                FileUploadResponse.objects.create(submission=submission, question_id=question_id, file=ContentFile(file_data, name=f"upload_{question_id}.jpg"))

            elif question_type == "SpecialField":
                SpecialFieldResponse.objects.create(submission=submission, question_id=question_id, special_text=answer)

        return submission
