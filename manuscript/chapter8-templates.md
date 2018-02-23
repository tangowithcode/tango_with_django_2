#Working with Templates {#chapter-templates-extra}
So far, we've created several HTML templates for different pages within our Rango application. As you've created more and more templates, you may have noticed that a lot of the HTML code is actually repeated. We are violating the [DRY Principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself). Furthermore, you might have noticed that the way we have been referring to different pages using *hard coded* URL paths. Taken together, maintaining the site will be nightmare, because if we want to make a change to the general site structure or change a URL path, we will have to modify every template.

In this chapter, we will use *template inheritance* to overcome the first problem, and the *URL template tag* to solve the second problem. We will start with addressing the latter problem first.

## Using Relative URLs in Templates
So far, we have been directly coding the URL of the page or view we want to
show within the template, i.e. `<a href="/rango/about/">About</a>`. This kind of hard coding of URLs means that if we change our URL mappings in `urls.py`, then we will have to also change all of these URL references. The preferred way is to use the template tag `url` to look up the URL in the `urls.py` files and dynamically insert the URL path. 

It's pretty simple to include relative URLs in your templates. To refer to the *About* page, we would insert the following line into our templates:

{lang="html",linenos=off}
	<a href="{% url 'about' %}">About</a>

The Django template engine will look up any `urls.py` module for a URL pattern with the attribute `name` set to `about` (`name='about'`), and then reverse match the actual URL. This means if we change the URL mappings in `urls.py`, we don't have to go through all our templates and update them. 

One can also reference a URL pattern without a specified name, by referencing the view directly as shown below.

{lang="html",linenos=off}
	<a href="{% url 'rango.views.about' %}">About</a>

In this example, we must ensure that the app `rango` has the view `about`, contained within its `views.py` module.

In your app's `index.html` template, you will notice that you have a parameterised URL pattern (the `show_category` URL/view takes the `category.slug` as a parameter). To handle this, you can pass the `url` template tag the name of the URL/view and the slug within the template, as follows:

{lang="html",linenos=off}
	{% for category in categories %}
	    <li>
	        <a href="{% url 'show_category' category.slug %}">
	            {{ category.name }}
	        </a>
	    </li>
	{% endfor %}

Before you run off to update all the URLs in all your templates with relative URLs, we need to restructure and refactor our templates by using inheritance to remove repetition.

