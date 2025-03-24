from django.contrib import admin
from .models import (
    Forms, Choice, RadioButton, CheckBox, DropDown, ShortChoice, LongChoice,
    RangeField, FileUpload, SpecialField, FormSubmission, RadioButtonResponse,
    CheckBoxResponse, DropDownResponse, ShortChoiceResponse, LongChoiceResponse,
    RangeFieldResponse, FileUploadResponse, SpecialFieldResponse
)

# Inline options for Questions
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class BaseQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "form", "required", "order")
    list_filter = ("form", "required")
    search_fields = ("question_text",)

class RadioButtonAdmin(BaseQuestionAdmin):
    filter_horizontal = ("options",)

class CheckBoxAdmin(BaseQuestionAdmin):
    filter_horizontal = ("options",)

class DropDownAdmin(BaseQuestionAdmin):
    filter_horizontal = ("options",)

# Registering models
admin.site.register(Forms)
admin.site.register(Choice)
admin.site.register(RadioButton, RadioButtonAdmin)
admin.site.register(CheckBox, CheckBoxAdmin)
admin.site.register(DropDown, DropDownAdmin)
admin.site.register(ShortChoice, BaseQuestionAdmin)
admin.site.register(LongChoice, BaseQuestionAdmin)
admin.site.register(RangeField, BaseQuestionAdmin)
admin.site.register(FileUpload, BaseQuestionAdmin)
admin.site.register(SpecialField, BaseQuestionAdmin)

# Form Submissions
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "form", "submitted_at")
    list_filter = ("submitted_at", "form")
    search_fields = ("user__username", "form__title")

admin.site.register(FormSubmission, FormSubmissionAdmin)

# Response Admins
admin.site.register(RadioButtonResponse)
admin.site.register(CheckBoxResponse)
admin.site.register(DropDownResponse)
admin.site.register(ShortChoiceResponse)
admin.site.register(LongChoiceResponse)
admin.site.register(RangeFieldResponse)
admin.site.register(FileUploadResponse)
admin.site.register(SpecialFieldResponse)
