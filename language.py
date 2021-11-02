"""
Language Modeling Project
Name: Amulya
Roll No: 2021501007
"""

from types import new_class

from matplotlib.pyplot import bar
import language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    message = []
    with open(filename) as file1:
        txt = file1.read().splitlines()
    for i in txt:
        if len(i) !=0:
            message .append( i.split(' ') )
    return message


'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    sum = 0
    for word in corpus:
        sum = sum +len(word)
    return sum

'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    newlst = []
    for word in corpus:
        for i in word:
            if i not in newlst:
                newlst.append(i)
    return newlst


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    newlst = buildVocabulary(corpus)
    dict1 = {}
    for i in corpus:
        for j in i:
            if j in newlst:
                if j not in dict1:
                    dict1[j] = 1
                else:
                    dict1[j] +=1
    return dict1


'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus):
    newlst = []
    for i in corpus:
        if i[0] not in newlst:
            newlst.append(i[0])
    return newlst


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    strtlst = getStartWords(corpus)
    dict1 = {}
    for i in corpus:
        if i[0] in strtlst:
            if i[0] not in dict1:
                dict1[i[0]] = 1
            else:
                dict1[i[0]] +=1
    return dict1


'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    dict1 = {}
    for word in corpus:
        for j in range(len(word)-1):
            if word[j] not in dict1:
                dict1[word[j]] = {}
            if word[j+1] not in dict1[word[j]] :
                dict1[word[j]][word[j+1]] = 1
            else:
                dict1[word[j]][word[j+1]] +=1
    return dict1


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    newlst = []
    for i in unigrams:
        newlst.append(1 / len(unigrams))
    return newlst


'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    lst = []
    for i in range(len(unigrams)):
        if unigrams[i] in unigramCounts:
            lst.append(unigramCounts[unigrams[i]] / totalCount)
    return lst


'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    nesteddict = {}
    for prevWord in bigramCounts:
        word = []
        prob = []
        for key,value in bigramCounts[prevWord].items():
            word.append(key)
            prob.append(value / unigramCounts[prevWord]) 
            temp = {}
            temp["words"] =word
            temp["probs"] = prob
        nesteddict[prevWord] = temp
    return nesteddict


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
import operator
def getTopWords(count, words, probs, ignoreList):
    dict1 = {}
    dict2 = {}
    for i in range(len(words)):
        if i not in ignoreList:
            dict2[words[i]] = probs[i]
    mostcommon = dict(sorted(dict2.items(), key=operator.itemgetter(1), reverse=True))
    for i,j in mostcommon.items():
        if len(dict1) != count and i not in ignoreList:
            dict1[i] = j
    return dict1


'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
def generateTextFromUnigrams(count, words, probs):
    string = ""
    for i in range(count):
        rword = choices(words,weights = probs)
        string = string + rword[0] + ' '
    return string

'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    sentence = ""
    rword = choices(startWords, weights = startWordProbs)
    sentence += rword[0]
    lst = sentence
    for i in range(count-1):
        if lst != '.':
            if lst in bigramProbs:
                lst = choices(bigramProbs[lst]["words"], weights = bigramProbs[lst]["probs"])[0]
                sentence = sentence + ' ' + lst
        else:
            rword = choices(startWords, weights = startWordProbs)
            sentence =sentence+' '+ rword[0]
            lst = rword[0]
    return sentence


### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]


'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus):
    unigrams = buildVocabulary(corpus)
    unigramcount = countUnigrams(corpus)
    length = getCorpusLength(corpus)
    unigramprob = buildUnigramProbs(unigrams, unigramcount, length)
    res = getTopWords(50, unigrams, unigramprob, ignore)

    return barPlot(res,"Top 50")


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):
    strtwords = getStartWords(corpus)
    strtcount = countStartWords(corpus)
    strtprob = buildUnigramProbs(strtwords, strtcount, len(corpus))
    res = getTopWords(50, strtwords, strtprob, ignore)
    return barPlot(res, "Top Start Words")


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    unigramcount = countUnigrams(corpus)
    bigramcount = countBigrams(corpus)
    succword = buildBigramProbs(unigramcount, bigramcount)
    res = getTopWords(10, succword[word]["words"], succword[word]["probs"], ignore)
    return barPlot(res, "Top 10")


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    finaldict = {}
    frstprob = []
    secondprob = []
    unigrams1, unigrams = buildVocabulary(corpus1), buildVocabulary(corpus2)
    dict1, unigramcount = countUnigrams(corpus1), countUnigrams(corpus2)
    length1, length = getCorpusLength(corpus1), getCorpusLength(corpus2)
    probs1, unigramprob = buildUnigramProbs(unigrams1, dict1, length1), buildUnigramProbs(unigrams, unigramcount, length)
    res1, res2 = getTopWords(topWordCount, unigrams1, probs1, ignore), getTopWords(topWordCount, unigrams, unigramprob, ignore)
    lst = list(res1.keys()) + list(res2.keys())
    topwords = list(dict.fromkeys(lst))
    for i in range(len(topwords)):
        if topwords[i] in unigrams1:
            ind = unigrams1.index(topwords[i])
            frstprob.append(probs1[ind])
        else:
            frstprob.append(0)
        if topwords[i] in unigrams:
            ind = unigrams.index(topwords[i])
            secondprob.append(unigramprob[ind])
    finaldict["topWords"] = topwords
    finaldict["corpus1Probs"] = frstprob
    finaldict["corpus2Probs"] = secondprob
    return finaldict


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    dict1 = setupChartData(corpus1, corpus2, numWords)
    sideBySideBarPlots(dict1["topWords"], dict1["corpus1Probs"], dict1["corpus2Probs"], name1, name2, "Top Words Side By Side")
    return


'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    dict1 = setupChartData(corpus1, corpus2, numWords)
    scatterPlot(dict1["corpus1Probs"], dict1["corpus2Probs"], dict1["topWords"], "Top Words Scatter Plot")
    return


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()

    ## Uncomment these for Week 2 ##

    # print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.week2Tests()
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek2()


    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()