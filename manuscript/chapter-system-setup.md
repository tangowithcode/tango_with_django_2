#Setting up your System {#chapter-system-setup}
This supplementary chapter provides additional setup guides that complement the [initial setup chapter](#chapter-getting-ready). We provide setup guides for installing and configuring the various technologies that you will be using within Tango with Django. Refer to the section that is relevant to you; you do not need to work through all of this chapter if things are already working for you.

I> ### Common Guides
I>
I> This chapter provides instructions on how to set up the various technologies that you'll be using throughout Tango with Django that we believe will work on the largest number of systems. However, every computer setup is different -- different versions of software, different operating systems, etc. These differences make providing universal setup guides very difficult to do.
I> 
I> If you are using this book as part of a course, you may be provided with setup instructions unique to your lab computers. Follow these instructions instead -- a majority of the setup work will likely be taken care of for you already.
I>
I> However, if you are working solo and you follow the instructions provided in this chapter without success, we recommend heading to your favourite search engine and entering the problem you're having. Typically, this will involve copying and pasting the error message you see at whatever step you're struggling at. By pasting in the message verbatim, chances are you'll find someone who suffered the same issue as you -- and from that point, you'll hopefully find a solution to resolve your problem.

## Installing Python 3 {#section-system-setup-python}
How do you go about installing Python 3.7 on your computer? This section answers that question. As we [discussed previously](#chapter-getting-ready-python3), you may find that you already have Python installed on your computer. If you are using a Linux distribution or macOS, you will definitely have it installed. Some of your operating system's functionality [is implemented in Python](http://en.wikipedia.org/wiki/Yellowdog_Updater,_Modified), hence the need for an interpreter! Unfortunately, nearly all modern operating systems that come preloaded with Python use a version that is much older than what we require. However, to keep your operating system functioning, we must install an updated Python version side-by-side with the old one.

There's many different ways in which you can install Python. We demonstrate here the most common approaches that you can use on Apple's macOS, various Linux distributions and Windows 10. Pick the section associated with your operating system to proceed. Note that we favour the use of [package managers](https://en.wikipedia.org/wiki/Package_manager) where appropriate to ensure that you have the means of maintaining and updating the software easily (when required).

### Apple macOS
The simplest way to acquire Python 3 for macOS is to download a `.dmg` image file from the [official Python website](https://www.python.org/downloads/mac-osx/). This will provide you with a step-by-step installation interface that makes setting everything up straightforward. If your development environment will be kept lightweight (i.e. Python only), this option makes sense. Simply download the installer, and Python 3 should then be available on your Mac's terminal!

However, [package managers make life easier](https://softwareengineering.stackexchange.com/questions/372444/why-prefer-a-package-manager-over-a-library-folder) when development steps up and involves a greater number of software tools. Installing a package manager makes it easy to maintain and update software on your computer -- and even to install new software, too. macOS does not come preinstalled with a package manager, so you need to download and install one yourself. If you want to go down this route, we'll introduce you to *MacPorts*, a superb package manager offering a [large host of tools](https://www.macports.org/ports.php) for you to download and use. We recommend that you follow this route. Although more complex, the end result will be a complete development environment, ready for you to get coding.

A prerequisite for using MacPorts is that you have Apple's *Xcode* environment installed. This download is several gigabytes in size. The easiest way to acquire this is through the App Store on your macOS installation. You'll need your Apple account to download that software. Once XCode has been installed, follow the following steps to setup MacPorts.

1. Verify that XCode is installed by launching it. You should see a welcome screen. If you see this, quit the app.
2. Open a Terminal window. Install the XCode command line tools by entering the command `$ xcode-select --install`. This will download additional software tools that will be required by XCode and additional development software that you later install.
3. Agree to the XCode license, if you have not already. You can do this by entering the command `$ xcode-build license`. Read the terms to the bottom of the page, and type `Y` to complete -- but only if you agree to the terms!
4. From [the MacPorts installation page](https://www.macports.org/install.php), download the MacPorts installer for your correct macOS version.
5. On your Mac's Finder, open the directory where you downloaded the installer to, and double-click the file to launch the installation process.
6. Follow the steps, and provide your password to install the software.
7. Once complete, delete the installer file -- you no longer require it. Close down any Terminal windows that are still open.

Once the MacPorts installation has been completed, installing Python is straightforward.

1. Open a new Terminal window. It is important that you launch a new window after MacPorts installation!
2. Enter the command `$ sudo port install python37`. After entering your password, this will take a few minutes. Several dependencies will be required -- agree to these being installed by responding with `Y`.
3. Once installation completes, activate your new Python installation. Enter the command `$ sudo port select --set python python37`.
4. Test that the command succeeds by issuing the command `$ python`. You should then see the interpreter for Python 3.7.2 (or whatever version you just installed).

Once this has been completed, Python has been successfully installed and is ready to use. You'll want to check later sections of this chapter referring to virtual environments and pip to ensure these are installed and setup correctly.

N> ### Installating Additional Software with MacPorts
N>
N> MacPorts provides an extensive, preconfigured library of open-source software suited specifically for development environments. When you need something new, it's a cinch to install. **For example,** you want to install the *LaTeX* typesetting system, search [the MacPorts ports list](https://www.macports.org/ports.php) -- the resultant package name being `texlive-latex`. This could then be installed with the command `$ sudo port install texlive-latex`. All software that LaTeX is dependent upon is also installed. This saves you significant amounts of time trying to find all the right bits of software to make things work.
N>
N> To view the packages MacPorts has already installed on your system, issue the command `$ port list installed`. You will see `python37` listed!

### Linux Distributions
There are many different ways in which you can download, install and run an updated version of Python on your Linux distribution. Methodologies unfortunately vary from distribution to distribution. This makes providing a sequence of instructions working across all distributions difficult. However, tools such as `pyenv` make installing different versions of Python across distributions much more straightforward.

We've worked out a series of steps that you can follow to download and install Python 3.7 on your Linux computer. These have been tested in Ubuntu; other distributions should also work with minor tweaks for the packages. A cursory search on your favorite search engine should reveal the correct command to enter. For example, on a *Red Hat Enterprise Linux* installation, the system package manager is `yum` instead of `apt`.

1. While `pyenv` makes it easy to install multiple versions of Python, you do need prerequisites to be present on your system for the Python installation to succeed. Issue the following command.
   
   {lang="bash",linenos=off}
   	apt install curl git build-essential libssl-dev libffi-dev python-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev

2. So do the next step.

<!-- 1. INSTALL PREREQS

1. If you're using a graphical environment, open a new Terminal window.
2. Issue `$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash` to download the `pyenv` installer, and start it.
3.
 -->

prereqs
	curl
	git
	apt install build-essential libssl-dev libffi-dev python-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev
	
	bz2
	readline libreadline-dev
	sqlite3 libsqlite3-dev

append to end of .bashrc file
	export PATH="~/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"

restart terminal

pyenv update

pyenv install 3.7.2


 
### Windows {#section-system-setup-python-windows}
By default, Microsoft Windows comes with no installation of Python. This means that you do not have to worry about leaving existing installations alone; installing from scratch should work just fine. You can download a 64-bit of 32-bit version of Python from [the official Python website](http://www.python.org/download/). If you aren't sure what one to download, you can determine if your computer is 32-bit or 64-bit by looking at the instructions provided [on the Microsoft website](https://support.microsoft.com/en-gb/help/13443/windows-which-operating-system).

1. Download the appropriate installer from the [official Python website](http://www.python.org/download/). At the time of writing, the latest release was version 3.7.2.
2. Run the installer. You'll want to make sure that you check the box saying that Python 3.7 is added to `PATH`. You'll want to install for all users, too. Choose the `Customize` option.
3. Proceed with the currently selected check boxes, and choose `Next`.
4. Make sure that the check box for installing Python for all users is checked. The installation location will change. Refer to [the figure below](#fig-ch4setup-pywin-3) for an example.
5. Click `Next` to install Python. You will need to give the installer elevated privileges to install the software.
6. Close the installer when completed, and delete the file you downloaded -- you no longer require it.

Once the installer is complete, you should have a working version of Python 3.7 installed and ready to go. Following the instructions above, Python 3.7 is installed to the directory `C:\Program Files\Python37`. If you checked all of the options correctly, the `PATH` environment variable used by Windows should also have been updated to incorporate the new installation of Python. To test this, launch a Command Prompt window and type `$ python`. Execute the command. You should see the Python interpreter launch, as demonstrated in [the screenshot below](#fig-ch4setup-pywin-4). If this fails, check your `PATH` environment variable is set correctly by following [an online guide](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

{id="fig-ch4setup-pywin-3"}
![Configuring Python 3.7.2 on Windows 10 x64 -- allowing the installation to be run by all users.](images/chsetup-pywin-3.png)

{id="fig-ch4setup-pywin-4"}
![Python on Windows 10 x64. Note the correct version of the Python interpreter, 3.7.2, is launched.](images/chsetup-pywin-4.png)

## The Python Package Manager {#section-system-setup-pip}

## Virtual Environments {#section-system-setup-virtualenv}


on Windows

pip install virtualenv
pip install virtualenvwrapper-win

then the commands should work fine.

## Git Version Control System
