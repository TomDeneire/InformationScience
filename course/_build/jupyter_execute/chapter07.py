# Chapter 7: Searching, Evaluation, Ranking

## Introduction

In the previous chapter we went from searching to indexing rather quickly. In fact, although we acknowledged that searching is a discrete field of computer science, we limited our practical discussion of it to an example of *string*.find(*substring*) in Python! Evidently, there is more to searching than just this. Moreover, we also need to say something about the crucial follow-up of any searching operation, i.e. the evaluation and subsequent ranking of the search results. Indeed, the very basic Information Retrieval model is:

> Retrieval > Searching > Evaluation > Ranking

Having already discussed some of the aspects of retrieval (e.g. querying), in this chapter, we will try to discuss the other factors. Again, we will do so from a very practical and hands-on standpoint, neglecting more or less completely the theoretical or multimedia dimension of these issues (see chapters 4-5, 14 in *Modern Information Retrieval*). Indeed, we will focus on text exclusively here.

## Searching

We have already seen that searching text is rarely as easy as `string.find(substring)`. Searching vast data sets lead us to indexing, as did the issue of complex searches, such as Boolean queries. However, not all of the complex searches can be solved with indexing. Sometimes we want to include wildcards (many people are familiar with the `*` symbol) in our search, while other times we are not looking for exact results, but more interested in *fuzzy* searching.

### Regular expressions

![](images/regex.png)

