from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from .models import FlashCard
from .serializers import FlashCardSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from datetime import timedelta, date
from django.views import View
from django.db.models import Q
from .forms import CardCreateForm
from django.contrib import messages


class Home(APIView):
    def get(self, request):
        flash_cards = FlashCard.objects.all()
        serializer = FlashCardSerializer(flash_cards, many=True)
        return Response(serializer.data)


class Word(APIView):
    def get_object(self, pk):
        """
        متدی برای دریافت یک فلش‌کارت با بررسی وجود
        """
        try:
            return FlashCard.objects.get(pk=pk)
        except FlashCard.DoesNotExist:
            raise NotFound(detail="این فلش‌کارت یافت نشد!", code=404)

    def get(self, request, pk):
        """
        دریافت اطلاعات یک فلش‌کارت بر اساس کلید اصلی
        """
        flash_card = self.get_object(pk)
        serializer = FlashCardSerializer(flash_card)
        return Response(data=serializer.data)

    def post(self, request):
        word = request.data.get("word", "").strip()
        if not word:
            return Response(
                {"error": "فیلد 'word' الزامی است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # بررسی وجود کلمه تکراری
        if FlashCard.objects.filter(word=word).exists():
            raise ValidationError("این کلمه قبلاً ثبت شده است.")
        serializer = FlashCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        flash_card = self.get_object(pk)
        data = request.data

        # بررسی مقدار last_reply و افزایش نرخ
        last_reply = data.get("last_reply")
        rate = int(flash_card.rate)
        next_review_date = flash_card.next_review_date
        today = date.today()
        if (
            last_reply in ["True", "true", True]
            and rate < 8
            and next_review_date <= today
        ):

            data["rate"] = rate + 1
            data["next_review_date"] = date.today() + timedelta(days=1)

        # سریالایز و ذخیره داده‌ها
        serializer = FlashCardSerializer(flash_card, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # بازگرداندن خطاهای اعتبارسنجی
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        flash_card = self.get_object(pk)  # دریافت فلش‌کارت
        flash_card.delete()  # حذف فلش‌کارت
        return Response(
            {"detail": "فلش‌کارت با موفقیت حذف شد!"}, status=status.HTTP_204_NO_CONTENT
        )


class CardsView(View):
    def get(self, request):
        cards = FlashCard.objects.all()
        return render(request, "home/cards.html", {"cards": cards})


class CardDetialsView(View):
    def get(self, request, id):
        card = FlashCard.objects.get(id=id)
        return render(request, "home/card_details.html", {"card": card})

    def post(self, request, id):
        user_answer = request.POST.get("answer")
        card = FlashCard.objects.get(id=id)
        rate = card.rate

        if user_answer == "yes" and rate < 9:
            card.last_reply = True
            card.rate += 1
            card.next_review_date = date.today() + timedelta(days=1)

        if user_answer == "yes" and rate == 9:
            card.last_reply = True
            card.rate += 1
            card.next_review_date = date.today() + timedelta(weeks=1)

        if user_answer == "yes" and rate == 10:
            card.last_reply = True
            card.rate += 1
            card.next_review_date = date.today() + timedelta(days=30)

        if user_answer == "yes" and rate >= 11:
            card.last_reply = True
            card.rate += 1
            card.next_review_date = date.today() + timedelta(days=365)

        if user_answer == "no":
            card.last_reply = False
            card.next_review_date = date.today() + timedelta(days=1)
        card.save()

        return redirect("home:home")


class HomeView(View):
    def get(self, request):
        cards = FlashCard.objects.filter(next_review_date__lte=date.today()).order_by("?")
        return render(request, "home/home.html", {"cards": cards})


class CardsWrongView(View):
    def get(self, request):
        title = "wrong Cards"
        cards = FlashCard.objects.filter(last_reply=False)
        return render(
            request, "home/cards_wrong.html", {"cards": cards, "title": title}
        )


class CardCreatView(View):
    def get(self, request):
        title = "Create Card"
        form = CardCreateForm
        return render(request, "home/card_create.html", {"form": form, "title": title})

    def post(self, request):
        form = CardCreateForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.next_review_date = date.today() + timedelta(days=1)
            card.save()
            word = request.POST.get("word")
            messages.success(request, f'Word "{word}" successfully saved.', "success")
            return redirect("home:cardcreate")


class CardsSearchView(View):
    def get(self, request):
        query = request.GET.get(
            "query", ""
        )  # در صورتی که query وجود نداشته باشد، مقدار پیش‌فرض "" خواهد بود
        if query:
            cards = FlashCard.objects.filter(
                Q(word__icontains=query)
                | Q(meaning__icontains=query)
                | Q(example__icontains=query)
            )
        else:
            cards = FlashCard.objects.all()
        title = "Search Cards"

        return render(
            request, "home/cards_search.html", {"cards": cards, "title": title}
        )


class CardEditView(View):
    def get(self, request, id):
        card = get_object_or_404(FlashCard, id=id)
        form = CardCreateForm(instance=card)
        title = "Edit Card"
        return render(
            request, "home/card_edit.html", {"form": form, "card": card, "title": title}
        )

    def post(self, request, id):
        card = get_object_or_404(FlashCard, id=id)
        form = CardCreateForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
        return redirect("home:cardnewest")


class CardsNewestView(View):
    def get(self, request):
        cards = FlashCard.objects.all().order_by("-created_at")

        return render(request, "home/cards.html", {"cards": cards})
