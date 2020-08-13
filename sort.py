

def insertion_sort(InputList):
    for i in range(1, len(InputList)):
        j = i - 1
        nxt_element = InputList[i]
        while (InputList[j] > nxt_element) and (j >= 0):
            InputList[j + 1] = InputList[j]
            j = j - 1
        InputList[j + 1] = nxt_element
    return InputList


def my_sort(InputList):
    score = {}
    # this does not work properly yet!
    for unsorted in InputList:
        for check in InputList:
            if unsorted > check:
                if unsorted in score:
                    score[unsorted] += 1
                else:
                    score[unsorted] = 1
            else:
                if unsorted in score:
                    pass
                else:
                    score[unsorted] = 0
    print(score)
    sorted_list = ['x' for unsorted in InputList]
    for unsorted in InputList:
        index = score[unsorted]
        if sorted_list[index] == 'x':
            sorted_list[index] = unsorted
    return sorted_list


def random_sort(InputList):
    from random import shuffle
    check = 0
    while check == 0:
        shuffle(InputList)
        test = 0
        for unsorted in InputList:
            if unsorted >= test:
                check = 1
            else:
                check = 0
                break
            test = unsorted
    return InputList


unsorted_list = [0, 5, 6, 1, 2, 1, 11, 2]
print(insertion_sort(unsorted_list))
print(random_sort(unsorted_list))
print(my_sort(unsorted_list))