Credit: [xkcd.com](https://xkcd.com/1171/)

The `*` symbol we used is actually part of a separate programming language, called **regular expressions**. [Wikipedia](https://en.wikipedia.org/wiki/Regular_expression) says:

> A regular expression (shortened as regex or regexp; also referred to as rational expression) is a sequence of characters that define a search pattern. Usually such patterns are used by string-searching algorithms for "find" or "find and replace" operations on strings, or for input validation. It is a technique developed in theoretical computer science and formal language theory.

> The concept arose in the 1950s when the American mathematician Stephen Cole Kleene formalized the description of a regular language. The concept came into common use with Unix text-processing utilities. Different syntaxes for writing regular expressions have existed since the 1980s, one being the POSIX standard and another, widely used, being the Perl syntax.

> Regular expressions are used in search engines, search and replace dialogs of word processors and text editors, in text processing utilities such as sed and AWK and in lexical analysis. Many programming languages provide regex capabilities either built-in or via libraries.

Python uses the Perl regex syntax, as do, for instance, Java, JavaScript, Julia, Python, Ruby, Microsoft's .NET Framework, and others. Some environments actually let you choose the regex syntax you want to use, like PHP or the UNIX `grep` command.

Regular expressions are an extremely powerful tool, but as the above cartoon shows there is a downside too. It is sometimes said that regular expressions are a *write only* programming language, as the code is often hardly readable, especially if you revisit a regex written long ago. Moreover, regular expresssions can be very tricky, for example, when they provide exact matches in your tests, only to produce mismatches when you open up the use cases. 

Consider this example:


import re

rhyme = re.compile(r'\Dar')
my_text = "Let's look at the words bar, car, tar, mar and far"
print(re.findall(rhyme, my_text))

So I'm looking for potential rhymes on "bar" and have written a regex that looks for one letter character `\D` followed by `ar`. However, when you apply this to one of the paragraphs you quickly see some mismatches, as we forgot to specify that the pattern can only occur at the end of a word.

paragraph = "Regular expressions are an extremely powerful tool, but as the above cartoon shows there is a downside too. It is sometimes said that regular expressions are a write only programming language, as the code is often hardly readable, especially if you revisit a regex written long ago. Moreover, regular expresssions can be very tricky, for example, when they provide exact matches in your tests, only to produce mismatches when you open up the use cases."
print(re.findall(rhyme, paragraph))

So when you are inclined to use regular expressions, it is often good to ask yourself: is this the best solution for this problem. If you find yourself parsing XML with regular expressions (use a parsing library), or testing the type of user input with regexes (use `.isinstance()`), reconsider!

The only way to really get the hang of regular expressions is by diving in the deep end. Fortunately, there are many good tutorials online (e.g. at [w3schools](https://www.w3schools.com/python/python_regex.asp)) and there are also handy regex testers where you can immediately check your regex, like [regexr](https://regexr.com/). For a good Python cheat sheet, see this [Medium post](https://link.medium.com/BYkb73meJab).

A good and certainly not trivial exercise would be to write a regex that can detect a valid email address, as specified in [RFC 5322](https://tools.ietf.org/html/rfc5322). For a (more readable) summary, see [Wikipedia](https://en.wikipedia.org/wiki/Email_address#Syntax).

In practice, most applications that ask you to enter an email address will check on a simple subset of the specification. Can you whip something up that passes this test?

# Examples from https://en.wikipedia.org/wiki/Email_address#Examples
TEST = {
    # valid addresses
    "simple@example.com": True, 
    "very.common@example.com": True, 
    "disposable.style.email.with+symbol@example.com": True, 
    "other.email-with-hyphen@example.com": True, 
    "x@example.com (one-letter local-part)": True, 
    "admin@mailserver1": True,  # local domain name with no TLD, although ICANN highly discourages dotless email addresses
    # invalid_addresses
    "Abc.example.com": False,  # no @ character
    "A@b@c@example.com": False,  # only one @ is allowed outside quotation marks
    "1234567890123456789012345678901234567890123456789012345678901234+x@example.com": False,  # local part is longer than 64 characters
    "i_like_underscore@but_its_not_allow_in_this_part.example.com": False  # underscore is not allowed in domain part
}

def email_regex(address: str) -> bool:
    # expand test
    if address.count("@") == 1:
        return True
    else:
        return False

for case in TEST:
    result = email_regex(case)
    if not result == TEST[case]:
        print(f"Test failed on {case}. Expected = {TEST[case]}. Result = {result}")
    


### Fuzzy searching

Regular expressions can also be used to illustrate the concept of fuzzy searching or approximate string matching, which is the technique of finding strings that match a pattern approximately rather than exactly. __[Wikipedia](https://en.wikipedia.org/wiki/Approximate_string_matching)__ explains:

> The closeness of a match is measured in terms of the number of primitive operations necessary to convert the string into an exact match. This number is called the edit distance between the string and the pattern. The usual primitive operations are:

> > insertion: cot → co**a**t

> > deletion: co**a**t → cot

> > substitution: co**a**t → co**s**t

>These three operations may be generalized as forms of substitution by adding a NULL character (here symbolized by `*`) wherever a character has been deleted or inserted:

> > insertion: co*****t → co**a**t

> > deletion: co**a**t → co\*t

> > substitution: co**a**t → co**s**t

> Some approximate matchers also treat transposition, in which the positions of two letters in the string are swapped, to be a primitive operation.

> > transposition: co**st** → co**ts**

> Different approximate matchers impose different constraints. Some matchers use a single global unweighted cost, that is, the total number of primitive operations necessary to convert the match to the pattern. For example, if the pattern is coil, foil differs by one substitution, coils by one insertion, oil by one deletion, and foal by two substitutions. If all operations count as a single unit of cost and the limit is set to one, foil, coils, and oil will count as matches while foal will not.

>Other matchers specify the number of operations of each type separately, while still others set a total cost but allow different weights to be assigned to different operations. Some matchers permit separate assignments of limits and weights to individual groups in the pattern.

#### String metrics

A __[string metric](https://en.wikipedia.org/wiki/String_metric)__ (also known as a string similarity metric or string distance function) is a metric that measures distance ("inverse similarity") between two text strings. A string metric provides a number indicating an algorithm-specific indication of distance. The most widely known string metric is a rudimentary one called the __[Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance)__ (also known as edit distance). Another is the __[Jaro-Winkler distance](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)__.

## Evaluation and ranking

With string metrics we have arrived in the territory of search evaluation: so-called __[evaluation measures](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)__) offer us an exact means to quantify the success of our search. Nowadays, with the advent of big data and the ubiquity of information, the best search engines make the difference not by the amount of information they yield, but by the ranking of the results they display. Unfortunately, the scope of this course is too limited to go into ranking more deeply.

## Assignment: Spelling checker

One very practical application of string metrics, search evaluation and ranking is writing a spelling checker. 

I'm not going to reveal too much of the solution here, but what I can say is that you'll definitely need two things:

1. A dictionary of existing words. As the corpus of the dictionary you can use the collection of words found in the British fiction corpus from the previous chapter. This is limited, but it'll do for now.

2. A string metric. For this, you can use the Jaro-Winkler metric, which you do not have to implement yourself. Instead just use the code supplied in `jarowinkler.py` as shown below.

Your application should do two things:

1. Build the dictionary and save it in some form so it does not have to be rebuilt every time when the application is used.

2. Take a string and print on standard output a list of potential spelling mistakes, with a limited number of suggestions for the correction.

As a final tip, you should consider reusing some of your code from chapter 3 for this application...


from jarowinkler import jaro_winkler
print(jaro_winkler("coat", "cot"))

