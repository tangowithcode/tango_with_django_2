from datetime import datetime
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.shortcuts import redirect

from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from rango.bing_search import run_query, read_bing_key
from rango.models import UserProfile
from django.contrib.auth.models import User


def index(request):
    # return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    #request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!",
                    'categories': category_list,
                    'pages': page_list,
                    }

    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context_dict)


    # Return response back to the user, updating any cookies that need changed.
    return response



class AboutView(View):
    def get(self, request):
        # <view logic>
        visitor_cookie_handler(request)
        return render(request, 'rango/about.html', context={'visits': request.session['visits']})
        

def about(request):
    #if request.session.test_cookie_worked():
    #    print("TEST COOKIE WORKED!")
    #    request.session.delete_test_cookie()

    visitor_cookie_handler(request)
    return render(request, 'rango/about.html', context={'visits': request.session['visits']})


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        #pages = Page.objects.filter(category=category)
        pages = Page.objects.filter(category=category).order_by('-views')

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
        
    # New code added here to handle a POST request
    
    # create a default query based on the category name
    # to be shown in the search box
    context_dict['query'] = category.name
    
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        
        if query:
            # Run our search API function to get the results list!
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list
            
    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)



class AddCategoryView(View):
    
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})
        
    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm()
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
        return render(request, 'rango/add_category.html', {'form': form})   
            
@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

'''
def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            #return HttpResponse("Invalid login details supplied.")
            return render(request, 'rango/login.html', {'error_message':'Invalid username and/or password entered. Try again'})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))

'''

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler_client_side(request, response):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.COOKIES.get('visits', '1'))

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        # Set the last visit cookie
        response.set_cookie('last_visit', last_visit_cookie)

    # Update/set the visits cookie
    response.set_cookie('visits', visits)


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits
    
    
def search(request):
    result_list = []
    
    query = None
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
            
    return render(request, 'rango/search.html', {'result_list': result_list, 'query':query})



def goto_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
                
    return redirect(url)
    
    
@login_required
def register_profile(request):
    form = UserProfileForm()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            
            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form':form}
    
    return render(request, 'rango/profile_registration.html', context_dict)
    
    
    
@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture})
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    
    return render(request, 'rango/profile.html',
        {'userprofile': userprofile, 'selecteduser': user, 'form': form})
        
            
            
class ProfileView(View):
    
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('index')
            
        userprofile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})
        return (user, userprofile, form)
    
    @method_decorator(login_required)
    def get(self, request,  username):
        (user, userprofile, form) = self.get_user_details(username)
        return render(request, 'rango/profile.html',
            {'userprofile': userprofile, 'selecteduser': user, 'form': form})
        
    @method_decorator(login_required)
    def post(self, request,  username):
        (user, userprofile, form) = self.get_user_details(username)
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
        return render(request, 'rango/profile.html',
            {'userprofile': userprofile, 'selecteduser': user, 'form': form})
            
            
@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    
    return render(request, 'rango/list_profiles.html',
        {'userprofile_list' : userprofile_list})
        
@login_required
def like_category(request):
    print("in cat")
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()
    return HttpResponse(likes)
    
    
def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if len(starts_with.strip())>0:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list
    
    
def suggest_category(request):
    cat_list = []
    starts_with = ''
    
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        
    cat_list = get_category_list(8, starts_with)
    if len(cat_list) == 0:
        cat_list = Category.objects.order_by('-likes')
    
    return render(request, 'rango/cats.html', {'cats': cat_list })
    
    
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, 
                title=title, url=url)
            pages = Page.objects.filter(category=category).order_by('-views')
            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages
    return render(request, 'rango/page_list.html', context_dict)
