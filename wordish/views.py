from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def isTextValid(t):
    if len(t) != 5:
        return False
    else:
        for char in t:
            if not (ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z')):
                return False
        return True

def getColor(target, guess):
    targetDict = {}
    for char in target:
        if char in targetDict:
            targetDict[char] += 1
        else:
            targetDict[char] = 1
    
    rtn = [None] * 5

    for i in range(0,5):
        if target[i] == guess[i]:
            rtn[i] = 'green'
            targetDict[target[i]] -= 1
        if (guess[i] not in targetDict):
            rtn[i] = 'grey'

    for i in range(0,5):
        if target[i] != guess[i]:
            if guess[i] in targetDict:
                if targetDict[guess[i]] > 0:
                    rtn[i] = 'yellow'
                    targetDict[guess[i]] -= 1
                else:
                    rtn[i] = 'grey'

    return rtn

def checkValidState(D):
    for key in D:
        # if key == 'guessedNum':
        #     if not (ord('1') <= ord(D[key]) <= ord('6')):
        #         return False
        # elif key == 'finished':
        #     if not (D[key] == "win" or D[key] == "lose"):
        #         return False
        # elif key == 'targetText':
        #     if not isTextValid(D[key]):
        #         return False
        # elif 'color' in key:
        #     if not (D[key] == "green" or D[key] == "grey" or D[key] == "yellow"):
        #         return False
        # elif (key != 'guessText') and ('guess' in key):
        #     if not (len(D[key]) == 1 and (ord('A') <= ord(D[key]) <= ord('z'))):
        #         return False
        if D[key] == 'blahblah':
            return False
    return True
#context contains: 
#    context['status'] = "Please provide a guess." to display the status of the Game 
#    context['guessedNum']

#    context['guessText']
#    context['targetText'] 
#    context['guess00'] ... context['guess04']
#    ...
#    context['guess50'] ... context['guess54']
#    context['color00'] ... context['color04']
#    ...
#    context['color50'] ... context['color54']

def copyContext(context, excludes):
    rtn = {}
    for key in context:
        if key not in excludes:
            rtn[key] = context[key]
    return rtn

def allGreen(cList):
    for c in cList:
        if c != 'green':
            return False
    return True

def home_page(request):
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    return render(request, 'wordish/index.html', {})

def startGame(request):
    context = {}

    if 'targetText' not in request.POST:
        context['status'] = "invalid input"
        return render(request, 'wordish/index.html', context)
    else:
        t = request.POST['targetText']
        if not isTextValid(t):
            context['status'] = "invalid input"
            return render(request, 'wordish/index.html', context)
        else:
            context['status'] = "Start"
            context['targetText'] = request.POST['targetText']
            return render(request, 'wordish/game_page.html', context)

def processGame(request):
    validFields = ['targetText', 'guessedNum', 'status', 'finished', 'guessText', 'csrfmiddlewaretoken',
                   'color00', 'color01','color02','color03','color04',
                   'color10', 'color11','color12','color13','color14',
                   'color20', 'color21','color22','color23','color24',
                   'color30', 'color31','color32','color33','color34',
                   'color40', 'color41','color42','color43','color44',
                   'color50', 'color51','color52','color53','color54',
                   'guess01', 'guess02','guess03','guess04','guess00',
                   'guess11', 'guess12','guess13','guess14','guess10',
                   'guess21', 'guess22','guess23','guess24','guess20',
                   'guess31', 'guess32','guess33','guess34','guess30',
                   'guess41', 'guess42','guess43','guess44','guess40',
                   'guess51', 'guess52','guess53','guess54','guess50',
    ]

    for key in request.POST:
        if key not in validFields:
            c = {'status': "error: invalid game state"}
            return render(request, 'wordish/index.html', c)

    if not checkValidState(request.POST):
        c = {'status': "error: invalid game state"}
        return render(request, 'wordish/index.html', c)

    if 'finished' in request.POST:
        c = copyContext(request.POST, [])
        return render(request, 'wordish/game_page.html', c)
    
    if 'guessText' not in request.POST:
        c = copyContext(request.POST, ['status'])
        c['status'] = "invalid input"
        return render(request, 'wordish/game_page.html', c)
    else:
        if not isTextValid(request.POST['guessText']):
            c = copyContext(request.POST, ['status'])
            c['status'] = "invalid input"
            return render(request, 'wordish/game_page.html', c)
        else:
            numGuesses = 0
            if 'guessedNum' in request.POST:
                numGuesses = int(request.POST['guessedNum'])

            c = copyContext(request.POST, ['status', 'guessedNum'])
            c['status'] = request.POST['guessText']
            if 'guessedNum' in request.POST:
                c['guessedNum'] = str(int(request.POST['guessedNum'])+1)
            else:
                c['guessedNum'] = 1
            
            colorList = getColor(request.POST['targetText'], request.POST['guessText'])

            for j in range(0,5):
                c['guess'+str(numGuesses)+str(j)] = request.POST['guessText'][j]
                c['color'+str(numGuesses)+str(j)] = colorList[j]

            if allGreen(colorList):
                c['status'] = "win"
                c['finished'] = 'win'

            if not allGreen(colorList):
                if int(c['guessedNum']) >= 6:
                    c['status'] = "lose"
                    c['finished'] = 'lose'
            
            return render(request, 'wordish/game_page.html', c)


        
