# Getting Ready to Tango {#chapter-getting-ready}
Before we start coding, it's really important that we set your development environment up correctly so that you can *Tango with Django* with ease. You'll need to make sure that you have all of the necessary components installed on your computer, and that they are configured correctly. This chapter outlines the six key components you'll need to be aware of, setup and use. These are:

* the [terminal](https://en.wikipedia.org/wiki/Terminal_emulator) (on macOS or UNIX/Linux systems), or the [Command Prompt](https://en.wikipedia.org/wiki/Cmd.exe) (on Windows);
* *Python 3*, including how to code and run Python scripts;
* the Python Package Manager *pip*;
* *Virtual Environments*;
* your *Integrated Development Environment (IDE)*, if you choose to use one; and
* a *Version Control System (VCS)* called *Git*.

If you already have Python 3 and Django 2 installed on your computer and are familiar with the technologies listed above, you can skip straight ahead to the [Django Basics chapter](#chapter-django-basics). If you are not familiar with some or all of the technologies listed, we provide an overview of each below. These go hand in hand with later [supplementary chapter](#chapter-system-setup) that provides a series of pointers on how to set the different components up, if you need help doing so.

I> ### You Development Environment is Important!
I> Setting up your development environment can be a tedious and frustrating process. It's not something that you would do every day. The pointers we provide in this chapter (and the [additional supplementary chapter](#chapter-system-setup)) should help you in getting everything to a working state. The effort you expend now in making sure everything works will ensure that development can proceed unhindered.
I>
I> From experience, we can also say with confidence that as you set your environment up, it's a good idea to note down the steps that you took. You will probably need that workflow again one day -- maybe you will purchase a new computer, or be asked to help a friend set their environment up, too. *Don't think short-term, think long-term!*

## Python 3 {#chapter-getting-ready-python3}
To work with Tango with Django, we require you to have installed on your computer a copy of the *Python 3* programming language. A Python version of 3.5 or greater should work fine with Django 2.0, 2.1 and 2.2 -- although the official Django website recommends that you have the most recent version of Python installed. As such, we recommend you install *Python 3.7*. At the time of writing, the most recent release is *Python 3.7.2.* If you're not sure how to install Python and would like some assistance, have a look at [our quick guide on how to install Python](#section-system-setup-python).

W> ### Running macOS, Linux or UNIX?
W> On installations of macOS, Linux or UNIX, you will find that Python is already installed on your computer -- albeit a much older version, typically 2.x. This version is required by your operating system to perform essential tasks such as downloading and installing updates. While you can use this version, it won't be compatible with Django 2, and you'll need to install a newer version of Python to run *side-by-side* with the old installation. *Do not uninstall or hack away at deleting Python 2.x* if it is already present on your system; you may break your operating system!

I> ## Django 2.0, 2.1 or 2.2?
I> In this book, we explicitly use Django version `2.1.5`. However, we have also tested the instructions provided with versions `2.0.13`, `2.1.10`, and `2.2.3`. Therefore, you will be able to use version 2.2 if you wish! If you do use a different version, substitute `2.1.5` with the version you are using.
I>
I> We'll be regularly checking the compatibility of the instructions provided with future Django releases. If you notice any issues with later versions, feel free to get in touch with us. You can [send us a tweet](https://twitter.com/tangowithdjango), [raise an issue on GitHub](https://github.com/leifos/tango_with_django_2/issues), or e-mail us -- our addresses are available on the [www.tangowithdjango.com](https://www.tangowithdjango.com) website.
I>
I> You must however make sure you are using *at least* Python version 3.5. Version 3.4 and below are incompatible with these releases of Django.

I> ## Python Skills Rusty?
I> If you haven't used Python before -- or you simply want to brush up on your skills -- then we highly recommend that you check out and work through one or more of the following guides:
I>
I> * [**The Official Python Tutorial**](https://docs.python.org/3/tutorial/);
I> * [**Think Python: How to Think like a Computer Scientist**](https://greenteapress.com/wp/think-python-2e/) by Allen B. Downey; or
I> * [**Learn Python in 10 Minutes**](https://www.stavros.io/tutorials/python/) by Stavros;
I> * [**Learn to Program**](https://www.coursera.org/course/programming1) by Jennifer Campbell and Paul Gries.
I>
I> These guides will help you familiarise yourself with the basics of Python so you can start developing with Django. Note you don't need to be an expert in Python to work with Django -- Python is straightforward to use, and you can pick it up as you go, especially if you already know the ins and outs of at least one other programming language.

## Virtual Environments {#chapter-getting-ready-venv}
With a working installation of Python 3 (and the basic programming skills to go with it), we can now setup our environment for the Django project (called Rango) we'll be creating in this tutorial. One super useful tool we *strongly* encourage you to use is a virtual environment. Although not strictly necessary, it provides a useful separation between your computer's Python installation and the environment you'll be using to develop Rango with.

A virtual environment allows for multiple installations of Python packages to exist in harmony, within unique *Python environments*. Why is this useful? Say you have a project, `projectA` that you want to run in Django 1.11, and a further project, `projectB` written for Django 2.1. This presents a problem as you would normally only be able to install one version of the required software at a time. By creating virtual environments for each project, you can then install the respective versions of Django (and any other required Python software) within each unique environment. This ensures that the software installed in one environment does not tamper with the software installed on another.

You'll want to create a virtual environment using Python 3 for your Rango development environment. Call the environment `rangoenv`. If you are unsure as to how to do this, go to the supplementary chapter detailing [how to set up virtual environments before continuing](#section-system-setup-virtualenv). If you do choose to use a virtual environment, remember to activate the virtual environment by issuing the following command.

{lang="bash",linenos=off}
	$ workon rangoenv

From then on, all of your prompts with the terminal or Command Prompt will precede with the name of your virtual environment to remind you that it is switched on. Check out the following example to know what we are discussing.

{lang="bash",linenos=off}
	$ workon rangoenv
	(rangoenv) $ pip install django==2.1.5
	...
	(rangoenv) $ deactivate
	$ 

The penultimate line of the example above demonstrates how to switch your virtual environment off after you have finished with it -- note the lack of `(rangoenv)` before the prompt. Again, [refer to the system setup chapter in the appendices of this book](#section-system-setup-virtualenv) for more information on how to setup and use virtual environments.

## The Python Package Manager
Going hand in hand with virtual environments, we'll also be making use of the Python package manager, *pip*, to install several different Python software packages -- including Django -- to our development environment. Specifically, we'll need to install two packages: Django 2 and *Pillow*. Pillow is a Python package providing support for handling image files (e.g. `.jpg` and `.png` files), something we'll be doing later in this tutorial.

A package manager, whether for Python, your [operating system](https://en.wikipedia.org/wiki/Advanced_Packaging_Tool) or [some other environment](https://docs.npmjs.com/cli/install), is a software tool that automates the process of installing, upgrading, configuring and removing *packages* -- that is, a package of software which you can use on your computer that provides some functionality. This is opposed to downloading, installing and maintaining software manually. Maintaining Python packages is pretty painful. Most packages often have *dependencies* -- additional packages that are required for your package to work! This can get very complex very quickly. A package manager handles all of this for you, along with issues such as conflicts regarding different versions of a package. Luckily, *pip* handles all this for you.

Try and run the command `$ pip` to execute the package manager. Make sure you do this with your virtual environment `acivate`d. Globally, you may have to use the command `pip3`. If these don't work, you have a setup issue -- refer to our [`pip` setup guide](#section-system-setup-pip) for help.

With your virtual environment switched on, execute the following two commands to install Django and Pillow.

{lang="bash",linenos=off}
	$ pip install django==2.1.5
	$ pip install pillow==5.4.1

Installing these two packages will be sufficient to get you started. As you work through the tutorial, there will be a couple more packages that we will require. We'll tell you to install them as we require them. For now, you're good to go.

I> ### Problems Installing `pillow`?
I> When installing Pillow, you may receive an error stating that the installation failed due to a lack of JPEG support.
I> This error is shown as the following:
I> 
I> {lang="text",linenos=off}
I> 	ValueError: jpeg is required unless explicitly disabled using
I> 	            --disable-jpeg, aborting
I>
I> If you receive this error, try installing Pillow *without* JPEG support enabled, with the following command.
I>
I> {lang="text",linenos=off}
I> 	pip install pillow==5.4.1 --global-option="build_ext"
I> 	                          --global-option="--disable-jpeg"
I>
I> While you obviously will have a lack of support for handling JPEG images, Pillow should then install without problem. Getting Pillow installed is enough for you to get started with this tutorial. For further information, check out the [Pillow documentation](https://pillow.readthedocs.io/en/stable/installation.html).

T> ### Working within in a Virtual Environment
T> Substitute `pip3` with `pip` when working within your virtual environment. The command `pip` is aliased to the correct one for your virtual environment.

## Integrated Development Environment
While not necessary, a good Python-based IDE can be very helpful to you during the development process. Several exist, with perhaps [*PyCharm*](http://www.jetbrains.com/pycharm/) by JetBrains and *PyDev* (a plugin of the [Eclipse IDE](http://www.eclipse.org/downloads/)) standing out as popular choices. The [Python Wiki](http://wiki.python.org/moin/IntegratedDevelopmentEnvironments) provides an up-to-date list of Python IDEs.

Research which one is right for you, and be aware that some may require you to purchase a licence. Ideally, you'll want to select an IDE that supports integration with Django. Of course, if you prefer not to use an IDE, using a simple text editor like [Sublime Text](https://www.sublimetext.com/), [TextMate](https://macromates.com/) or [Atom](https://atom.io/) will do just fine. Many modern text editors support Python syntax highlighting, which makes things much easier!

We use PyCharm as it supports virtual environments and Django integration -- though you will have to configure the IDE accordingly. We don't cover that here -- although JetBrains does provide a [guide on setting PyCharm up](https://www.jetbrains.com/help/pycharm/2016.1/creating-and-running-your-first-django-project.html).

## Version Control
We should also point out that when you develop code, you should always house your code within a version-controlled repository such as [SVN](http://subversion.tigris.org/) or [Git](http://git-scm.com/). We won't be explaining this right now so that we can get stuck into developing an application in Django. We have however written a [chapter providing a crash course on Git](#chapter-git) for your reference that you can refer to later on. **We highly recommend that you set up a Git repository for your projects.**

X> ### Exercises
X> To get comfortable with your environment, try out the following exercises.
X>
X> - Get up to speed with Python if you're new to the language. Try out one or more of the tutorials we listed earlier.
X> - Install Python 3.7. Make sure `pip3` (or `pip` within your virtual environment) is also installed and works on your computer.
X> - Play around with your *command line interface (CLI)*, whether it be the Command Prompt (Windows) or a terminal (macOS, Linux, UNIX, etc.).
X> - Create a new virtual environment using Python 3.7. This is optional, but we *strongly encourage you to use virtual environments.*
X> - Within your environment, install Django 2 and Pillow 5.4.1.
X> - Set up an account on a Git repository site like [GitHub](https://github.com/) or [BitBucket](https://bitbucket.org/) if you haven't already done so.
X> - Download and set up an IDE like [PyCharm](https://www.jetbrains.com/pycharm/), or set up your favourite text editor for working with Python files.
X>
X> As previously stated, we've made the code for the application available on our [GitHub repository](https://github.com/maxwelld90/tango_with_django_2_code).
X>
X> - If you spot any errors or problems, please let us know by making an [issue on GitHub](https://github.com/leifos/tango_with_django_2/issues).
X> - If you have any problems with the exercises, you can check out the repository to see how we completed them.

## Testing your Implementation {#section-getting-ready-tests}
As you work through your implementation of the requirements for the Rango app, we want you to have the confidence to know that *what you are coding up is correct.* We can't physically sit next to you, so we've gone and done the next best thing -- **we've implemented a series of different tests that you can run against your codebase to see what's correct, and what can be improved**.

These are available from our sample codebase repository, [available on GitHub](https://github.com/maxwelld90/tango_with_django_2_code/tree/master/progress_tests). The `progress_tests` directory on this repository contains a number of different Python modules, each containing a series of different test modules you can run against your Rango implementation. Note that they are for individual chapters -- for example, you should run the module `tests_chapter3.py` against your implementation *after* completion of Chapter 3, but before starting Chapter 4. Note that not every chapter will have tests at the end of it.

W> ### Complete the Exercises!
W> These tests assume that you complete all of the exercises for a chapter! If you don't do this, it's likely some tests will not pass.

We check the basic functionality that should be working up to the point you are testing at. We also check what is returned from the server when a particular URL is accessed -- and if the response doesn't match *exactly* what we requested in the book, *the test will fail.* This might seem overly harsh, but we want to drill into your head that *you must satisfy requirements exactly as they are laid out -- no deviation is acceptable.* This also drills into your head the idea of *test-driven development,* something that we outline [at the start of the testing chapter](#chapter-testing).

How do you run the tests, though? This step-by-step process demonstrates the basic process on what you have to do. We will assume that you want to run the tests for [Chapter 3, Django Basics](#chapter-django-basics).

1. First, identify what chapter's tests you want to run.
2. Either make a clone of our [sample code repository](https://github.com/maxwelld90/tango_with_django_2_code) on your computer, or access the individual test module that you want from the [GitHub web interface](https://github.com/maxwelld90/tango_with_django_2_code/tree/master/progress_tests).
    * To do the latter, click the module you require (i.e. `tests_chapter3.py`). When you see the code on the GitHub website, click the `Raw` button and save the page that then loads.
3. Move the `tests_chapter3.py` module to your project's `rango` directory. This step does not make sense right now; as you progress through the book and come back here to refresh your memory on what to do, this will make sense.
4. Run the command `$ python manage.py test rango.tests_chapter3`. This will start the tests.

You will also need to ensure that when these tests run, your `rangoenv` virtual environment is active.

Once the tests all complete, you should see `OK`. This means they all passed! If you don't see `OK`, something failed -- look through the output of the tests to see what test failed, and why. Sometimes, you might have missed something which causes an exception to be raised before the test can be carried out. In instances like this, you'll need to look at what is expected, and go back and fill it in. You can tweak your code and re-run the tests to see if they then pass.

X> ### Test your Implementation
X> When you have completed enough of the book to reach another round of tests, we'll denote the prompt for you to do this like so. We'll tell you what module to run, and always point you back to here so you can refresh your memory if you forget how to run them.

T> ### Delete when Complete!
T> When you have finished with the tests for a particular chapter, we **highly recommend** that you delete the module that you moved over to your `rango` directory. In the example above, we'd be looking to delete `tests_chapter3.py`. Once you have confirmed your solution passes the tests we provide, there's no need for the module anymore. Just delete it -- don't clutter your repository up with these modules!