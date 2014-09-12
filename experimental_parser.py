import re

ss = "header\n=====\n\nnormal text here\nwith some extra stuff\nand moar lines\n\n= simple answer\n\nsome more text here\nand here\n[explanation]\nexplanation\n[explanation]"
print(ss)

header = ""

# question stuff
question = ""
kind = ""
options = []
answer = []
explanation = ""
no_more_questions = False

'''
parse lines:

    if line has 2 or more '==' followed by \n, previous line must be header
        else treat as text

    if line has ' = <text>\n' set question to <text> and kind to 'text', then set no_more_questions to true
        else treat as text

    if line has [] / () work on this later
        treat as text for now

    if line has '[explanation]\n', check for next '[explanation]' and set explanation to that content
        else treat as text

    convert blank lines to <br/> !!!
    create html fragment via XBlock

'''

tmp = ss.split('\n')
fragment = []

print("\n\n--- Parsing")

i = 0

while i < len(tmp):

    line = tmp[i]

    # Try for headers

    if i < len(tmp) - 1 and re.search(r'(={2})', tmp[i+1]):
        fragment.append("<h1>" + tmp[i] + "</h1>")
        i += 1 # skip next line

    # Try for text question
    elif re.search(r'(= .*)', line):

        if not no_more_questions:
        
            options.append(line[2:])
            answer.append(0)
            kind = "text"
            no_more_questions = True
            fragment.append("<input type=\"text\">") # needs work

    # Try for multiple answer question

    # Try for multiple choice question

    # Try for explanation
    elif line == "[explanation]":

        # seek the end of the string or the next occurrence of [explanation]
        for x in range(i+1, len(tmp)):

            if tmp[x] == "[explanation]":
                i = x
                break
            else:
                explanation += tmp[x] + '\n'

    # Treat as regular text or new line
    else:

        if line == "":
            fragment.append("<br/>")

        else:

            if not no_more_questions:
                question += line + '\n'

            fragment.append("<p>" + line + "</p>")

    i += 1

print "\n\n--- Vars"
print question[:-1]
print kind
print options
print answer
print explanation[:-1]

print "\n\n--- HTML output"

for tag in fragment:
    print(tag)
