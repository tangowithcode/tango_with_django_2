# Getting Ready to Tango
Before we get down to coding, it's really important that we get our development environment setup so that you can *Tango with Django!* You'll need to ensure that you have all the necessary components installed on your computer. This chapter outlines the five key components that you need to be aware of, setup and use. These are listed below.

* Working with the [terminal](https://en.wikipedia.org/wiki/Terminal_emulator) or [Command Prompt](https://en.wikipedia.org/wiki/Cmd.exe).
* *Python* and your *Python* installation.
* The Python Package Manager *pip* and *virtual environments*.
* Your *Integrated Development Environment (IDE)*, if you choose to use one.
* A *Version Control System (VCS)*, *Git*.

If you already have Python 2.7/3.4/3.5 and Django 1.9/1.10 installed on your computer, and are familiar with the technologies mentioned, then you can skip straight to the [Django Basics chapter](#chapter-django-basics). Otherwise, below we provide an overview of the different components and why they are important. We also provide a series of pointers on how to setup the various components.

I> ### Your Development Environment
I> Setting up your development environment is pretty tedious and often frustrating. It's not something that you'd do everyday. Below, we have put together the list of core technologies you need to get started and pointers on how to install them.
I>
I> From experience, we can also say that it's a good idea when setting your development environment up to note down the steps you took. You'll need them again one day - whether because you have purchased a new computer, or you have been asked to help someone else set their computer up! Taking a note of everything you do will save you time and effort in the future. Don't just think short term!

## Python
To work with Tango with Django, we require you to have installed on your computer a copy of the Python programming language. Any version from the `2.7` family - with a minimum of `2.7.5` - or version `3.4+` will work fine. If you're not sure how to install Python and would like some assistance, have a look at [the chapter dealing with installing Python](#section-system-setup-python).

I> ### Not sure how to use Python?
I> If you haven't used Python before - or you simply wish to brush up on your skills - then we highly recommend that you check out and work through one or more of the following guides:
I> 
I> * [**Learn Python in 10 Minutes**](http://www.korokithakis.net/tutorials/python/) by Stavros;
I> * [**The Official Python Tutorial**](http://docs.python.org/2/tutorial/);
I> * [**Think Python: How to Think like a Computer Scientist**](http://www.greenteapress.com/thinkpython/) by Allen B. Downey; or
I> * [**Learn to Program**](https://www.coursera.org/course/programming1) by Jennifer Campbell and Paul Gries.
I>
I> These will get you familiar with the basics of Python so you can start developing using Django. Note you don't need to be an expert in Python to work with Django. Python is awesome and you can pick it up as you go, if you already know another programming language.



## The Python Package Manager
Pip is the python [package manager](https://en.wikipedia.org/wiki/Package_manager). The package manager allows you install various libraries for the Python programming language to enhance its functionality.

A package manager, whether for Python, your [operating system](https://en.wikipedia.org/wiki/Advanced_Packaging_Tool) or [some other environment](https://docs.npmjs.com/cli/install), is a software tool that automates the process of installing, upgrading, configuring and removing *packages* - that is, a package of software which you can use on your computer. This is opposed to downloading, installing and maintaining software manually. Maintaining Python packages is pretty painful. Most packages often have *dependencies* so these need to be installed too. Then these packages may conflict or require particular versions which need to be resolved. Also, the system path to these packages needs to be specified and maintained. Luckily *pip* handles all this for you - so you can sit back and relax.

Try and run pip with the command `$ pip`. If the command is not found, you'll need to install pip itself - check out the [system setup chapter](#chapter-system-setup) for more information. You should also ensure that the following packages are installed on your system. Run the following commands to install Django and [pillow](https://pillow.readthedocs.io/en/5.0.0/) (an image manipulation library for Python).

{lang="bash",linenos=off}
	$ pip install -U django==1.9.10
	$ pip install pillow

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
I> 	pip install pillow --global-option="build_ext"
I> 	                   --global-option="--disable-jpeg"
I>
I> While you obviously will have a lack of support for handling JPEG images, Pillow should then install without problem. Getting Pillow installed is enough for you to get started with this tutorial. For further information, check out the [Pillow documentation](http://pillow.readthedocs.io/en/3.2.x/installation.html).


## Virtual Environments

We're almost all set to go! However, before we continue, it's worth pointing out that while this setup is fine to begin with, there are some drawbacks. What if you had another Python application that requires a different version to run, or you wanted to switch to the new version of Django, but still wanted to maintain your Django 1.9 project?

The solution to this is to use [virtual environments](http://simononsoftware.com/virtualenv-tutorial/). Virtual environments allow multiple installations of Python and their relevant packages to exist in harmony. This is the generally accepted approach to configuring a Python setup nowadays.

Setting up a virtual environment is not necessarily but it is highly recommended. The [virtual environment chapter](#chapter-virtual-environments) details how to setup, create and use virtual environments.


## Integrated Development Environment
While not absolutely necessary, a good Python-based IDE can be very helpful to you during the development process. Several exist, with perhaps [*PyCharm*](http://www.jetbrains.com/pycharm/) by JetBrains and *PyDev* (a plugin of the [Eclipse IDE](http://www.eclipse.org/downloads/)) standing out as popular choices. The [Python Wiki](http://wiki.python.org/moin/IntegratedDevelopmentEnvironments) provides an up-to-date list of Python IDEs.

Research which one is right for you, and be aware that some may require you to purchase a licence. Ideally, you'll want to select an IDE that supports integration with Django.

We use PyCharm as it supports virtual environments and Django integration - though you will have to configure the IDE accordingly. We don't cover that here - although JetBrains do provide a [guide on setting PyCharm up](https://www.jetbrains.com/help/pycharm/2016.1/creating-and-running-your-first-django-project.html).

## Code Repository
We should also point out that when you develop code, you should always house your code within a version-controlled repository such as [SVN](http://subversion.tigris.org/) or [Git](http://git-scm.com/). We won't be explaining this right now, so that we can get stuck into developing an application in Django. We have however written a [chapter providing a crash course on Git](#chapter-git) for your reference that you can refer to later on. **We highly recommend that you set up a Git repository for your own projects.**

X> ###Exercises
X> 
X> To get comfortable with your environment, try out the following exercises.
X> 
X>  - Install Python 2.7.5+/3.4+ and Pip.
X>  - Play around with your *command line interface (CLI)* and create a directory called `code`,  which we use to create our projects in.
X>  - Setup your Virtual Environment (optional)
X>  - Install the Django and Pillow packages
X>  - Setup an account on a Git Repository site like: GitHub, BitBucket, etc if you haven't already done so.
X>  - Download and setup an Integrated Development Environment like [PyCharm](https://www.jetbrains.com/pycharm/)
X> 
X>  As previously stated, we've made the code for the book and application available on our [GitHub repository](https://github.com/leifos/tango_with_django_19/).
X> 
X>  - If you spot any errors or problem, please let us know by making a change request on GitHub.
X>  - If you have any problems with the exercises, you can check out the repository to see how we completed them.

D> ### What is a Directory?
D> In the text above, we refer to creating a *directory*. But what exactly is a *directory*? If you have used a Windows computer up until now, you'll know a directory as a *folder*. The concept of a folder is analogous to a directory - it is a cataloguing structure that contains references to other files and directories.
