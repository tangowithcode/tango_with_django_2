#Setting up your System {#chapter-system-setup}
This supplementary chapter provides additional setup guides that complement the [initial setup chapter](#chapter-getting-ready). We provide setup guides for installing and configuring the various technologies that you will be using within Tango with Django. Refer to the section that is relevant to you; you do not need to work through all of this chapter if things are already working for you.

I> ## Common Guides
I>
I> This chapter provides instructions on how to set up the various technologies that you'll be using throughout Tango with Django that we believe will work on the largest number of systems. However, every computer setup is different -- different versions of software, different operating systems, etc. These differences make providing universal setup guides very difficult to do.
I> 
I> If you are using this book as part of a course, you may be provided with setup instructions unique to your lab computers. Follow these instructions instead -- a majority of the setup work will likely be taken care of for you already.
I>
I> However, if you are working solo and you follow the instructions provided in this chapter without success, we recommend heading to your favourite search engine and entering the problem you're having. Typically, this will involve copying and pasting the error message you see at whatever step you're struggling at. By pasting in the message verbatim, chances are you'll find someone who suffered the same issue as you -- and from that point, you'll hopefully find a solution to resolve your problem.

## Installing Python 3 {#section-system-setup-python}
How do you go about installing Python 3.7 on your computer? This section answers that question. As we [discussed previously](#chapter-getting-ready-python3), you may find that you already have Python installed on your computer. If you are using a Linux distribution or macOS, you will definitely have it installed. Some of your operating system's functionality [is implemented in Python](http://en.wikipedia.org/wiki/Yellowdog_Updater,_Modified), hence the need for an interpreter! Unfortunately, nearly all modern operating systems that come preloaded with Python use a version that is much older than what we require. However, to keep your operating system functioning, we must install an updated Python version side-by-side with the old one.

There's many different ways in which you can install Python. We demonstrate here the most common approaches that you can use. Pick the section for your operating system to proceed. Note that we favour the use of [package managers](https://en.wikipedia.org/wiki/Package_manager) where appropriate to ensure that you have the means of maintaining and updating the software easily (when required).

### Windows {#section-system-setup-python-windows}
By default, Microsoft Windows comes with no installation of Python. This means that you do not have to worry about leaving existing installations alone; installing from scratch should work just fine. You can download a 64-bit of 32-bit version of Python from [the official Python website](http://www.python.org/download/). If you aren't sure what one to download, you can determine if your computer is 32-bit or 64-bit by looking at the instructions provided [on the Microsoft website](https://support.microsoft.com/en-gb/help/13443/windows-which-operating-system).

1. Download the appropriate installer from the [official Python website](http://www.python.org/download/). At the time of writing, the latest release was version 3.7.2.
2. Run the installer. You'll want to make sure that you check the box saying that Python 3.7 is added to `PATH`. You'll want to install for all users, too. Choose the `Customize` option.
3. Proceed with the currently selected check boxes, and choose `Next`.
4. Make sure that the check box for installing Python for all users is checked. The installation location will change. Refer to [the figure below](#fig-ch4setup-pywin-3) for an example.
5. Click `Next` to install Python. You will need to give the installer elevated privileges to install the software.
6. Close the installer when completed, and delete the file you downloaded -- you no longer require it.

{id="fig-ch4setup-pywin-3"}
![Configuring Python 3.7.2 on Windows 10 x64 -- allowing the installation to be run by all users.](images/chsetup-pywin-3.png)

Once the installer is complete, you should have a working version of Python 3.7 installed and ready to go. Following the instructions above, Python 3.7 is installed to the directory `C:\Program Files\Python37`. If you checked all of the options correctly, the `PATH` environment variable used by Windows should also have been updated to incorporate the new installation of Python. To test this, launch a Command Prompt window and type `python`. Execute the command. You should see the Python interpreter launch, as demonstrated in [the screenshot below](#fig-ch4setup-pywin-4).

{id="fig-ch4setup-pywin-4"}
![A successful Python installation on Windows 10 x64. Note the correct version of the Python interpreter, 3.7.2, is launched.](images/chsetup-pywin-4.png)
