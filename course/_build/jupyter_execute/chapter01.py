# Chapter 1: Welcome

![](images/welcome.png)

Credit: [xkcd](https://xkcd.com/722/)

## Welcome

Welcome to the course "Information Science" for the University of Antwerp [Master of Digital Text Analysis](https://www.uantwerpen.be/en/study/programmes/all-programmes/digital-text-analysis/)!

## Who am I and why does that matter?

### Who am I?

My name is [Tom Deneire](https://tomdeneire.github.io/) and I work as a **software engineer**.

However, my carreer did not start in IT. On the contrary, I studied Classics (MA 2003, PhD 2009) and was active in humanities research and education for quite some time.

From 2009-2013 I worked in **academia** as a postdoctoral researcher (Neo-Latin Studies) and a visiting professor (Latin rhetoric and stylistics), focussing mainly on the interplay of Neo-Latin and the vernacular, literary theory and dabbling in (then emerging) Digital Humanities (see e.g. [Deneire 2018](https://hdl.handle.net/10067/1535070151162165141)).

In 2013 I moved to the **library world** (University Library of Antwerp) as Curator of the Special Collections, where I became increasingly interested in library metadata and data science. I learned the basics of XML, SQL and Python, and started using these tools to research and aggregate library metadata.

In 2018 this lead to a switch from the Special Collections to the library's **software department** [Anet](https://www.uantwerpen.be/nl/projecten/anet/), where I have been working since on a product called [Brocade Library Services](https://en.wikipedia.org/wiki/Brocade_Library_Services). My technology stack mainly includes Python and especially [MUMPS](https://en.wikipedia.org/wiki/MUMPS), the language for our database engine (GT.M, provided by [YottaDB](https://yottadb.com/)). My current project is a complete rewrite and integration of the library's two modules for authority control. Occasionally, I also use SQL, Golang, HTML/CSS, Javascript and PHP. My OS of choice is Linux (i.c. the [Linux Mint](https://linuxmint.com/) distro).

### Why does that matter?

This should make clear that I am not an academic expert in Information Science, nor have I been a professional developer for a long time. Indeed, at first I was not sure if I am the best person to teach this course! So it goes without saying that I will certainly not have all the answers in this course. 

On the other hand, my profile is very kindred to that of my **intended audience**, which I think of as humanities majors looking to acquire digital skills. I hope this common perspective will enable me to teach what such students need most from a vast field such as Information Science.

## Contents and learning outcomes

My specific profile also implies that this will not be a standard introduction to Information Science. If this is really what you are after, there is enough  literature out there to acquire this knowledge by yourself. 

Instead what is offered here is a very **hands-on introduction** into information science and the technologies used in the field. Think of this class as an internship with an information systems company, rather than an academic course! The aim of this course is to provide you with a minimum of theoretical knowledge, but a maximum of practical experience.

The course will discuss the following topics:

1. Definition, history, ethics
2. Encoding
3. Databases
4. Querying
5. Metadata
6. Indexing
7. Searching

In line with the hands-on nature of this course, most chapters will feature a **coding assignment**, designed to offer a realistic example of a real-world implementation of the technology discussed in the chapter.

## Reading

### Required

Given the very applied nature of this course, I feel it is necessary to supplement it with a brief theoretical introduction to the topic of information. To meet that goal, this course requires reading chapters 1-7 of this highly readable book:

*Foundations of Information*, by Amy J. Ko (2021), available as a free [e-book](https://faculty.washington.edu/ajko/books/foundations-of-information/) and [GitHub repository](https://github.com/amyjko/foundations-of-information) 
  

### Optional

If a subject of this course is of particular interest to you, you can find more information about the various topics in the following publications:

- *Handbook of Information Science*, By Wolfgang G. Stock, Mechtild Stock, (Berlin: De Gruyter Saur, 2013), [ISBN 978-3110234992](https://isbnsearch.org/isbn/9783110234992), https://doi.org/10.1515/9783110235005

- *The Myth and Magic of Library Systems*, By Keith J. Kelley, [ISBN 978-0081000762](https://isbnsearch.org/isbn/9780081000762)

- *Modern Information Retrieval: The Concepts and Technology behind Search*, By Ricardo Baeza-Yates, Berthier Ribeiro-Neto, Second edition (Harlow e.a.: Addison-Wesley, 2011), [ISBN 978-0-321-41691-9](https://isbnsearch.org/isbn/9780321416919)

- *Information Architecture*, 4th Edition, By Louis Rosenfeld, Peter Morville, Jorge Arango, [ISBN 978-1491911686](https://isbnsearch.org/isbn/9781491911686)

- *A Librarian's Guide to Graphs, Data and the Semantic Web*, By James Powell, [ISBN 978-1843347538](https://isbnsearch.org/isbn/9781843347538)

- *Apprenticeship Patterns*, By Dave Hoover, Adewale Oshineye, [ISBN 978-0596518387](https://isbnsearch.org/isbn/9780596518387)

## Other resources

While this course is designed for beginners, it may still be possible that you feel your knowledge about a certain topic is lacking, especially when it comes to certain technological concepts. If so, the Internet offers a vast array of resources designed to help your learning process.

For me, one of the best resources for self-improvement is [Medium](https://medium.com/), an online publishing platform for blogs dealing with just about anything, but with a strong emphasis on software and technology. Medium lets you configure your interests so you get a personalized list of reading suggestions. Most articles on Medium are free and the site also allows you to read up to 3 premium articles for free every month. Personally, I find a paying membership more than worthwile.

Other good, free resources include:

- [Tutorialspoint](https://www.tutorialspoint.com/index.htm)
- [w3schools](https://www.w3schools.com/)

Finally, if you're looking for more hands-on introductions to topics similar to those treated in this course, you might want to have a look at [Library Carpentry](https://librarycarpentry.org/), a non-profit organization who offer free online [workshops](https://librarycarpentry.org/lessons/) teaching technical skills for people working in library- and information-related roles (UNIX shell, Git, Python, R, XML, ...).

## Technical requirements

This course is available as a series of Jupyter Notebooks and published on the [GitHub repository](https://github.com/TomDeneire/InformationScience) for this course. 

To view the content **without code execution**, you can:

1. Read the notebooks as a Jupyter Book hosted on [GitHub Pages](https://tomdeneire.github.io/InformationScience)
2. Read the notebooks in the [GitHub repository](https://github.com/TomDeneire/InformationScience/tree/main/course)

To view the content **with code execution**, you can:

1. Use an editor with a Jupyter Notebook extension, such as [VS Code](https://code.visualstudio.com/)
2. Install [Jupyter](https://jupyter.org/install) (Lab or Notebook) locally and open the notebooks in your browser

If you don't want to install Jupyter on your machine, you can open the notebooks with [Google Colab](https://colab.research.google.com/notebooks/), but executing the code isn't always guaranteed to work (because of missing third-party libraries and stack overflows in heavy data operations).

The best way to obtain these course materials on your local machine and to participate with the course, is to:

1. Get a GitHub account (if you don't already have one)
2. Fork this repo to your own GitHub account
3. Clone the repo to your local machine
4. Make a new folder in the repo and push changes 

The fourth step especially applies to the code assignments and would enable me (if you want!) to see your solutions for the assignments. The workflow for this is:

1. Create a new folder `assignments`
2. Create an empty file `test.py` in it
3. Add the new folder to the repo
4. Commit and push these changes to your fork 

And of course if you find errors in the other course materials or want to propose changes or additions, I am very open to pull requests.

### Git help!

If you're unsure how to do all of this, this [GitHub guide](https://guides.github.com/activities/forking/) will help. 

Other interesting sources on Git are this [Medium article](https://link.medium.com/w1ShAzxQE9) and Atlassian's [tutorial](https://www.atlassian.com/git/tutorials/what-is-git). This [Medium article](https://link.medium.com/NdBy7ILHIbb) contains even more references to cheatsheets, tutorials, etc.

Bear in mind that you can use Git from the command line (which I would always advise in the learning stages), but that there are also desktop applications, such as [GitHub Desktop](https://desktop.github.com/) or integrations for your editor, such as [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) for VSCode.




```{toctree}
:hidden:
:titlesonly:


chapter02
chapter03
chapter04
chapter05
chapter06
chapter07
chapter08
coursedetails
project
```
