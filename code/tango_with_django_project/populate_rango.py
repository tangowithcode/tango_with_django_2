import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django

django.setup()
from rango.models import Category, Page


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/"
         ,"views": 20},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/"
         ,"views": 25},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/"
         ,"views": 35}]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"
         ,"views": 36},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/"
         ,"views": 23},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/"
         ,"views": 45}]

    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/"
         ,"views": 3},
        {"title": "Flask",
         "url": "http://flask.pocoo.org"
         ,"views": 34}]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes":64 },
            "Django": {"pages": django_pages, "views": 64, "likes":32 },
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes":16 }}

    # If you want to add more catergories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.

    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data)
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"],p["views"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, cat_data):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = cat_data["views"]
    c.likes= cat_data["likes"]
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
