# Chapter 1: Welcome

![](images/data_to_conspiracy.jpg)

Credit: unknown

## Welcome

Welcome to the course "Information Science" for the University of Antwerp __[Master of Linguistics](https://www.uantwerpen.be/en/study/programmes/all-programmes/digital-text-analysis/)__ (from 2021-2022 onwards: "Master of Digital Text Analysis")!

## Who am I and why does that matter?

### Who am I?

My name is Tom Deneire, I hold a PhD in Classics from the Katholieke Universiteit Leuven (2009). 

From 2009-2013 I worked as a **postdoctoral researcher** (Neo-Latin Studies) and a visiting professor (Latin rhetoric and stylistics), focussing mainly on the interplay of Neo-Latin and the vernacular, literary theory and dabbling in (then emerging) Digital Humanities (see e.g. __[Deneire 2018](https://hdl.handle.net/10067/1535070151162165141)__).

In 2013 I moved to the University Library of Antwerp as **Curator of the Special Collections**, where I became increasingly interested in library metadata and data science. I started studying  XML, SQL and Python, and using these digital tools to research and aggregate library metadata.

In 2018 this lead to a switch from the Special Collections to the University Library's software department __[Anet](https://www.uantwerpen.be/nl/projecten/anet/)__, where I have been  working since then as a **software engineer** for __[Brocade Library Services](https://en.wikipedia.org/wiki/Brocade_Library_Services)__. My main languages are Python and especially __[MUMPS](https://en.wikipedia.org/wiki/MUMPS)__, the language for our database engine (GT.M, provided by __[YottaDB](https://yottadb.com/)__). My current project is a complete rewrite and integration of the library's double module for authority files. Occasionally, I also use SQL, Golang, PHP, Javascript and HTML/CSS. I use Linux as OS (esp. the __[Linux Mint](https://linuxmint.com/)__ distro).

(More information about me and links at __[https://tomdeneire.github.io/](https://tomdeneire.github.io/)__).

### Why does that matter?

The above should make clear that I am not an expert in Information Science, nor a Computer Science major, nor have I been a professional developer for a long time. Indeed, at first I was not sure if I should really be teaching this course! So be warned that I will certainly not have all the answers in this course. On the other hand, my own profile is very kindred to that of my **intended audience**: humanities majors looking to acquire digital skills. I hope this common perspective will enable me to teach what such students need most from a vast field such as Information Science.

## Course contents and learning outcomes

My specific profile also implies that this will not be a standard introduction to Information Science. If this is really what you are after, I think there is enough scholarly literature out there to get by. Instead what is offered here is a very hands-on introduction into library science and the technologies used in the field. Indeed, I am not exaggerating if I claim that in my professional activities developing library software, I will use each and every one of the topics dealt with in this course on an almost **daily basis**.

The aim of this course is to provide you with enough theoretical knowledge and especially practical experience to use these technologies in the field.

## Technical setup

I have prepared this course as a series of Jupyter Notebooks and published on the __[GitHub repo](https://github.com/TomDeneire/InformationScience)__ for this course. 

I have chosen Jupyter Notebooks because they offer a way to teach both in a classroom and online (should COVID-19 regulations prohibit live teaching). You can choose how you interact with these notebooks.

To view the content **with code execution**, you can:

1. use an editor with a Jupyter Notebook extension, such as __[VS Code](https://code.visualstudio.com/)__
2. install __[Jupyter](https://jupyter.org/install)__ (Lab or Notebook) locally and open the notebooks in your browser

If you don't want to install Jupyter on your machine, you can open the notebooks with __[Google Colab](https://colab.research.google.com/notebooks/)__, but executing the code isn't always guaranteed to work (because of missing third-party libraries and stack overflows in heavy data operations).

To view the content **without code execution**, you can:

1. read the notebooks in this __[GitHub repository](https://github.com/TomDeneire/InformationScience/tree/main/course)__
2. read the notebooks as a Jupyter Book hosted on __[GitHub Pages](https://tomdeneire.github.io/InformationScience)__

In order to obtain these course materials and to participate with the course, please do the following:

1. fork this repo to your own GitHub account
2. clone it to your local machine
3. make and push changes 

The third step especially applies to the coding assignments (see below). By commiting and pushing your changes I will be able to see them by going through the different forks to my repo. And of course if you find errors in the other course materials or want to propose changes, you can also make pull requests.

If you're unsure how to do all of this, this __[GitHub guide](https://guides.github.com/activities/forking/)__ will help. (Other interesting sources on Git are this __[Medium article](https://link.medium.com/w1ShAzxQE9)__ and Atlassian's __[tutorial](https://www.atlassian.com/git/tutorials/what-is-git)__). This __[Medium article](https://link.medium.com/NdBy7ILHIbb)__ contains even more references to cheatsheets, tutorials, etc.

To be sure everyone is setup okay, please do the following:

1. create a new folder "assignments"
2. put some test code in there (e.g. "test.py"), commit and push these changes to your fork

## Course and assignments

During the academic year 2020-2021, the course will take place on Fridays, from 9h30 to 12h30, in room C.203, during weeks 9-13.

Each course will feature about 1,5 to 2 hours of theory and about 1 hour of practice. Most courses will feature a **coding assignment**, which will be introduced and discussed during the practical part of the course. Students are expected to finish the assignments after hours. 

Model solutions for the assignments will be made available in the repository with a few weeks delay.

### !Covid-19 update (5 November 2020)

The University of Antwerp has decided to switch to online teaching only, at least until 30 November. 

For this course this will be organized as follows:

1. About one week before the course takes place, students will receive a Google Drive link where they can view a recording of the week's course (+/- 1 hour).
2. Students watch the recording in their own time (+/- 1 hour) and also start implementing the coding assignment (+/- 0,5 hours).
3. On Fridays, from 9h30 to 11h (+/- 1,5 hours) we will meet in a Jitsi meeting room (link will be emailed) to discuss the course recording and the coding assignment. This session will also be recorded and uploaded to Google Drive.

I hope that this online method can provide the hands-on mix of theory and practice I had hoped to achieve in person, without putting any additional strain on the students.

If there are any changes to this MO, I will let the students know ASAP.


## Exam: Project assignment

The aforementioned assignments lead up to a **project assignment** which will serve as the exam for this course. The project assignment will be introduced during the final course. The course coding assignments are not part of the course evaluation, but students who have succesfully completed the previous course assignments will be excellently prepared for submitting an adequate project assignment. Students will be required to finish the project in a certain timeframe.

## Things you might find interesting

The following links are reading material *ad libitum*. While I certainly do not expect you to read them, you might find them interesting. In any case, I did! Please feel free to send me suggestions too!

As a general note: you'll notice that I often refer to __[Medium](https://medium.com/)__, an online publishing platform for blogs dealing with just about anything. Medium lets you configure your interests so you get a personalized list of reading suggestions. Medium allows you to read upto 3 premium articles for free every month, but I find a paying membership more than worthwile.

- Book recommendations for Python on __[Medium](https://towardsdatascience.com/python-books-you-must-read-in-2020-a0fc33798bb)__
- A fantastic Python __[cheat sheet](https://gto76.github.io/python-cheatsheet/)__
- A GitHub repo of __[free programming books](https://github.com/EbookFoundation/free-programming-books)__
- __[Computational Humanities Research](https://discourse.computational-humanities-research.org/)__, a platform for discussion on digital humanities, where you can also ask help with technical questions (code, tools, ...)


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
