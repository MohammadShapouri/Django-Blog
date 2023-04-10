from django import template

register = template.Library()



def check_existance_in_list(targetValue, targetString, ignoreSpaceBeforeFirstLetter):
    targetList = []

    if ignoreSpaceBeforeFirstLetter == False:
        targetString = targetString.replace(', ', ',')
        targetList = targetString.split(',')
    else:
        targetList = targetString.split(',')


    if targetValue in targetList:
        return True
    else:
        return False









register.filter('check_existance_in_list', check_existance_in_list)