#Making Rango Tango Exercises {#chapter-ex}
So far, we have added in several key pieces of functionality to Rango. We've been building the app up in a manner that hopefully gets you familiar with using the Django framework, and to learn how to contstruct the various parts of a web application.

However, Rango at the moment is not very cohesive or interactive. In this chapter, we challenge you to improve the app and its user experience further by bringing together some of the functionality we have implemented along with some new features. To make Rango more coherent, integrated and interactive, let's look at implementing the following functionality.

In Rango's `Category` and `Page` models, we've included a `views` field. However, we haven't actually used them yet, so why not implement the functionality to track views to both types of content? Specifically, we'll be looking at:

- counting the number of times that a category is viewed; and
- counting the number of times a page is clicked from a Rango category view.

We'll also be wanting to collect likes for different categories, as this is also something that we have not yet implemented. We'll be looking at implementing this with AJAX (see [AJAX in Django](#chapter-ajax)). We'll also make use of AJAX to allow users to filter the categories that they see on the left-hand categories bar.

In addition to these new features, we'll be working to provide further services to registered users of Rango. Specifically, we'll be working to:

- allow users registering to the site to again specify a profile image and website (if you worked through the chapter on `django-registration-redux`, this functionality will have been lost);
- let users view and edit their profile; and
- let users who are logged in view a list of other users and their profiles.

I> ### Note
I> As we have alluded to above, we won't be working through all of these tasks in this chapter. The AJAX-related tasks (as well as definition of what AJAX actually is!) will be left to the [AJAX in Django]({#chapter-ajax}) later on, while others will be left to you to complete as additional exercises.

Before we start to add this additional functionality, we will make a *todo* list to plan our workflow for each task. Breaking tasks down into smaller sub-tasks will greatly simplify the implementation process. We'll then be attacking each main activity with a clear plan. In this chapter, we'll be providing you with the workflow for a number of the above tasks. From what you have learnt so far, you should now be able to fill in the gaps and implement most of it on your own (except for those requiring AJAX).

We've included hints, tips and code snippets to help you along. Of course, if you get really stuck, you can always check out [our implementation for the exercises on GitHub](https://github.com/maxwelld90/tango_with_django_2_code). Let's get started with tracking page clicks!

## Tracking Page Clickthroughs {#chapter-ex-clickthroughs}
Currently, Rango provides direct links to external pages. While simple, this approach does not allow us to record how many clicks each page receives -- a click takes you away from Rango without any ability to record information on what has just happened. In order to address this, we can implement a simple view to record a click -- and *then* redirect the user to the request page.

This is what happens in many contemporary social media platforms, as an example -- if someone sends you a link in Facebook Messenger, for instance, Facebook inserts a simple redirect device in order to be able to track that you clicked the link.

In order to implement functionality to track page links, have a go at the following steps.

1. First, create a new view called `goto_url()`. This should be mapped to the URL `/rango/goto/`, with a URL mapping name of `goto`.
    - The `goto_url()` view will examine the HTTP `GET` request parameters, and pull out the `page_id` that is passed along with the request. The HTTP `GET` request will take the form of something along the lines of `/rango/goto/?page_id=1`. This means that we want to redirect the user to a `Page` model instance with an `id` of `1`.
    - In the view, `get()` the `Page` with an `id` of `page_id` (from the `GET` request).
    - For that particular `Page` instance, increment the `views` field count by one, and then `save()` the changes you have made.
    - After incrementing the `views` field, redirect the user to the page instance's `url` value using the handy `redirect()` function, available at `django.shortcuts`.
    - If the `page_id` parameter is not supplied in the `GET` request, or an unknown `page_id` is supplied, then you should simply redirect the user to Rango's homepage. Again, you'll need to make use of the `redirect()` helper function, and the `reverse()` function to lookup the URL for the Rango homepage. Error handling should mean that you structure your code with `try`/`except` blocks.
    - See [Django shortcut functions](https://docs.djangoproject.com/en/2.1/topics/http/shortcuts/) for more on `redirect` and    
    [Django reverse function](ttps://docs.djangoproject.com/en/2.1/ref/urlresolvers/#django.urls.reverse) for more on `reverse`.
2. Update Rango's `urls.py` URL mappings to incorporate the new view to use the URL `/rango/goto/`. The mapping should also be given the name `goto`.
3. Then you can update Rango's `category.html` template so that instead of providing a direct link to each page, you link to the new `goto_url()` view.
    - Remember to use the `url` template tag instead of hard-coding the URL `/rango/goto/?page_id=x`, as shown in the example below.
    
    {lang="python",linenos=off}
    	<a href="{% url 'rango:goto' %}?page_id={{page.id}}">
    
    - Update the `category.html` template to also report the number of views that individual pages receive. Remember, watch out for grammar -- use the singular for one view, and plural for more than one!
4. Our final step involves updating the `show_category()` view. As we are now incrementing the `views` counter for each page when the corresponding link is clicked, how can you update the ORM query to return a list of pages, ordered by the number of clicks they have received? This should be in *descending* order, with the page boasting the largest number of clicks being ranked first.

I> ### `GET` Parameters Hint
I>
I> If you're unsure of how to retrieve the `page_id` *querystring* from the HTTP `GET` request, the following code sample should help you.
I>
I> {lang="python",linenos=off}
I> 	page_id = None
I> 	if request.method == 'GET':
I> 	    page_id = request.GET.get('page_id')
I> 	    ...
I>
I> Always check the request method is of type `GET` first. Once you have done that, you can then access the dictionary `request.GET` which contains values passed as part of the request. If `page_id` exists within the dictionary, you can pull the required value out with `request.GET.get('page_id')`.
I>
I> You could also do this without using a *querystring*, but through the URL instead. This would mean that instead of having a URL that looks like `/rango/goto/?page_id=x`, you could create a URL pattern that matches to `/rango/goto/<int:page_id>/`. Either solution would work, but if you do this, you would obtain `page_id` in `goto_url()` from a parameter to the function call, rather than from the `request.GET` dictionary.

## Searching Within a Category Page  {#chapter-ex-searching}
Rango aims to provide users with a helpful dictionary of useful web pages. At the moment, the search page functionality is essentially independent of the categories. It would be nicer to have search integrated within the categories.

In order to implement this functionality, we will assume that a user will first browse through the category of interest. If they can't find a relevant page, they can then search. If they find a page that is relevant, then they can add it to the category.

For this section, let us focus on the first problem that entails putting search on the category page. To do this, perform the following steps.

1. Remove the generic *Search* link from the navigation bar. This implies that we are decommissioning the global search functionality that we implemented earlier. You can also comment out the URL mapping and view for search if you like, too. **Comment out, don't delete** -- you'll be using the code to form the basis of your updated search functionality in subsequent steps!
2. Take the search form and results template markup from `search.html`, and place it into `category.html` *underneath* the list of pages. You'll only want to show the search functionality if the category exists in the database.
3. Update the search form such that the action refers back to the category URL, rather than the search URL.

{lang="html",linenos=off}
	<form class="form-inline"
	      id="user-form" 
	      method="post"
	      action="{% url 'rango:show_category' category.slug %}">

4. Update the `show_category()` view to handle a HTTP `POST` request. The view must then include any search results in the context dictionary for the template to render. Remember that the search query will be provided as part of the `POST` request in field `query`.
5. Finally, update Rango so that only users who are logged in can view and use the updated search functionality. To restrict access within the `category.html` template, we can use something along the lines of the following code snippet.

{lang="html",linenos=off}
	{% if user.is_authenticated %} 
	    <!-- Your search code goes here -->
	{% endif %}

T> ### Commenting out Code
T> Commenting out code stops the interpreter or compiler from using the selected code. Although it cannot see it and execute it, you can still read it and use it. In Python, the simplest way to comment out a line of code is to prepend a `#` to the line -- put it before any text.
T>
T> Other languages will have different commenting syntax. HTML for example uses `<!--` to denote the start of a commented-out block of markup, and `-->` to denote the end.

## Create and View User Profiles
If you have swapped over to the `django-registration-redux` package [as we worked on in an earlier chapter](#chapter-redux), then users who are registering won't be asked for a website or profile image. Essentially, the `UserProfile` information is not being collected. In order to fix this issue, we'll need to change the steps that users go through when registering. Instead of simply redirecting users to the index page once they have successfully filled out the initial registration form, we'll redirect them to a new form to collect the additional `UserProfile` information.

To add the UserProfile registration functionality, you need to undertake the following steps.

1. First, create a `profile_registration.html` template, which will display the `UserProfileForm`. This will need to be placed within the `rango` templates directory. Although it makes sense to place it in the `registration` directory, it is Rango specific; as such, it should live in the `rango` directory.
2. After this, you need to create a new `UserProfileForm` `ModelForm` class to handle the new form.
3. Create a new `register_profile()` view in Rango's `views.py` to capture the `UserProfile` details.
4. Finally, change where you redirect newly-registered users. We'll have to provide you with some code to show you how to do this. You can find that in the [next chapter](#section-hints-profiles).

It would also be useful to let users inspect and edit their own profiles once they have been created. To do this, undertake the following steps.

1. Create a new template called `profile.html`. This should live in the `rango` templates directory. Within this template, add in the fields associated with the `UserProfile` and the `User` instances, such as the username, website and user profile image.
2. Create a view called `profile()` in Rango's `views.py`. This view will obtain the necessary information required in order to render the `profile.html` template.
3. Map the URL `/rango/profile/` to your new `profile()` view. The mapping should have name of `profile`.
4. Finally, you should add a link in the `base.html` navigation bar called *Profile*. This link should only be available to users who are logged in (those that pass the check `{% if user.is_authenticated %}`).

To allow users to browse through other user profiles, you can also create a *users page* that lists all users registered on Rango. If you click on a username, you will then be redirected to their *profile page.* However, **you must ensure that a user is only able to edit their own profile**, and that logged in users can see the users page! 

T> ### Referencing Uploaded Content in Templates
T> If you have successfully completed all of the [Templates and Media Files chapter](#section-templates-upload), your Django setup should be ready to deal with the uploading and serving of user-defined media files (in this case, profile images). You should be able to reference the `MEDIA_URL` URL (defined in `settings.py`) in your templates through use of the `{{ MEDIA_URL }}` tag, provided by the [media template context processor](https://docs.djangoproject.com/en/2.1/howto/static-files/). We asked you to try this out as an exercises much earlier in the book. Displaying an image `cat.jpg`, the associated HTML markup would be `<img src="{{ MEDIA_URL}}cat.jpg">`.

The next chapter provides you with complete solutions to each of the exercises we outlined here. Try and do as much of them as you can by yourself without turning over to the next chapter!