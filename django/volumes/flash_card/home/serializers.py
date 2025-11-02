from .models import FlashCard
from rest_framework import serializers
from khayyam import JalaliDate


class FlashCardSerializer(serializers.ModelSerializer):
    created_at_jalali = serializers.SerializerMethodField()
    next_review_date_jalali = serializers.SerializerMethodField()

    class Meta:
        model = FlashCard
        fields = [
            "id",
            "word",
            "meaning",
            "example",
            "rate",
            "last_reply",
            "created_at",
            "next_review_date",
            "created_at_jalali",
            "next_review_date_jalali",
        ]

    def get_created_at_jalali(self, obj):
        if obj.created_at:
            return JalaliDate(obj.created_at).strftime("%A, %d %B, %Y")
        return None

    def get_next_review_date_jalali(self, obj):
        if obj.next_review_date:
            return JalaliDate(obj.next_review_date).strftime("%A, %d %B, %Y")
        return None
