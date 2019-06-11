from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders

# Thanks to Enzo Roiz https://github.com/enzoroiz who made these tests during an internship with us - you are legend


class GeneralTests(TestCase):
    def test_serving_static_files(self):
        # If using static media properly result is not NONE once it finds rango.jpg
        result = finders.find('images/rango.jpg')
        self.assertIsNotNone(result)


class IndexPageTests(TestCase):

    def test_index_contains_hello_message(self):
        # Check if there is the message 'Rango Says'
        # Chapter 4
        response = self.client.get(reverse('index'))
        self.assertIn(b'Rango says', response.content)

    def test_index_using_template(self):
        # Check the template used to render index page
        # Chapter 4
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_rango_picture_displayed(self):
        # Check if is there an image called 'rango.jpg' on the index page
        # Chapter 4
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'rango.jpg', response.content)

    def test_index_has_title(self):
        # Check to make sure that the title tag has been used
        # And that the template contains the HTML from Chapter 4
        response = self.client.get(reverse('index'))
        self.assertIn(b'<title>', response.content)
        self.assertIn(b'</title>', response.content)


class AboutPageTests(TestCase):

    def test_about_contains_create_message(self):
        # Check if in the about page is there - and contains the specified message
        # Exercise from Chapter 4
        response = self.client.get(reverse('rango:about'))
        self.assertIn(b'This tutorial has been put together by', response.content)

    def test_about_contain_image(self):
        # Check if is there an image on the about page
        # Chapter 4
        response = self.client.get(reverse('rango:about'))
        self.assertIn(b'img src="/media/', response.content)

    def test_about_using_template(self):
        # Check the template used to render index page
        # Exercise from Chapter 4
        response = self.client.get(reverse('rango:about'))

        self.assertTemplateUsed(response, 'rango/about.html')


class ModelTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')

    def get_category(self, name):

        from rango.models import Category
        try:
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:
            cat = None
        return cat

    def test_python_cat_added(self):
        cat = self.get_category('Python')
        self.assertIsNotNone(cat)

    def test_python_cat_with_views(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.views, 128)

    def test_python_cat_with_likes(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)


class Chapter4ViewTests(TestCase):
    def test_index_contains_hello_message(self):
        # Check if there is the message 'hello world!'
        response = self.client.get(reverse('rango:index'))
        self.assertIn( b'Rango says', response.content)

    def test_does_index_contain_img(self):
        # Check if the index page contains an img
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'img',response.content)

    def test_about_using_template(self):
        # Check the template used to render index page
        # Exercise from Chapter 4
        response = self.client.get(reverse('rango:about'))
        self.assertTemplateUsed(response, 'rango/about.html')

    def test_does_about_contain_img(self):
        # Check if in the about page contains an image
        response = self.client.get(reverse('rango:about'))
        self.assertIn(b'img',response.content)

    def test_about_contains_create_message(self):
        # Check if in the about page contains the message from the exercise
        response = self.client.get(reverse('rango:about'))
        self.assertIn(b'This tutorial has been put together by', response.content)


class Chapter5ViewTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')

    def get_category(self, name):

        from rango.models import Category
        try:
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:
            cat = None
        return cat

    def test_python_cat_added(self):
        cat = self.get_category('Python')
        self.assertIsNotNone(cat)

    def test_python_cat_with_views(self):
        cat = self.get_category('Python')

        self.assertEquals(cat.views, 128)

    def test_python_cat_with_likes(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)

    def test_view_has_title(self):
        response = self.client.get(reverse('index'))

        # Check title used correctly
        self.assertIn(b'<title>', response.content)
        self.assertIn(b'</title>', response.content)

    # Need to add tests to:
    # check admin interface - is it configured and set up

    def test_admin_interface_page_view(self):
        from rango.admin import PageAdmin
        self.assertIn('category', PageAdmin.list_display)
        self.assertIn('url', PageAdmin.list_display)


class Chapter6ViewTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')

    # test the slug field works..
    def test_does_slug_field_work(self):
        from rango.models import Category
        cat = Category(name='how do i create a slug in django')
        cat.save()
        self.assertEqual(cat.slug, 'how-do-i-create-a-slug-in-django')

    # test does index page contain top five pages?
    def test_index_view_has_top_five_pages(self):
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'How to Tango with Django', response.content)
        self.assertIn(b'Official Django Tutorial', response.content)
        self.assertIn(b'Learn Python in 10 Minutes', response.content)
        self.assertIn(b'Flask', response.content)
        self.assertIn(b'How to Think like a Computer Scientist', response.content)

    # test does index page contain the words "most liked" and "most viewed"
    def test_index_view_has_most_liked(self):
        response = self.client.get(reverse('rango:index'))
        self.assertIn(b'Most Liked', response.content)
        self.assertIn(b'Most Viewed', response.content)

    # test does category page contain a link back to index page?
    def test_category_view_has_back_link(self):
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertIn(b'/rango/', response.content)
