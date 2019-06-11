#JQuery and Django {#chapter-jquery}
 [JQuery](https://jquery.com/) is a library written in JavaScript that lets you access the power of JavaScript without too much pain. 
 This is because a few lines of JQuery often encapsulates hundreds of lines of JavaScript. 
 Also, JQuery provides a suite of functionality that is mainly focused on manipulating HTML elements. 
 In this chapter, we will describe:

- how to incorporate JQuery within your Django app;
- explain how to interpret JQuery code; and
- and provide a number of small examples.

## Including JQuery in Your Django Project/App
In your *base* template include a reference to JQuery (we will be using version 3.3.1). You can do these either by including a reference directly to the JQuery site:

{lang="html",linenos=off}
 <script src="https://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	
or if you have downloaded and saved a copy to your static directory, then you can reference it as follows:

{lang="html",linenos=off}
	<script src="{% static "js/jquery-3.3.1.min.js" %}"></script>
	<script src="{% static "js/rango-jquery.js" %}"></script>

Note, that if you already done the [Bootstrap Chapter](#chapter-bootstrap), the the SLIM version of the JQuery library has already been imported, right at the bottom of the template.	You will need to change it, otherwise you wont have access to the functions needed to perform AJAX calls in the next chapter!

Make sure you have your static files set up (see [Chapter Templates and Static Media](#chapter-templates-static)) and that you have `	{% load staticfiles %}` at the top of `base.html`.

Also, add a reference to a script called `rango-jquery.js` after the JQuery library import.

{lang="html",linenos=off}
	<script src="{% static "js/rango-jquery.js" %}"></script>

In the `static` directory, create a *js* directory and place the JQuery JavaScript file (`jquery.js`) here along with an file called `rango-jquery.js`. This script will house our JavaScript code. In `rango-jquery.js`, add the following JavaScript:

{lang="javascript",linenos=off}
	$(document).ready(function() {
	    // JQuery code to be added in here.
	});

This piece of JavaScript utilises JQuery. It first selects the document object (with `$(document)`), and then makes a call to `ready()`. Once the document is ready (i.e. the complete page is loaded), the anonymous function denoted by `function() { }` will be executed. It is pretty typical, if not standard, to wait until the document has been finished loading before running the JQuery functions. Otherwise, the code may begin executing before all the HTML elements have been downloaded. See the [JQuery Documentation on Ready](http://api.jquery.com/ready/) for more details.

I> ### Select and Act Pattern
I> JQuery requires you to think in a more *functional* programming style, as opposed to the typical JavaScript style which is often written in a more *procedural* programming style. For all the JQuery commands, they follow a similar pattern: **Select and Act**. Select an element, and then perform some action on/with the element.

### Example Popup Box on Click
In this example, we want to show you the difference between doing the same functionality in standard JavaScript versus JQuery. In your `about.html` template, add the following piece of code:

{lang="html",linenos=off}
    <button  class="btn btn-primary" 
        onClick="alert('You clicked the button using inline JavaScript.');"> 
        Click Me - I run JavaScript 
    </button>

As you can see, we are assigning the function `alert()` to the `onClick` handler of the button. Load up the `about` page, and try it out. Now lets do it using JQuery, by first adding another button:

{lang="html",linenos=off}
	<button  class="btn btn-primary" id="about-btn"> 
	    Click Me - I'm JavaScript on Ice
    </button>

Notice that there is no JavaScript code associated with the button currently. We will be doing that with the following code added to `rango-jquery.js`:

{lang="javascript",linenos=off}
	$(document).ready( function() {
	    $("#about-btn").click( function(event) {
	        alert("You clicked the button using JQuery!");
	    });
	});

Reload the page, and try it out. Hopefully, you will see that both buttons pop up an alert.

The JQuery/JavaScript code here first selects the document object, and when it is ready, it executes the functions within its body, i.e. `$("#about-btn").click()`. This code selects the element in the page with an `id` equal to `about-btn`, and then programatically assigns to the `click` event the `alert()` function.

At first, you might think that JQuery is rather cumbersome, as it requires us to include a lot more code to do the same thing. This may be true for a simple function like `alert()`. For more complex functions, it is much cleaner as the JQuery/JavaScript code is maintained in a separate file. This is because we assign the event handler at runtime rather than statically within the code. We achieve separation of concerns between the JQuery/JavaScript code and the HTML markup.

T> ###Keep Them Separated
T> [Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) is a design principle that is good to keep in mind. In terms of web apps, the HTML is responsible for the page content; CSS is used to style the presentation of the content, while JavaScript is responsible for how the user can interact with the content, and manipulating the content and style.
T>
T> By keeping them separated, you will have cleaner code and you will reduce maintenance woes in the future.
T>
T> Put another way, *never mix, never worry!*

### Selectors
There are different ways to select elements in JQuery. The above example shows how the `#` selector can be used to find elements with a particular `id` in your HTML document. To find classes, you can use the `.` selector, as shown in the example below.

{lang="javascript",linenos=off}
	$(".ouch").click( function(event) {
	    alert("You clicked me! ouch!");
	});

Then all elements in the document that have the `class="ouch"` would be selected, and assigned to its on click handler, the `alert()` function. Note that all the elements would be assigned the same function.

HTML tags can also be selected by referring to the tag in the selector:

{lang="javascript",linenos=off}
	$("p").hover( function() {
	    $(this).css('color', 'red');
	}, 
	function() {
	    $(this).css('color', 'black');
	});

Add this JavaScript to your `rango-jquery.js`, and then in the `about.html` template, add a paragraph, `<p>This text is for a JQuery Example</p>`. Try it out, go to the about page and hover over the text.

Here, we are selecting all the `p` HTML elements, and on hover we are associated two functions, one for on hover, and the other for hover off. You can see that we are using another selector called, `this`, which selects the element in question, and then sets its colour to red or blue respectively. Note that the JQuery `hover()` function takes [two functions](http://api.jquery.com/hover/), and the JQuery [`click()`](http://api.jquery.com/click/) function requires the event to be passed through.

Try adding the above code your `rango-jquery.js` file, making sure it is within the `$(document).ready()` function. What happens if you change the `$(this)` to `$(p)`?

Hovering is an example of a mouse move event. For descriptions on other such events, see the [JQuery API documentation](http://api.jquery.com/category/events/mouse-events/).

## DOM Manipulation Example
In the above example, we used the `hover` function to assign an event handler to the on hover event, and then used the `css` function to change the colour of the element. The `css` function is one example of DOM manipulation, however, the standard JQuery library provides many other ways in which to manipulate the DOM. For example, we can add classes to elements, with the `addClass` function:

{lang="javascript",linenos=off}
	$("#about-btn").removeClass('btn-primary').addClass('btn-success');

This will select the element with `id` `#about-btn`, and first remove the `btn-primary` class which makes the button blue, and then adds the `btn-success` class to make it green. 

It is also possible to access the inner HTML of a particular element. For example, lets put a `div` in the `about.html` template:

{lang="html",linenos=off}
	<div id="msg">Hello  - I'm here for a JQuery Example too</div>

Then add the following JQuery to `rango-jquery.js`:

{lang="javascript",linenos=off}
	$("#about-btn").click( function(event) {
	    msgstr = $("#msg").html()
	    msgstr = msgstr + "ooo"
	    $("#msg").html(msgstr)
	});

When the element with `id` `#about-btn` is clicked, we first get the HTML inside the element with `id` `msg` and append `"o"` to it. We then change the HTML inside the element by calling the `html()` function again, but this time passing through string `msgstr` to replace the HTML inside that element.

In this chapter, we have provided a very rudimentary guide to using JQuery and how you can incorporate it within your Django app. From here, you should be able to understand how JQuery operates and experiment with the different functions and libraries provided by JQuery and JQuery developers. In the next chapter, we will be using JQuery to help provide AJAX functionality within Rango.