import re
ass = ['hello boi(nigga)', 'hello boi(nigga2)', 'hello boi(nigga3)', 'hello boi(nigga4)']
pattern = r'\((.*?)\)'
inner = []
for one in ass:
    word = (re.findall(pattern, one))
    inner.append(word[0])
print(inner)