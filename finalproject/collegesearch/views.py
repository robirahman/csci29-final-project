from django.shortcuts import render

from django.http import HttpResponse

from .utils import top_matches, embed_description


def index(request):
    return render(request, "collegesearch/index.html")

def results(request):
    if request.method == "POST":
        description = request.POST["description"]
        vector = embed_description(description)
        size = int(request.POST["size"])
        sat_verbal = int(request.POST["sat_verbal"])
        sat_math = int(request.POST["sat_math"])
        public = int(request.POST["public"])
        preferences = {
            "description": description,
            "vector": vector,
            "size": size,
            "sat_verbal": sat_verbal,
            "sat_math": sat_math,
            "public": public
        }
    return render(request, "collegesearch/results.html", {
        "preferences": preferences,
        "colleges": top_matches(preferences)
    })
