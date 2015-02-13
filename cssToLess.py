import tinycss
import CSSMediaQueryParser
import argparse
from sys import argv

script, f = argv
ap = argparse.ArgumentParser(description='Translate a complex css file into a valid LESS file')
ap.add_argument('input', help='CSS file to translate.')
ap.add_argument('output', help='CSS output file.', default='output.css', nargs='?')
ap.add_argument('-p', '--pretty', dest='format', help='Pretty print the output file.', action='store_true')
ap.add_argument('-m', '--map', dest='varmap', help='Path to file with variable map.')
args = ap.parse_args()
print args

parser = CSSMediaQueryParser.CSSMediaQueryParser()
stylesheet = parser.parse_stylesheet_file(f)

dictRules = {}
output = ''
at_rules = ''


def add_rule (sel, declarations, obj):
    sel = sel.strip()
    tokens = sel.split(' ')
    current_level = obj

    for item in tokens:
        if item not in current_level:
            current_level[item] = {}
        current_level = current_level[item]

    for dec in declarations:
        current_level[dec.name] = dec.value.as_css()

def add_media (media, rules):
    media = '@media ' + media

    if media not in dictRules:
        dictRules[media] = {}

    for rule in rules:
        sels = rule.selector.as_css().split(',')
        for sel in sels:
            add_rule(sel, rule.declarations, dictRules[media])

def generate_less (obj):
    output = ''
    for key in obj:
        if type(obj[key]) == dict:
            output = output + key + '{' + generate_less(obj[key]) + '}'
        else:
            output = output + key + ':' + obj[key] + ';'
    return output

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))


for rule in stylesheet.rules:
    if (rule.at_keyword == '@import'):
        at_rules = at_rules + rule.at_keyword + ' "' + rule.uri + '";'
    elif (rule.at_keyword == '@media'):
        add_media(rule.media, rule.rules)
    else:
        sels = rule.selector.as_css().split(',')

        for sel in sels:
            add_rule(sel, rule.declarations, dictRules)

output = at_rules + generate_less(dictRules)

print output

with open('output.css', 'w') as f:
    f.write(output)

