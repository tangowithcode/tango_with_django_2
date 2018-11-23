# Logging {#chapter-logging}
Building a web application and getting the functionality working is only just part of the process. Web applications need to evolve and improve - while we could get feedback from users on what they like and what they dont like - this would take a lot of time and be quite costly. Worse still is that if you ask ten users you will get ten different answers - while intitially this is very helpful - it will largely tell you things that you have already identified as problematic. For example, if you log in and it is not clear that you are logged in. If there are a number of steps that need to be taken to complete a process but there is not clear set of steps to follow. Or, that the style doesn't render properly on different devices, etc. What is very difficult to determine is whether adding, changing, improving particular improvements are making people happier or making the product more successful.

A key part of developing data-driven web applications is to provide infrastructure for the logging and recording of user interactions with the web application. So, for instance, let's say that we want to add an extra feature to Rango - will the feature be used? who will use the feature? does the feature add more value to Rango? These are important questions. Often more and more features are requested - users want extra features, clients want extra features, developers want to add some extra feature that they like, etc.  This leads to a well known anti-pattern called, [feature creep]<https://en.wikipedia.org/wiki/Feature_creep> which results software bloat. The more features in the web application the more maintenance.


By logging the interactions of users, we can obtain a picture of how people are using our web application. Then, if we add a new feature, we can see how their behavior changes in response to the new feature. Let's say we add a quick add feature, so that it is easier and faster to add categories or pages. Does this actually lead to more categories being created? Maybe, but are these new categories or pages any good? And if there is not an increase in categories being created, why?  

Let's say we did add such a feature - then what information would we want to record? We want to know when we introduced the feature, when categories were created, how they were created i.e. through the new quick add feature or through the standard feature,  what pages were added, which user created/add the pages, and what were their characteristics i.e. new user, long term user, a user that has added many cats/pages, etc. 

As you can see there is lots of different things we will want to know. But what if we had a different feature, say we had a new recommendation algorithm, which would suggest links to users based on their past interaction. What kinds of things would we want to log and track?


We will want to know how many of the recommendations were selected, and by which user, we might want to record what recommendations were shown, or and what was on the rest of the page. Essentially, there is no limit to want we might want to log - however, what we log determines what questions we can answer and how we can use the interaction data to inform the design and development of our application.



##Django Logging Functionality
- introduce django's inbuilt logging 
- explain how it is set up and how it logs django internals for debugging


##Application Specific Logging
- remove django logging
- set up our own logger
- create a method to log out interactions given a request, a message, and other information

- user (id or anon), exp_id=1, .... what other values?_
- should we create a decorator method? that logs when the view is called, and when the view is completed?
- add in some logging


##A/B Testing

- explain the basis of a/b testing
- goals, experiments, splitting data

- create a model to record the user id and exp id, cond_id
- current experiments dictionary - ( and traffic split)
- default app configuration

- experiment vs control
- handling experiment and control in views
- handling experiment and control in templates
- handling experiment and control in javascript?




# Processing the Log

- simulate log data?

- query the log

- extract out statistics

- compare

https://measuringu.com/usability-metrics/

https://usabilitygeek.com/usability-metrics-a-guide-to-quantify-system-usability/


https://conversionsciences.com/blog/ab-testing-statistics/
https://conversionxl.com/blog/ab-testing-statistics/


https://measuringu.com/papers/Sauro_Dumas_CHI2009.pdf