T> ### URLs and Multiple Django Apps
T> This book focuses on the development on a single Django app, Rango. However, you may find yourself working on a Django project with multiple apps being used at once. This means that you could literally have hundreds of potential URLs with which you may need to reference. This scenario begs the question *how can we organise these URLs?* Two apps may have a view of the same name, meaning a potential conflict would exist. 
T>
T> [Django provides the ability to *namespace* URL configuration modules](http://django.readthedocs.io/en/1.9.x/intro/tutorial03.html#namespacing-url-names) (e.g. `urls.py`) for each individual app that you employ in your project. Simply adding an `app_name` variable to your app's `urls.py` module is enough. The example below specifies the namespace for the Rango app to be `rango`.
T>
T> {lang="python",linenos=off}
T> 	from django.conf.urls import url
T> 	from rango import views
T> 	
T> 	app_name = 'rango'
T> 	urlpatterns = [
T>	    url(r'^$', views.index, name='index'),
T>	    ...
T> 	]
T>
T> Adding an `app_name` variable would then mean that any URL you reference from the `rango` app could be done so like:
T>
T> {lang="html",linenos=off}
T> 	<a href="{% url 'rango:about' %}">About</a>
T> 
T> where the colon in the `url` command separates the namespace from the URL name.
T> Of course, this is an advanced feature for when multiple apps are in presence - but it is a useful trick to know when things start to scale up.


## Dealing with Repetition
While pretty much every professionally made website that you use will have a series of repeated components (such as page headers, sidebars, and footers, for example), repeating the HTML for each of these repeating components is not a particularly wise way to handle this. What if you wanted to change part of your website's header? You'd need to go through *every* page and change each copy of the header to suit. That could take a long time - and allow the possibility for human error to creep in.

Instead of spending (or wasting!) large amounts of time copying and pasting your HTML markup, we can minimise repetition in Rango's codebase by employing *template inheritance* provided by Django's template language.

The basic approach to using inheritance in templates is as follows.

1.  Identify the reoccurring parts of each page that are repeated across your application (i.e. header bar, sidebar, footer, content pane). Sometimes, it can help to draw up on paper the basic structure of your different pages to help you spot what components are used in common.
2.  In a *base template*, provide the skeleton structure of a basic page, along with any common content (i.e. the copyright notice that goes in the footer, the logo and title that appears in the section). Then, define a number of *blocks* which are subject to change depending on which page the user is viewing.
3.  Create specific templates for your app's pages - all of which inherit from the base template - and specify the contents of each block.


### Reoccurring HTML and The Base Template
Given the templates that we have created so far, it should be pretty obvious that we have been repeating a fair bit of HTML code. Below, we have abstracted away any page specific details to show the skeleton structure that we have been repeating within each template.

{lang="html",linenos=on}
	<!DOCTYPE html>
	{% load staticfiles %}
	
	<html>
	    <head lang="en">
	        <meta charset="UTF-8" />
	        <title>Rango</title>
	    </head>
	    <body>
	        <!-- Page specific content goes here -->
	    </body>
	</html>

For the time being, let's make this simple HTML page our app's base template. Save this markup in `base.html` within the `templates/rango/` directory (e.g. `templates/rango/base.html`).

W> ### `DOCTYPE` goes First!
W>
W> Remember that the `<!DOCTYPE html>` declaration *always needs to be placed on the first line* of your template.
W> Not having a [document type declaration](https://en.wikipedia.org/wiki/Document_type_declaration) on line one may mean that the resultant page generated from your template will not comply with [W3C HTML guidelines](https://www.w3.org/standards/webdesign/htmlcss).

### Template Blocks
Now that we've created our base template, we can add template tags to denote what parts of the template can be overridden by templates that inherit from it. To do this we will be using the `block` tag. For example, we can add a `body_block` to the base template in `base.html` as follows:

{lang="html",linenos=on}
	<!DOCTYPE html>
	{% load staticfiles %}
	
	<html>
	    <head lang="en">
	        <meta charset="UTF-8" />
	        <title>Rango</title>
	    </head>
	    <body>
	        {% block body_block %}
	        {% endblock %}
	    </body>
	</html>


Recall that standard Django template commands are denoted by `{%` and `%}` tags. To start a block, the command is `{% block <NAME> %}`, where `<NAME>` is the name of the block you wish to create. You must also ensure that you close the block with the `{% endblock %}` command, again enclosed within Django template tags.

You can also specify *default content* for your blocks, which will be used if no inheriting template defines the given block (see [further down](#section-templates-inheritance)). Specifying default content can be easily achieved by adding HTML markup between the `{% block %}` and `{% endblock %}` template commands, just like in the example below.

{lang="html",linenos=off}
	{% block body_block %}
	    This is body_block's default content.
	{% endblock %}

When we create templates for each page, we will inherit from `rango/base.html` and override the contents of `body_block`. However, you can place as many blocks in your templates as you so desire. For example, you could create a block for the page title, a block for the footer, a block for the sidebar, and more. Blocks are a really powerful feature of Django's templating system, and you can learn more about them check on [Django's official documentation on templates](https://docs.djangoproject.com/en/1.9/topics/templates/).

I> ### Extract Common Structures
I>
I> You should always aim to extract as much reoccurring content for your base templates as possible. While it may be a hassle to do, the time you will save in maintenance will far outweigh the initial overhead of doing it up front.
I>
I> *Thinking hurts, but it is better than doing lots of grunt work!*


### Abstracting Further
Now that you have an understanding of blocks within Django templates, let's take the opportunity to abstract our base template a little bit further. Reopen the `rango/base.html` template and modify it to look like the following.

{lang="html",linenos=on}
	<!DOCTYPE html>
	{% load staticfiles %}
	
	<html>
	    <head>
	        <title>
	            Rango - 
	            {% block title_block %} 
	                How to Tango with Django!
	            {% endblock %}
	        </title>
	    </head>
	    <body>
	        <div>
	            {% block body_block %}
	            {% endblock %}
	        </div>
	        <hr />
	        <div>
	            <ul>
	                <li><a href="{% url 'add_category' %}">Add New Category</a></li>
	                <li><a href="{% url 'about' %}">About</a></li>
	                <li><a href="{% url 'index' %}">Index</a></li>
	            </ul>
	        </div>
	    </body>
	</html>

From the example above, we have introduced two new features into the base template.

-   The first is a template block called `title_block`. This will allow us to specify a custom page title for each page inheriting from our base template. If an inheriting page does not override the block, then the `title_block` defaults to `How to Tango with Django!`, resulting in a complete title of `Rango - How to Tango with Django!`. Look at the contents of the `<title>` tag in the above template to see how this works.
-   We have also included the list of links from our current `index.html` template and placed them into a HTML `<div>` tag underneath our `body_block` block. This will ensure the links are present across all pages inheriting from the base template. The links are preceded by a *horizontal rule* (`<hr />`) which provides a visual separation for the user between the content of the `body_block` block and the links.

## Template Inheritance {#section-templates-inheritance}
Now that we've created a base template with blocks, we can now update all the templates we have created so that they inherit from the base template. Let's start by refactoring the template `rango/category.html`.

To do this, first remove all the repeated HTML code leaving only the HTML and template tags/commands specific to the page. Then at the beginning of the template add the following line of code:

{lang="html",linenos=off}
	{% extends 'rango/base.html' %}

The `extends` command takes one parameter - the template that is to be extended/inherited from (i.e. `rango/base.html`). The parameter you supply to the `extends` command should be relative from your project's `templates` directory. For example, all templates we use for Rango should extend from `rango/base.html`, not `base.html`. We can then further modify the `category.html` template so it looks like the following complete example.

{lang="html",linenos=on}
	{% extends 'rango/base.html' %}
	{% load staticfiles %}
	
	{% block title_block %}
	    {{ category.name }}
	{% endblock %}
	
	{% block body_block %}
	    {% if category %}
	        <h1>{{ category.name }}</h1>
	        
	        {% if pages %}
	            <ul>
	            {% for page in pages %}
	                <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	            {% endfor %}
	            </ul>
	        {% else %}
	            <strong>No pages currently in category.</strong>
	        {% endif %}
	        <a href="{% url 'add_page' category.slug %}">Add a Page</a>
	    {% else %}
	        The specified category does not exist!
	    {% endif %}
	{% endblock %}

W> ### Loading `staticfiles`
W> You'll need to make sure you add `{% load staticfiles %}` to the top of **each template** that makes use of static media. If you don't, you'll get an error! Django template modules must be imported individually for each template that requires them. If you've programmed before, this works somewhat differently from object orientated programming languages such as Java, where imports cascade down inheriting classes.
Notice how we used the `url` template tag to refer to `rango/<category-name>/add_page/` URL pattern. The `category.slug` is passed through as a parameter to the `url` template tag and Django's Template Engine will produce the correct URL for us.

Now that we inherit from `rango/base.html`, the `category.html` template is much cleaner extending the `title_block` and `body_block` blocks. You don't need a well-formatted HTML document because `base.html` provides all the groundwork for you. All you're doing is plugging in additional content to the base template to create the complete, rendered HTML document that is sent to the client's browser. This rendered HTML document will then conform to the standards, containing components such as the document type declaration on the first line.


I> ### More about Templates 
I> Here we have shown how we can minimise the repetition of structure HTML in our templates. However, the Django templating language is very powerful, and even lets you create your own template tags.
I>
I> Templates can also be used to minimise code within your application's views. For example, if you wanted to include the same database driven content on each page of your application, you could construct a template that calls a specific view to handle the repeating portion of your app's pages. This then saves you from having to call the Django ORM functions that gather the required data for the template in every view that renders it.
I>
I> If you haven't already done so, now would be a good time to read through the official [Django documentation on templates](https://docs.djangoproject.com/en/1.9/topics/templates/).


X> ### Exercises
X> Now that you've worked through this chapter, there are a number of exercises that you can work through to reinforce what you've learnt regarding Django and templating.
X>
X> - Update all other previously defined templates in the Rango app to extend from the new `base.html` template. Follow the same process as we demonstrated above. Once completed, your templates should all inherit from `base.html`. 
X> - While you're at it, make sure you remove the links from our `index.html` template. We don't need them anymore! You can also remove the link to Rango's homepage within the `about.html` template. 
X> - When you refactor the `index.html` keep the images that are served up from the static files and media server.
X> - Update all references to Rango URLs by using the `url` template tag. You can also do this in your `views.py` module too - check out the [`reverse()` helper function](https://docs.djangoproject.com/en/1.9/ref/urlresolvers/#reverse).


T> ### Hints
T> - Start refactoring the `about.html` template first.
T> - Update the `title_block` then the `body_block` in each template.
T> - Have the development server running and check the page as you work on it. Don't change the whole page to find it doesn't work. Changing things incrementally and testing those changes as you go is a much safer solution.
T> - To reference the links to category pages, you can use the following template code, paying particular attention to the Django template `{% url %}` command.
T>
T> {lang="html",linenos=off}
T> 		<a href="{% url 'show_category' category.slug %}">{{ category.name }}</a>

<!-->
![A class diagram demonstrating how your templates should inherit from
`base.html`.](../images/rango-template-inheritance.svg)
-->

## The `render()` Method and the `request` Context
When writing views we have used a number of different methods, the preferred way is to use the Django shortcut method `render()`. The `render()` method requires that you pass through the `request` as the first argument. The `request` context houses a lot of information regarding the session, the user, etc, see the [Official Django Documentation on Request objects](https://docs.djangoproject.com/en/1.9/ref/request-response/#httprequest-objects). By passing the `request` through to the template mean that you will also have access to such information when creating templates. In the next chapter we will access information about the `user` - but for now check through all of your views and make sure that they have been implemented using the `render()` method. Otherwise, your templates won't have the information we need later on.

I> ### Render and Context
I> As a quick example of the checks you must carry out, have a look at the `about()` view. Initially, this was implemented with a hard-coded string response, as shown below. Note that we only send the string - we don't make use of the request passed as the `request` parameter.
I>
I> {lang="python",linenos=off}
I> 	def about(request):
I> 	    return HttpResponse('Rango says: Here is the about page.
I> 	                         <a href="/rango/">Index</a>')
I>
I> To employ the use of a template, we call the `render()` function and pass through the `request` object. This will allow the template engine to access information such as the request type (e.g. `GET`/`POST`), and information relating to the user's status (have a look at [Chapter 9](#chapter-user)).
I>
I> {lang="python",linenos=off}
I> 	def about(request):
I>	    # prints out whether the method is a GET or a POST
I>	    print(request.method)
I>	    # prints out the user name, if no one is logged in it prints `AnonymousUser`
I>	    print(request.user)
I>	    return render(request, 'rango/about.html', {})
I>
I> Remember, the last parameter of `render()` is the context dictionary with which you can use to pass additional data to the Django template engine. As we have no additional data to give to the template, we pass through an empty dictionary, `{}`. 


## Custom Template Tags
It would be nice to show the different categories that users can browse through in the sidebar on each page. Given what we have learnt so far, we could do the following:

- in the `base.html` template, we could add some code to display an item list of categories; and
- within each view, we could access the `Category` object, get all the categories, and return that in the context dictionary.

However, this is a pretty nasty solution because we will need to be repeatedly including the same code in all views. A [DRYer](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) solution would be to create custom template tags that are included in the template, and which can request *their own* data.

### Using Template Tags
Create a directory `rango/templatetags`, and create two new modules within it. One must be called `__init__.py`, and this will be kept blank. Name the second module `rango_template_tags.py`. Add the following code to this second module.

{lang="python",linenos=on}
	from django import template
	from rango.models import Category
	
	register = template.Library()
	
	@register.inclusion_tag('rango/cats.html')
	def get_category_list():
	    return {'cats': Category.objects.all()}

From this code snippet, you can see a new method called `get_category_list()`. This method returns a list of categories - but is mashed up with the template `rango/cats.html` (as can be seen from the `register.inclusion_tag()` decorator). You can now create this template file, and add the following HTML markup:

{lang="html",linenos=on}
	<ul>
	{% if cats %}
	    {% for c in cats %}
	        <li><a href="{% url 'show_category'  c.slug %}">{{ c.name }}</a></li>
	    {% endfor %}
	{% else %}
	    <li><strong>There are no categories present.</strong></li>
	{% endif %}
	</ul>

To use the template tag in your `base.html` template, first load the custom template tag by including the command `{% load rango_template_tags %}` at the top of the `base.html` template. You can then create a new block to represent the sidebar - and we can call our new template tag with the following code.

{lang="html",linenos=off}
	<div>
	    {% block sidebar_block %}
	        {% get_category_list %}
	    {% endblock %}
	</div>

Try it out. Now all pages that inherit from `base.html` will also include the list of categories (which we will move to the side later on). 

T> ### Restart the Server!
T> You'll need to restart the Django development server (or ensure it restarted itself) every time you modify template tags. If the server doesn't restart, Django won't register the tags.

### Parameterised Template Tags 
We can also *parameterise* the template tags we create, allowing for greater flexibility. As an example, we'll use parameterisation to highlight which category we are looking at when visiting its page. Adding in a parameter is easy - we can update the `get_category_list()` method as follows.

{lang="python",linenos=off}
	def get_category_list(cat=None):
	    return {'cats': Category.objects.all(),
	            'act_cat': cat}

Note the inclusion of the `cat` parameter to `get_category_list()`, which is optional - and if you don't pass in a category, `None` is used as the subsequent value.

We can then update our `base.html` template which makes use of the custom template tag to pass in the current category - but only if it exists.

{lang="html",linenos=off}
	<div>
	    {% block sidebar_block %}
	        {% get_category_list category %}
	    {% endblock %}
	</div>

We can also now update the `cats.html` template, too.

{lang="html",linenos=off}
	{% for c in cats %}
	    {% if c == act_cat %}
	        <li>
	        <strong>
	              <a href="{% url 'show_category' c.slug %}">{{ c.name }}</a>
	        </strong>
	        </li>
	    {% else  %}
	        <li>
	            <a href="{% url 'show_category' c.slug %}">{{ c.name }}</a>
	        </li>
	    {% endif %}
	{% endfor %}

In the template, we check to see if the category being displayed is the same as the category being passed through during the `for` loop (i.e. `c == act_cat`). If so, we highlight the category name by making it **bold** through use of the `<strong>` tag. 

## Summary
In this chapter, we showed how we can:

- reduce coupling between URLs and templates by using the `url` template tag to point to relative URLs;
- reduced the amount of boilerplate code by using template inheritance; and
- avoid repetitive code appearing in views by creating custom templates tags.

Taken together, your template code should be much cleaner and easier to maintain. Of course, Django templates offer a lot more functionality - find out more by visiting the [Official Django Documentation on Templates](https://docs.djangoproject.com/en/1.9/ref/templates/).