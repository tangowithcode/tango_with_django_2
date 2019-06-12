# Adding Search to Rango {#chapter-bing}
Now that most of the core functionality of Rango has been implemented (and it looks good, too!), we can move to addressing some more advanced functionality. In this chapter, we will connect Rango up to a *search API* so that users can also *search* for pages, rather than simply *browse* categories. Therefore, the main point of this chapter is to show you how you can connect and use other web services -- and how to integrate them within your own Django app.

The search API that we will be using will be *Microsoft's Bing Search API*. However, you could just as readily use any available search API, such as those provided by [Webhose](https://webhose.io/) or [Yandex](https://yandex.com/support/search/robots/search-api.html).

To use the Bing Search API, we will need to write a [wrapper](https://en.wikipedia.org/wiki/Adapter_pattern), which enables us to send a query and obtain the results from Bing's API -- all the while returning results to us in a convenient format that we can readily use in our code. However, before we can do so, we first need to set up a Microsoft Azure account to use the Bing Search API.

## The Bing Search API
The [Bing Search API](https://docs.microsoft.com/en-gb/rest/api/cognitiveservices/bing-web-api-v7-reference) provides you with the ability to embed search results from the Bing search engine within your own applications. Through a straightforward interface, you can request results from Bing's servers to be returned in either XML or JSON. The data returned can then be interpreted by a XML or JSON parser, with the results then, for example, rendered as part of a template within your application.

Although the Bing API can handle requests for different kinds of content, we'll be focusing on web search only for this tutorial, with JSON-formatted responses. To use the Bing Search API, you will need to sign up for an *API key*. The key currently provides subscribers with access to 3000 queries per month, which should be more than enough for our experimental purposes.

I> ### Application Programming Interface (API)
I> An [Application Programming Interface](http://en.wikipedia.org/wiki/Application_programming_interface) specifies how software components should interact with one another. In the context of web applications, an API is considered as a set of HTTP requests along with a definition of the structures of response messages that each request can return. Any meaningful service that can be offered over the Internet can have its own API. We aren't limited to web search! For more information on web APIs, [Luis Rei provides an excellent tutorial on APIs](http://blog.luisrei.com/articles/rest.html).


### Registering for a Bing API Key
To obtain a Bing API key, you must first register for a Microsoft Azure account. The account provides you with access to a wide range of Microsoft services. If you already have a Microsoft account, you dont need to register you can log in. Otherwise, you can go online and create a free account with Microsoft at [`https://account.windowsazure.com`](https://account.windowsazure.com).

When your account has been created, log in and go to the portal. The link is at the top right of the page.

Once the portal has loaded, you should see a list of options down the left-hand side of the viewport. Find the top option called `Create a resource` and click it. The right-hand side of the page will then be populated with more lists. From there, find the `AI + Machine Learning` option and select that. Scroll through the options on the subsequent menu that appears, and select the `Bing Search v7` option.

W> ### Entering Personal Information
W> At this stage, you may be redirected to a page where you have to supply details such as your address and payment card. Microsoft says that this information is required to ensure that spammers and bots do not infiltrate their services -- and rest assured, if you need to provide payment details, no money will be taken from your bank account unless you specifically authorise it. We will be using the free Bing Search API allowance, so no money will need to be transferred.
W> If you do need to provide this information, you'll need to head back to the portal and look for the `Bing Search v7` option once more.

You'll then be greeted with a page similar to [the one below](#fig-azure-create). Here, you need to provide a name for your Bing Search service -- something like `rango_bing_search` will do the job nicely. Ensure that you select `Free Trial` for the subscription, and pricing tier `T0` (allowing 3000 free requests per month). Selecting these options will ensure that you will not be charged for access to the API. You'll also need to make a new group -- we made one called `rango`. The resource location doesn't really matter as we won't be worrying about things like response times and the like. Once you are happy, click `Create` at the bottom of the page.

{id="fig-azure-create"}
![Creating a free Bing Search API resource in the Microsoft Azure web application.](images/ch14-azure-create.png)

You'll then need to wait for the resource to be created -- this will take a few minutes. After it has been created, you should see a screen confirming that your new resource has been created. On that screen, click the `Go to resource` button.

A new page will then load. Here, you should look for the `Keys` option under the `Resource Management` header. You should see the screen like the one below. The keys in this figure are deliberately obscured. Take a note of each of the three items on this page -- `name`, `key 1` and `key 2`. Copy the values of each field into a text file and save it somewhere, but not in your Git repository! The keys you save here will be required when we attempt to access the Bing Search API later on.

{id="fig-azure-keys"}
![The keys screen for the Bing Search API resource. Make sure you take a note of the `name`, `key 1` and `key 2` values! You will need them later on.](images/ch14-azure-keys.png)

## Adding Search Functionality
Below we have provided the code that we can use to issue queries to the Bing search service. Create a file called `rango/bing_search.py` and import the following code. You will note that we need to import a package called `requests` so that we can make web requests. However, to use the `requests` package you will need to run, `pip install requests` to install it with your virtual environment, first.

{lang="python",linenos=on}
	import json
	import requests

	# Add your Microsoft Account Key to a file called bing.key
	def read_bing_key():
		"""
		reads the BING API key from a file called 'bing.key'
		returns: a string which is either None, i.e. no key found, or with a key
		remember to put bing.key in your .gitignore file to avoid committing it to the repo.
	
		See Python Anti-Patterns - it is an awesome resource to improve your python code
		Here we using "with" when opening documents
		http://bit.ly/twd-antipattern-open-files
		"""
	
		bing_api_key = None
		try:
			with open('bing.key','r') as f:
				bing_api_key = f.readline().strip()
			
		except:
			raise IOError('bing.key file not found')
		
		if not bing_api_key:
			raise KeyError('Bing key not found')	
	
		return bing_api_key

	def run_query(search_terms):
		"""
		See the Microsoft's documentation on other parameters that you can set.
		http://bit.ly/twd-bing-api
		"""
		bing_key = read_bing_key()
		search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
		headers = {"Ocp-Apim-Subscription-Key" : bing_key}
		params  = {"q": search_terms, "textDecorations":True, "textFormat":"HTML"}
		response = requests.get(search_url, headers=headers, params=params)
		response.raise_for_status()
		search_results = response.json()
		results = []
		for result in search_results["webPages"]["value"]:
			results.append({
				'title': result['name'],
				'link': result['url'],
				'summary': result['snippet']})
		return results


I> ### Python Anti-Patterns
I> In the wrapper we avoided problems with opening files (and not remembering to close them) by using the `with` command.
I> Opening the file directly is a common anti-pattern that should be avoided.
I> To find out more about anti-patterns in Python, then check out the [Little Book of Python Anti-Patterns](http://bit.ly/twd-python-anti-patterns).
I> It is an awesome resource that will help you to improve your python code.


In the module(s) above, we have implemented two functions: one to retrieve your Bing API key from a local file, and another to issue a query to the Bing search engine. Below, we discuss how both of the functions work.

### `read_bing_key()` - Reading the Bing Key {#section-bing-adding-key}
The `read_bing_key()` function reads in your key from a file called `bing.key`, located in your Django project's root directory (i.e. `<workspace>/tango_with_django/`). We have created this function because if you are putting your code into a public repository on GitHub for example, you should take some precautions to avoid sharing your API Key publicly. 

From the Azure website, take a copy of your *Account key* and save it into `<workspace>/tango_with_django/bing.key`. The key should be the only contents of the file - nothing else should exist within it. This file should NOT be committed to your GitHub repository. To make sure that you do not accidentally commit it, update your repository's `.gitignore` file to exclude any files with a `.key` extension, by adding the line `*.key`. This way, your key file will only be stored locally and you will not end up with someone using your query quota (or worse).
	
T> ### Keys and Rings
T>
T> Keep them secret, keep them safe!


### `run_query()` - Executing the Query
The `run_query()` function takes a query as a string, and returns the top ten results from Bing in a list that contains a dictionary of the result items (including the `title`, a `link`, and a `summary`). 

To summarise though, the logic of the `run_query()` function can be broadly split into six main tasks.

* First, the function prepares for connecting to Bing by preparing the URL that we'll be requesting.
* The function then prepares authentication, making use of your Bing API key. This is obtained by calling `read_bing_key()`, which in turn pulls your Account key from the `bing.key` file you created earlier.
* The response is then parsed into a Python dictionary object using the `json` Python package.
* We loop through each of the returned results, populating a `results` dictionary. For each result, we take the `title` of the page, the `link` or URL and a short `summary` of each returned result.
* The list of dictionaries is then returned by the function.

<!-->
Notice that results are passed from Bing's servers as JSON. This is because they by default return the results using JSON. 

Also, note that if an error occurs when attempting to connect to Bing's servers, the error is printed to the terminal via the `print` statement within the `except` block.
-->

I> ###Bing it on!
I> There are many different parameters that the Bing Search API can handle which we don't cover here. 
I> If you want to know more about the API check out the [Bing Search API Documentation](https://docs.microsoft.com/en-gb/rest/api/cognitiveservices/bing-web-api-v7-reference).

X> ### Exercises
X> Extend your `bing_search.py` module so that it can be run independently, i.e. running `python bing_search.py` from your terminal or Command Prompt. Specifically, you should implement functionality that:
X> 
X> - prompts the the user to enter a query, i.e. use `raw_input()`; and
X> - issues the query via `run_query()`, and prints the results.
X>
X> Update the `run_query()` method so that it handles network errors gracefully.


T> ### Hint
T> Add the following code, so that when you run `python bing_search.py` it calls the `main()` function:
T> 	
T> {lang="python",linenos=off}
T>		def main():
T>		    #insert your code here
T>		
T>		if __name__ == '__main__':
T>		    main()
T>
T> When you run the module explicitly via `python bing_search.py`, the `bing_search` module is treated as the `__main__` module, and thus triggers `main()`. However, when the module is imported by another module, then `__name__` will not equal `__main__`, and thus the `main()` function not be called. This way you can `import` it with your application without having to call `main()`.


## Putting Search into Rango
Now that we have successfully implemented the search functionality module, we need to integrate it into our Rango app. There are two main steps that we need to complete for this to work.

- We must first create a `search.html` template that extends from our `base.html` template. The `search.html` template will include a HTML `<form>` to capture the user's query as well as template code to present any results.
- We then create a view to handle the rendering of the `search.html` template for us, as well as calling the `run_query()` function we defined above.

### Adding a Search Template
Let's first create a template called, `rango/search.html`. Add the following HTML markup, Django template code, and Bootstrap classes.

{lang="html",linenos=on}
	{% extends 'rango/base.html' %}
	{% load staticfiles %}
	{% block title %} Search {% endblock %}
	{% block body_block %}
	<div>
	    <h1>Search with Rango</h1>
	    <br/>
	    <form class="form-inline" id="user_form" 
	          method="post" action="{% url 'rango:search' %}">
	        {% csrf_token %}
	        <div class="form-group">
	            <input class="form-control" type="text" size="50" 
	                   name="query" value="" id="query" />
	        </div>
	        <button class="btn btn-primary" type="submit" name="submit"
	                value="Search">Search</button>
	    </form>
	    <div>
	        {% if result_list %}
	        <h3>Results</h3>
	        <!-- Display search results in an ordered list -->
	        <div class="list-group">
	        {% for result in result_list %}
	            <div class="list-group-item">
	            <h4 class="list-group-item-heading">
	            <a href="{{ result.link }}">{{ result.title|safe|escape}}</a>
	            </h4>
	            <p class="list-group-item-text">{{ result.summary|safe|escape }}</p>
	            </div>
	        {% endfor %}
	        </div>
	        {% endif %}
	    </div>
	</div>	
	{% endblock %}

The template code above performs two key tasks.

- In all scenarios, the template presents a search box and a search buttons within a HTML `<form>` for users to enter and submit their search queries.
- If a `results_list` object is passed to the template's context when being rendered, the template then iterates through the object displaying the results contained within.
	
To style the HTML, we have made use of Bootstrap [jumbotron](https://getbootstrap.com/docs/4.2/components/jumbotron/), [list groups](https://getbootstrap.com/docs/4.2/components/list-group/), and [forms](https://getbootstrap.com/docs/4.2/components/forms/).

To render the title and summary correctly, we have used the `safe` and `escape` tags to inform the template that the `result.title` and `result.summary` should be rendered as is (i.e. as HTML).

In the view code, in the next subsection, we will only pass through the results to the template, when the user issues a query. Initially, there will be no results to show.

### Adding the View
With our search template added, we can then add the view that prompts the rendering of our template. Add the following `search()` view to Rango's `views.py` module.

{lang="python",linenos=off}	
	def search(request):
	    result_list = []
	    
	    if request.method == 'POST':
	        query = request.POST['query'].strip()
	        if query:
	            # Run our Bing function to get the results list!
	            result_list = run_query(query)
	    
	    return render(request, 'rango/search.html', {'result_list': result_list})
	
The code should be pretty self explanatory. 
The only major addition is that we have called the `run_query()` function we defined earlier in this chapter. 
To call it though, we need to import the `bing_search.py` module. 
So check that before you run the script that you add the following `import` statement at the top of the `views.py` module.

{lang="python",linenos=off}
	from rango.bing_search import run_query, read_bing_key

You'll also need to ensure you do the following, too.

- Add a mapping between your `search()` view and the `/rango/search/` URL calling it `name='search'` by adding in `path('search/', views.search, name='search'),` to `rango/urls.py`.
- Also, update the `base.html` navigation bar to include a link to the search page. Remember to use the `url` template tag to reference the link.
- You will need a copy of the `bing.key` in your project's root directory (`<workspace>/tango_with_django_project`, alongside `manage.py`).

Once you have put in the URL mapping and added a link to the search page, you should now be able issue queries to the Bing Search API and have the results shown within the Rango app (as shown in the figure below).

{id="fig-bing-python-search"}
![Searching for "Python for Noobs".](images/ch14-bing-python-search.png)

X> ### Search Box Exercise
X>
X> You may notice that when you issue a query, the query disappears when the results are shown. This is not very user friendly. Update the view and template so that the user's query is displayed within the search box.
X>
X> Within the view, you will need to put the `query` into the context dictionary. Within the template, you will need to show the query text in the search box.