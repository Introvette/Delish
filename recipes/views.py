from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from recipes.forms import RatingForm

try:
    from recipes.forms import RecipeForm
    from recipes.models import Recipe
except Exception:
    RecipeForm = None
    Recipe = None


def create_recipe(request):
    if request.method == "POST" and RecipeForm:
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect("recipe_detail", pk=recipe.pk)
    elif RecipeForm:
        form = RecipeForm()
    else:
        form = None
    context = {
        "form": form,
    }
    return render(request, "recipes/new.html", context)


def change_recipe(request, pk):
    if Recipe and RecipeForm:
        instance = Recipe.objects.get(pk=pk)
        if request.method == "POST":
            form = RecipeForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect("recipe_detail", pk=pk)
        else:
            form = RecipeForm(instance=instance)
    else:
        form = None
    context = {
        "form": form,
    }
    return render(request, "recipes/edit.html", context)


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/list.html"


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm()
        return context


def log_rating(request, recipe_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.recipe = Recipe.objects.get(pk=recipe_id)
            rating.save()
    return redirect("recipe_detail", pk=recipe_id)
