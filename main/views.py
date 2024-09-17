from django.shortcuts import render, redirect
from main.forms import MoodEntryForm
from main.models import MoodEntry

# Create your views here.
def show_main(request):
    mood_entries = MoodEntry.objects.all()

    context = {
        'name': 'Pak Bepe',
        'class': 'PBP D',
        'npm': '2306123456',
        'mood_entries': mood_entries
    }

    return render(request, "main.html", context)

def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_mood_entry.html", context)