# Automated Testing {#chapter-testing}
If you're new to software development, it would be a good thing to get into the habit of writing and developing tests for the code you write. A lot of software engineering is about writing and developing tests and test suites to ensure the developed software is robust. Of course, most of the time, we are too busy trying to build things to bother about making sure that they work -- or too arrogant to believe that what we create would fail!

However, trust us. **Through our experiences writing code in both industrial and academic settings, writing tests have saved us. On multiple occasions.** They are a vital part of a software engineer's toolbox, and provide you with confidence that the software you write does what you think it will!

According to the [Django Tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial05/), there are numerous reasons why you should include tests. Several key reasons listed are repeated below.

- **Writing tests will save you time.** Even a slight change in a complex system can cause failures in places that you simply wouldn't think of.
- **Tests don't just identify problems, they prevent them.** Tests show where the code is not meeting expectations.
- **Test make your code more attractive.** *"Code without tests is broken by design"* -- Jacob Kaplan-Moss, one of Django's original developers.
- **Tests help teams work together.** You want to be a team player, right? Then write tests. Writing tests will make sure your team doesn't inadvertently break your code, or you don't break the code of your team members!

In addition to these reasons, the [Python Guide](http://docs.python-guide.org/en/latest/writing/tests/) lists several general rules that you should try to follow when writing tests. Below are some of the main rules.

1. Tests should focus on *one small bit of functionality.*
2. Tests should have a *clear purpose.*
3. Tests should be *independent from your existing codebase.*
4. Run your tests before you code. Make sure everything works before you start.
5. Run your tests after you code, but before you `commit` and `push`. Make sure you haven't broken anything.
	- Why not write a hook that executes your tests every time you do a `commit`?
7. The longer and more descriptive the names you give for your tests, the better.

I> ### Testing in Django
I> This chapter provides the very basics of testing with Django, and follows a similar structure to the [Django Tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial05/) -- with some additional notes. If there is a strong desire from readers for us to expand this chapter further, we will! Get in touch if you think this would be advantageous to you.

## Running Tests
Django comes complete with a suite of tools to test the apps that you build. You can test your developed Rango app by using the terminal or Command Prompt. Simply issue the following command, and observe the output you see.

{lang="text",linenos=off}
	$ python manage.py test rango
	
	Creating test database for alias 'default'...
	
	----------------------------------------------------------------------
	Ran 0 tests in 0.000s
	
	OK
	Destroying test database for alias 'default'...

This command will run through all tests that have been created for the Rango app. However, at the moment, nothing much happens. This is because the `tests.py` that lives inside the `rango` app directory is pretty much blank, except for a single `import` statement. Every time you create a new Django app, this nearly-blank `tests.py` module is created for you to encourage you to write tests!

From the output shown above, you might also notice that a database called `default` is referred to. When you run tests, a temporary database is constructed, which your tests can populate and perform operations on. This way your testing is *performed independently* of your live database, satisfying one of the rules we listed above.

### Testing Rango's Models
Given that there are presently no tests, let's create one! In the `Category` model, we want to ensure that the number of views received is zero or greater because you cannot have a negative number of views. To create a test for this, we can put the following code into Rango's `tests.py` module, being careful to keep the existing `import` statement.

{lang="python", linenos=off}
	class CategoryMethodTests(TestCase):
        def test_ensure_views_are_positive(self):
            """
            Ensures the number of views received for a Category are positive or zero.
            """
            category = Category(name='test', views=-1, likes=0)
            category.save()
            
            self.assertEqual((category.views >= 0), True)

You'll also want to make sure that you `import` the `Category` model.

{lang="python", linenos=off}
	from rango.models import Category

The first thing to notice about the test we have written is that we must place the tests within a class. This class must inherit from `django.test.TestCase`. Each method implemented within a class tests a particular piece of functionality. These methods should always have a name that starts with `test_`, and should always contain some form of assertion. In this example, we use `assertEqual` which checks whether two items are equal. However, there are lots of other assert checks you can use -- as demonstrated in the [official Python documentation](https://docs.python.org/3/library/unittest.html#assert-methods). Django's testing machinery is derived from the Python implementation, but also provides several asserts and specific test cases unique to Django and web development.

If we then run the test, we will see the following output.

{lang="text",linenos=off}
	$ python manage.py test rango
	
	Creating test database for alias 'default'...
	F
	======================================================================
	FAIL: test_ensure_views_are_positive (rango.tests.CategoryMethodTests)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	    File "/Users/maxwelld90/Workspace/tango_with_django_project/rango/tests.py", 
	    line 12, in test_ensure_views_are_positive
	    self.assertEqual((cat.views>=0), True)
	    AssertionError: False != True
	    
	----------------------------------------------------------------------
	Ran 1 test in 0.001s
	
	FAILED (failures=1)

We can see that Django picked up our solitary test, and it `FAILED`. This is because the model does not check whether the value for `views` is less than zero. Since we want to ensure that the values are non-zero for this particular field, we will need to update the model to ensure that this requirement is fulfilled. Update the model now by adding some code to the `save()` method of the `Category` model, located in Rango's `models.py` module. The code should check the value of the `views` attribute, and update it accordingly if the value provided is less than zero. A simple conditional check on `self.views` should suffice.

Once you have updated your model, re-run the test. See if your code now passes the test. If not, try again and work out a solution that passes the test. 

Let's try adding a further test that ensures that an appropriate `slug` is created. This should mean a slug with dashes instead of spaces (`-`), and all in lowercase. Add the following test method to your new `CategoryMethodTests` class.

{lang="python", linenos=off}
	def test_slug_line_creation(self):
	    """
	    Checks to make sure that when a category is created, an
	    appropriate slug is created.
	    Example: "Random Category String" should be "random-category-string".
	    """
	    category = Category(name='Random Category String')
	    category.save()
	    
	    self.assertEqual(category.slug, 'random-category-string')

Run the tests again. Does your code pass both tests? You should now be starting to see that if you have tests written up that you are confident satisfy the requirements of a particular component, you can write code that complies with these tests -- ergo your code satisfies the requirements provided!

### Testing Views
The two simple tests that we have written so far focus on ensuring the integrity of the data housed within Rango's `Category` model. Django also provides mechanisms to test views. It does this with a mock client (or browser) that internally makes calls to the Django development server via a URL. In these tests, you have access to the server's response (including the rendered HTML markup), as well as the context dictionary that was used.

To demonstrate this testing feature, we can create a test that checks when the index page loads. When the `Category` model is empty, it should present the user with a message that *exactly* says `There are no categories present`.

{lang="python",linenos=off}
	class IndexViewTests(TestCase):
	    def test_index_view_with_no_categories(self):
	        """
	        If no categories exist, the appropriate message should be displayed.
	        """
	        response = self.client.get(reverse('rango:index'))
	        
	        self.assertEqual(response.status_code, 200)
	        self.assertContains(response, "There are no categories present")
	        self.assertQuerysetEqual(response.context['categories'], [])

As we are using the Django `reverse()` function to perform a URL lookup, we'll need to make sure that the correct `import` statement is included at the top of the `tests.py` module, too.

{lang="python",linenos=off}
	from django.urls import reverse

Looking at the code above, the Django `TestCase` class has access to a `client` object which can make requests. Here, it uses the helper function `reverse()` to lookup the URL of Rango's `index` page. It then tries to issue an HTTP `GET` request on that page. The response is returned and stored in `response`. The test then checks several things: whether the page loaded successfully (with a `200` status code returned); whether the response's HTML contains the string `"There are no categories present"`; and whether the context dictionary used to render the response contains an empty list for the `categories` supplied.

Recall that when you run tests, a new database is created, which by default is not populated. This is true for each test method -- and explains why the categories you create in the two `CategoryMethodTests` tests are not visible to the test in `IndexViewTests`.

Now let's check the `index` view when categories *are* present. We can add a helper function for us to achieve this. This simple function doesn't live within a class -- just place it in the `test.py` module.

{lang="python",linenos=off}
	def add_category(name, views=0, likes=0):
	    category = Category.objects.get_or_create(name=name)[0]
	    category.views = views
	    category.likes = likes
	    
	    category.save()
	    return category

`add_category()` takes a `name` string, `views` and `likes` integers, and adds the category to the `Category` model, returning a reference to the model instance it creates (or retrieves, if it already exists). Note that `views` and `likes` are set to optional parameters, defaulting to zero if they are not supplied.

Make use of this helper method by creating a further test method inside your `IndexViewTests` class.

{lang="python",linenos=off}
	def test_index_view_with_categories(self):
	    """
	    Checks whether categories are displayed correctly when present.
	    """
	    add_category('Python', 1, 1)
	    add_category('C++', 1, 1)
	    add_category('Erlang', 1, 1)
	    
	    response = self.client.get(reverse('rango:index'))
	    self.assertEqual(response.status_code, 200)
	    self.assertContains(response, "Python")
	    self.assertContains(response, "C++")
	    self.assertContains(response, "Erlang")
	    
	    num_categories = len(response.context['categories'])
	    self.assertEquals(num_categories, 3)

In this test, we populate the database with three sample categories, `Python`, `C++` and `Erlang`. We make use of our helper function `add_category()` here. We then again request the `index` page, check the response was successful (HTTP `200`), and check whether all three categories are presented on the page. We also check the number of categories listed in the context dictionary is equal to three -- the number of categories present in the database at the time.

Run the test. Does it pass?

X> ### Update your Existing Tests
X> Update the existing tests that you have created so far to make use of the helper `add_category()` function.

### Testing the Rendered Page
Django's test suite also allows you to perform tests that load up your web app, and programmatically interact with the DOM elements on the rendered HTML pages. This is incredibly useful, as you can test your web app as a human would -- by 'clicking' links, or entering information into form fields and submitting them. This is achieved with some further third-party "driver" software that controls interactions on a webpage for you.

We don't explicitly cover how to set these tests up here, but you should refer to the [official Django documentation](https://docs.djangoproject.com/en/2.2/topics/testing/tools/#liveservertestcase) to learn more and see how this is achieved.

If you really want us to include examples of how to run tests this way, let us know!

## Examining Testing Coverage
One further point of discussion about testing is *coverage.* Code coverage measures how much of your codebase has been tested. You can install an additional package called `coverage` (`$pip install coverage`) that can automatically analyse how much of your codebase that has been covered by tests. Once `coverage` is installed, run the following command at your terminal or Command Prompt.

{lang="text",linenos=off}
	$ coverage run --source='.' manage.py test rango

This will run through all of the tests that you have implemented so far, and collect coverage data for the Rango app. To see the report, you then need to type the following command once the first command is completed.

{lang="text",linenos=off}
	$ coverage report
	Name                                          Stmts   Miss  Cover
	-----------------------------------------------------------------
	manage.py                                         9      2    78%
	populate_rango.py                                32     32     0%
	rango/__init__.py                                 0      0   100%
	rango/admin.py                                    9      0   100%
	rango/apps.py                                     3      3     0%
	rango/bing_search.py                             36     30    17%
	rango/forms.py                                   34      6    82%
	rango/migrations/0001_initial.py                  6      0   100%
	rango/migrations/0002_auto_20190325_1352.py       4      0   100%
	rango/migrations/0003_category_slug.py            4      0   100%
	rango/migrations/0004_auto_20190610_1139.py       6      0   100%
	rango/migrations/__init__.py                      0      0   100%
	rango/models.py                                  33      3    91%
	rango/templatetags/__init__.py                    0      0   100%
	rango/templatetags/rango_template_tags.py         6      0   100%
	rango/tests.py                                   35      0   100%
	rango/urls.py                                     4      0   100%
	rango/views.py                                  204    134    34%
	tango_with_django_project/__init__.py             0      0   100%
	tango_with_django_project/settings.py            29      0   100%
	tango_with_django_project/urls.py                12      1    92%
	tango_with_django_project/wsgi.py                 4      4     0%
	-----------------------------------------------------------------
	TOTAL                                           470    215    54%

We can see from the output of this command that critical parts of the code have not been tested. The `views.py` has a pretty low coverage percentage as an example of 34%. Therefore, this output can provide you with a measure-based approach to determine where to focus your efforts on writing tests.

The `coverage` package [has many more features](https://coverage.readthedocs.io/en/latest/) that you can explore to make your tests even more comprehensive!

X> ### Testing Exercises
X> Let's assume that we want to extend the `Page` model to include an additional field -- `last_visit`. This field will be of the type `models.DateTimeField`, and represents the date and time when the page was last accessed. If the page has never been accessed, the value given will be the date and time at which the page was saved -- whether this was the initial creation or an update. Given this requirement, complete the following tasks.
X>
X> - Update the `Page` model to include this new field.
X> - Update the `Page` model to set this value on creation to the current date and time.
X> - Update the `GotoView` to update the field when the page is clicked.
X>
X> Once you have completed these tasks, implement some tests.
X> 
X> - Add in a test to ensure that `last_visit` is not in the future.
X> - Add in a test to ensure that `last_visit` is updated when a page is requested.

T> ### Hints
T> You'll want to use the timezone-aware functionality of Django to get the current date and time. This requires you to import: `from django.utils import timezone`, with the current date and time accessible with `timezone.now()`.
T>
T> In order to compare two dates, you will need to make use of the `assertTrue()` method to perform the assertion. This takes a boolean expression, where you can perform your evaluation, such as `page.last_visit < timezone.now()`.
T>
T> When working on the second test, you'll need to make a call to the `rango:goto` view, passing the `page_id` as a parameter. You can do this with the `client.get()` method by providing a dictionary as the second argument with `page_id` as the key, and the ID of the page you are looking to access as the value. Depending upon how you implement this test, it may also require you to refresh a model instance from the database. This can be achieved using the `refresh_from_db()` method.
T>
T> As a final hint, it may also be helpful to write a further helper function to add a page to a given category. If you are stuck, we have implemented a [model solution on GitHub](https://github.com/maxwelld90/tango_with_django_2_code/tree/ba2cbed99316b667206eb3e43730463bf976001d).

I> ### Other Test Resources
I> - Run through [Part Five of the official Django Tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial05/) to learn more about testing.
I> - Check out the [tutorial on test-driven development by Harry Percival](https://www.obeythetestinggoat.com/book/part1.harry.html).
