import tinycss
from sys import argv

script, f = argv

parser = tinycss.make_parser('page3')
stylesheet = parser.parse_stylesheet_file(f)

dictRules = {}
output = ''
at_rules = ''


def addRule (sel, declarations):
    sel = sel.strip()
    tokens = sel.split(' ')
    current_level = dictRules

    for item in tokens:
        if item not in current_level:
            current_level[item] = {}
        current_level = current_level[item]

    for dec in declarations:
        current_level[dec.name] = dec.value.as_css()


def generateLess (obj):
    output = ''
    for key in obj:
        if type(obj[key]) == dict:
            output = output + key + '{' + generateLess(obj[key]) + '}'
        else:
            output = output + key + ':' + obj[key] + ';'
    return output


for rule in stylesheet.rules:
    print rule
    if (rule.at_keyword):
        at_rules = at_rules + rule.at_keyword + ' "' + rule.uri + '";'
    else:
        sels = rule.selector.as_css().split(',')

        for sel in sels:
            addRule(sel, rule.declarations)

output = at_rules + generateLess(dictRules)

print output

