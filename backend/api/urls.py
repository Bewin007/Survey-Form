from django.urls import path
from .views import (
    FormListView, FormRetrieveUpdateDeleteView,
    RadioButtonListCreateView, CheckBoxListCreateView, DropDownListCreateView,
    ShortChoiceListCreateView, LongChoiceListCreateView, RangeFieldListCreateView,
    FileUploadListCreateView, SpecialFieldListCreateView,
    ResponseListCreateView, ResponseRetrieveView,FormCreateView,
    TextAnswerListCreateView, ChoiceAnswerListCreateView, RangeAnswerListCreateView, FileAnswerListCreateView
)

urlpatterns = [
    # ---- FORM ENDPOINTS ----
    path('forms/create/', FormCreateView.as_view(), name='form-create'),
    path('forms/', FormListView.as_view(), name='form-list'),
    path('forms/<int:pk>/', FormRetrieveUpdateDeleteView.as_view(), name='form-detail'),

    # ---- QUESTION ENDPOINTS ----
    path('questions/radio/', RadioButtonListCreateView.as_view(), name='radio-question'),
    path('questions/checkbox/', CheckBoxListCreateView.as_view(), name='checkbox-question'),
    path('questions/dropdown/', DropDownListCreateView.as_view(), name='dropdown-question'),
    path('questions/shortchoice/', ShortChoiceListCreateView.as_view(), name='shortchoice-question'),
    path('questions/longchoice/', LongChoiceListCreateView.as_view(), name='longchoice-question'),
    path('questions/range/', RangeFieldListCreateView.as_view(), name='range-question'),
    path('questions/fileupload/', FileUploadListCreateView.as_view(), name='fileupload-question'),
    path('questions/special/', SpecialFieldListCreateView.as_view(), name='special-question'),

    # ---- RESPONSE ENDPOINTS ----
    path('responses/', ResponseListCreateView.as_view(), name='response-list-create'),
    path('responses/<int:pk>/', ResponseRetrieveView.as_view(), name='response-detail'),

    # ---- ANSWER ENDPOINTS ----
    path('answers/text/', TextAnswerListCreateView.as_view(), name='text-answer'),
    path('answers/choice/', ChoiceAnswerListCreateView.as_view(), name='choice-answer'),
    path('answers/range/', RangeAnswerListCreateView.as_view(), name='range-answer'),
    path('answers/file/', FileAnswerListCreateView.as_view(), name='file-answer'),
]
