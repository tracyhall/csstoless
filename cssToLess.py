import tinycss
import CSSMediaQueryParser
from sys import argv

script, f = argv

parser = CSSMediaQueryParser.CSSMediaQueryParser()
stylesheet = parser.parse_stylesheet_file(f)

dictRules = {}
output = ''
at_rules = ''


def addRule (sel, declarations, obj):
    sel = sel.strip()
    tokens = sel.split(' ')
    current_level = obj

    for item in tokens:
        if item not in current_level:
            current_level[item] = {}
        current_level = current_level[item]

    for dec in declarations:
        current_level[dec.name] = dec.value.as_css()

def addMedia (media, rules):
    media = '@media ' + media

    if media not in dictRules:
        dictRules[media] = {}

    for rule in rules:
        sels = rule.selector.as_css().split(',')
        for sel in sels:
            print sel
            addRule(sel, rule.declarations, dictRules[media])

def generateLess (obj):
    output = ''
    for key in obj:
        if type(obj[key]) == dict:
            output = output + key + '{' + generateLess(obj[key]) + '}'
        else:
            output = output + key + ':' + obj[key] + ';'
    return output

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))


for rule in stylesheet.rules:
    if (rule.at_keyword == '@import'):
        print rule
        at_rules = at_rules + rule.at_keyword + ' "' + rule.uri + '";'
    elif (rule.at_keyword == '@media'):
        addMedia(rule.media, rule.rules)
    else:
        sels = rule.selector.as_css().split(',')

        for sel in sels:
            addRule(sel, rule.declarations, dictRules)

output = at_rules + generateLess(dictRules)

print output

