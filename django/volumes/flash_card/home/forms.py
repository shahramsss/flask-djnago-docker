from django import forms
from .models import FlashCard


class CardCreateForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        fields = ["word", "meaning", "example"]

        widgets = {
            "word": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the word",
                }
            ),
            "meaning": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the meaning",
                }
            ),
            "example": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter an example (optional)",
                }
            ),
            "rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 5,
                    "placeholder": "Rate (0-5)",
                }
            ),
            "last_reply": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "next_review_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }
