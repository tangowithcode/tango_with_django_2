# A Crash Course in UNIX-based Commands {#chapter-unix}
Depending on your computing background, you may or may not have encountered a UNIX based system, or a derivative of. This small crash course focuses on getting you up to speed with the *terminal*, an application in which you issue commands for the computer to execute. This differs from a point-and-click *Graphical User Interface (GUI)*, the kind of interface that has made computing so much more accessible. A terminal based interface may be more complex to use, but the benefits of using such an interface include getting things done quicker, and more accurately, too.

I> ### Not for Windows!
I> Note that we're focusing on the Bash shell, a shell for UNIX-based operating systems and their derivatives, including OS X and Linux distributions. If you're a Windows user, you can use the [Windows Command Prompt](http://www.ai.uga.edu/mc/winforunix.html) or [Windows PowerShell](https://msdn.microsoft.com/en-us/powershell/mt173057.aspx). Users of Windows 10 with the [2016 Anniversary Update](https://blogs.windows.com/windowsexperience/2016/08/02/how-to-get-the-windows-10-anniversary-update/) will [also be able to issue Bash commands directly to the Command Prompt](http://www.pcworld.com/article/3050473/windows/heres-how-windows-10s-ubuntu-based-bash-shell-will-actually-work.html). You could also experiment by [installing Cygwin](https://www.cygwin.com/) to bring Bash commands to Windows.

## Using the Terminal
UNIX based operating systems and derivatives - such as OS X and Linux distributions - all use a similar looking terminal application, typically using the [Bash shell](https://en.wikipedia.org/wiki/Bash_(Unix_shell)). All possess a core set of commands that allow you to navigate through your computer's filesystem and launch programs - all without the need for any graphical interface.

Upon launching a new terminal instance, you'll be typically presented with something resembling the following.

{lang="text",linenos=off}
    sibu:~ david$

What you see is the *prompt*, and indicates when the system is waiting to execute your every command. The prompt you see varies depending on the operating system you are using, but all look generally very similar. In the example above, there are three key pieces of information to observe:

* your username and computer name (username of `david` and computer name of `sibu`);
* your *present working directory* (the tilde, or `~`); and
* the privilege of your user account (the dollar sign, or `$`).

D> ### What is a Directory?
D> In the text above, we refer to your present working directory. But what exactly is a *directory*? If you have used a Windows computer up until now, you'll probably know a directory as a *folder*. The concept of a folder is analogous to a directory - it is a cataloguing structure that contains references to other files and directories.

The dollar sign (`$`) typically indicates that the user is a standard user account. Conversely, a hash symbol (`#`) may be used to signify the user logged in has [root privileges](http://en.wikipedia.org/wiki/Superuser). Whatever symbol is present is used to signify that the computer is awaiting your input.

I> ### Prompts can Differ
I> The information presented by the prompt on your computer may differ from the example shown above. For example, some prompts may display the current date and time, or any other information. It all depends how your computer is set up.

When you are using the terminal, it is important to know where you are in the file system. To find out where you are, you can issue the command `pwd`. This will display your *Present Working Directory* (hence `pwd`). For example, check the example terminal interactions below.

{lang="text",linenos=off}
    Last login: Wed Mar 23 15:01:39 2016
    sibu:~ david$ pwd
    /users/grad/david
    sibu:~ david$

You can see that the present working directory in this example is `/users/grad/david`.

You'll also note that the prompt indicates that the present working directory is a tilde `~`. The tilde is used a special symbol which represents your *home directory*. The base directory in any UNIX based file system is the *root directory*. The path of the root directory is denoted by a single forward slash (`/`). As folders (or directories) are separated in UNIX paths with a `/`, a single `/` denotes the root!

If you are not in your home directory, you can *Change Directory* (`cd`) by issuing the following command:

{lang="text",linenos=off}
    sibu:/ david$ cd ~
    sibu:~ david$

Note how the present working directory switches from `/` to `~` upon issuing the `cd ~` command.

I> ### Path Shortcuts
I> UNIX shells have a number of different shorthand ways for you to move around your computer's filesystem. You've already seen that a forward slash (`/`) represents the [root directory](https://en.wikipedia.org/wiki/Root_directory), and the tilde (`~`) represents your home directory in which you store all your personal files. However, there are a few more special characters you can use to move around your filesystem in conjunction with the `cd` command.
I>
I> * Issuing `cd ~` will always return you to your home directory. On some UNIX or UNIX derivatives, simply issuing `cd` will return you to your home directory, too.
I> * Issuing `cd ..` will move your present working directory **up one level** of the filesystem hierarchy. For example, if you are currently in `/users/grad/david/code/`, issuing `cd ..` will move you to `/users/grad/david/`.
I> * Issuing `cd -` will move you to the **previous directory you were working in**. Your shell remembers where you were, so if you were in `/var/tmp/` and moved to `/users/grad/david/`, issuing `cd -` will move you straight back to `/var/tmp/`. This command obviously only works if you've move around at least once in a given terminal session.

Now, let's create a directory within the home directory called `code`. To do this, you can use the *Make Directory* command, called `mkdir`.

{lang="text",linenos=off}
    sibu:~ david$ mkdir code
    sibu:~ david$

There's no confirmation that the command succeeded. We can change the present working directory with the `cd` command to change to `code`. If this succeeds, we will know the directory has been successfully created.

{lang="text",linenos=off}
    sibu:~ david$ cd code
    sibu:code david$

Issuing a subsequent `pwd` command to confirm our present working directory yields `/users/grad/david/code` - our home directory, with `code` appended to the end. You can also see from the prompt in the example above that the present working directory changes from `~` to `code`.

X> ### Change Back
X> Now issue the command to change back to your home directory. What command do you enter?

From your home directory, let's now try out another command to see what files and directories exist. This new command is called `ls`, shorthand for *list*. Issuing `ls` in your home directory will yield something similar to the following.

{lang="text",linenos=off}
    sibu:~ david$ ls
    code

This shows us that there's something present our home directory called `code`, as we would expect. We can obtain more detailed information by adding a `l` switch to the end of the `ls` command - with `l` standing for *list*.

{lang="text",linenos=off}
    sibu:~ david$ ls -l
    drwxr-xr-x  2 david  grad  68  2 Apr 11:07 code

This provides us with additional information, such as the modification date (`2 Apr 11:07`), whom the file belongs to (user `david` of group `grad`), the size of the entry (`68` bytes), and the file permissions (`drwxr-xr-x`). While we don't go into file permissions here, the key thing to note is the `d` at the start of the string that denotes the entry is a directory. If we then add some files to our home directory and reissue the `ls -l` command, we then can observe differences in the way files are displayed as opposed to directories.

{lang="text",linenos=off}
    sibu:~ david$ ls -l
    drwxr-xr-x  2 david  grad      68  2 Apr 11:07 code
    -rw-r--r--@ 1 david  grad  303844  1 Apr 16:16 document.pdf
    -rw-r--r--  1 david  grad      14  2 Apr 11:14 readme.md

One final useful switch to the `ls` command is the `a` switch, which displays *all* files and directories. This is useful because some directories and files can be *hidden* by the operating system to keep things looking tidy. Issuing the command yields more files and directories!

{lang="text",linenos=off}
    sibu:~ david$ ls -la
    -rw-r--r--   1  david  grad     463 20 Feb 19:58 .profile
    drwxr-xr-x   16 david  grad     544 25 Mar 11:39 .virtualenvs
    drwxr-xr-x   2  david  grad      68  2 Apr 11:07 code
    -rw-r--r--@  1  david  grad  303844  1 Apr 16:16 document.pdf
    -rw-r--r--   1  david  grad      14  2 Apr 11:14 readme.md

This command shows a hidden directory `.virtualenvs` and a hidden file `.profile`. Note that hidden files on a UNIX based computer (or derivative) start with a period (`.`). There's no special `hidden` file attribute you can apply, unlike on Windows computers.

D> ### Combining `ls` Switches
D> You may have noticed that we combined the `l` and `a` switches in the above `ls` example to force the command to output a list displaying all hidden files. This is a valid command - and there are [even more switches you can use](http://man7.org/linux/man-pages/man1/ls.1.html) to customise the output of `ls`.

Creating files is also easy to do, straight from the terminal. The `touch` command creates a new, blank file. If we wish to create a file called `new.txt`, issue `touch new.txt`. If we then list our directory, we then see the file added.

{lang="text",linenos=off}
    sibu:~ david$ ls -l
    drwxr-xr-x  2 david  grad      68  2 Apr 11:07 code
    -rw-r--r--@ 1 david  grad  303844  1 Apr 16:16 document.pdf
    -rw-r--r--  1 david  grad       0  2 Apr 11:35 new.txt
    -rw-r--r--  1 david  grad      14  2 Apr 11:14 readme.md

Note the filesize of `new.txt` - it is zero bytes, indicating an empty file. We can start editing the file using one of the many available text editors that are available for use directly from a terminal, such as [`nano`](http://www.nano-editor.org/) or [`vi`](http://en.wikipedia.org/wiki/Vi). While we don't cover how to use these editors here, you can [have a look online for a simple how-to tutorial](http://www.howtogeek.com/howto/42980/the-beginners-guide-to-nano-the-linux-command-line-text-editor/). We suggest starting with `nano` - while there are not as many features available compared to other editors, using `nano` is much simpler.

## Core Commands {#section-unix-commands}
In the short tutorial above, you've covered a few of the core commands such as `pwd`, `ls` and `cd`. There are however a few more standard UNIX commands that you should familiarise yourself with before you start working for real. These are listed below for your reference, with most of them focusing upon file management. The list comes with an explanation of each, and an example of how to use them.

* `pwd`: As explained previously, this command displays your *present working directory* to the terminal. The full path of where you are presently is displayed.
* `ls`: Displays a list of files in the current working directory to the terminal. 
* `cd`: In conjunction with a path, `cd` allows you to change your present working directory. For example, the command `cd /users/grad/david/` changes the current working directory to `/users/grad/david/`. You can also move up a directory level without having to provide the [absolute path](http://www.coffeecup.com/help/articles/absolute-vs-relative-pathslinks/) by using two dots, e.g. `cd ..`.
* `cp`: Copies files and/or directories. You must provide the *source* and the *target*. For example, to make a copy of the file `input.py` in the same directory, you could issue the command `cp input.py input_backup.py`.
* `mv`: Moves files/directories. Like `cp`, you must provide the *source* and *target*. This command is also used to rename files. For example, to rename `numbers.txt` to `letters.txt`, issue the command `mv numbers.txt letters.txt`. To move a file to a different directory, you would supply either an absolute or relative path as part of the target - like `mv numbers.txt /home/david/numbers.txt`.
* `mkdir`: Creates a directory in your current working directory. You need to supply a name for the new directory after the `mkdir` command. For example, if your current working directory was `/home/david/` and you ran `mkdir music`, you would then have a directory `/home/david/music/`. You will need to then `cd` into the newly created directory to access it.
* `rm`: Shorthand for *remove*, this command removes or deletes files from your filesystem. You must supply the filename(s) you wish to remove. Upon issuing a `rm` command, you will be prompted if you wish to delete the file(s) selected. You can also remove directories [using the recursive switch](http://www.computerhope.com/issues/ch000798.htm). Be careful with this command - recovering deleted files is very difficult, if not impossible!
* `rmdir`: An alternative command to remove directories from your filesystem. Provide a directory that you wish to remove. Again, be careful: you will not be prompted to confirm your intentions.
* `sudo`: A program which allows you to run commands with the security privileges of another user. Typically, the program is used to run other programs as `root` - the [superuser](http://en.wikipedia.org/wiki/Superuser) of any UNIX-based or UNIX-derived operating system.

I> ### There's More!
I> This is only a brief list of commands. Check out Ubuntu's documentation on [Using the Terminal](https://help.ubuntu.com/community/UsingTheTerminal) for a more detailed overview, or the [Cheat Sheet](http://fosswire.com/post/2007/08/unixlinux-command-cheat-sheet/) by FOSSwire for a quick, handy reference guide. Like anything else, the more you practice, the more comfortable you will feel working with the terminal.