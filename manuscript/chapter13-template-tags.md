#Template Tags


##Providing Categories on Every Page

It would be nice to show the different categories that users can browse
through in the sidebar on each page. Given what we have learnt so far we
could do the following:

-   In the `base.html` template we could add some code to display an
    item list of categories, if the category list has been passed
    through.
-   Then in each view, we could access the Category object, get all the
    categories, and return that in the context dictionary.

However, this is a pretty nasty solution. It requires a lot of cutting
and pasting of code. Also, we will run into problems, when we want to
show the categories on pages serviced by the django-registration-redux
package. So we need a different approach, by using `templatetags` that
are included in the template that request the data required.

###Using Template Tags

Create a directory `rango/templatetags`, and create two files, one
called `__init__.py`, which will be empty, and another called,
`rango_extras.py`, where you can add the following code:

{lang="python",linenos=off}
	from django import template
	from rango.models import Category

	register = template.Library()

	@register.inclusion_tag('rango/cats.html')
	def get_category_list():
    	return {'cats': Category.objects.all()}

As you can see we have made a method called, `get_category_list()` which
returns the list of categories, and that is assocaited with a template
called `rango/cats.html`. Now create a template called
''rango/cats.html`in the templates directory with the following code:  

{lang="html",linenos=off}
	<ul class="nav nav-sidebar">
	{% if cats %}
		{% for c in cats %}             
			<li><a href="{% url 'category'  c.slug %}">{{ c.name }}</a></li>
		{% endfor %}      
	{% else %}
		<li> <strong >There are no category present.</strong></li>	
	{% endif %}  
	</ul> 
	
Now in your`base.html`you can access the template tag by first loading it up with`{%
load rango\_extras %}`and then slotting it into the page with`{%
get\_category\_list
%}`, i.e.:  

{lang="html",linenos=off}      
	<div class="col-sm-3 col-md-2 sidebar">          
		{% block side_block %}         
		{% get_category_list %}         
		{% endblock %}      
	</div>   
	

I> Restart Server to Register Tags
I>
I> You will need to restart your server every time you modify the template tags. Otherwise they will not be registered, and you will be really confused why your code is not working.

###Parameterised Template Tags 

Now lets extend this so that when we visit a category page, it highlights which category we are in. To do this we need to paramterise the templatetag. So update the method in`rango\_extras.py`to be: 

{lang="python",linenos=off}
       def get_category_list(cat=None):         
	   return {'cats': Category.objects.all(), 'act_cat': cat}  


This lets us pass through the category we are on. We can now update the`base.html`to pass through the category, if it exists.  

{lang="html",linenos=off}

	<div class="col-sm-3 col-md-2 sidebar">          
	{% block side_block %}         
	{% get_category_list category %}         
	{% endblock %}      
	</div>   
	
Now update the`cats.html` template:   

{lang="html",linenos=off}
	{% for c in cats %}
		{% if c == act_cat %} 
			<li  class="active" > 
		{% else  %} 
			 <li>
		{% endif %}
			<a href="{% url 'category'  c.slug %}">{{ c.name }}</a></li>
	{% endfor %}


Here we check to see if the category being displayed is the same as the category being passed through (i.e.`act\_cat`), if so, we assign the`active`class to it from Bootstrap (http://getbootstrap.com/components/#nav).   Restart the development web server, and now visit the pages. We have passed through the`category`variable. When you view a category page, the template has access to the`category`variable, and so provides a value to the template tag`get\_category\_list()`. This is then used in the`cats.html\`\`
template to select which category to highlight as active.
