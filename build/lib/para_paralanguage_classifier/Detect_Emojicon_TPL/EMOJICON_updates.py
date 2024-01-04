import regex
from itertools import groupby

temp1 = regex.findall(r'\X','❤️❤️❤️👨‍❤️‍💋‍👨 this is amazing !!!!! ')
temp2 = [w for w in temp if (w != ' ') & (len(re.findall('[a-zA-Z]', w)) ==0)]
temp3 = [key for key, _group in groupby(temp2)]


Counter(temp2), Counter(temp3)


temp1 = regex.findall(r'\X','^^ ^_^) this is amazing !!!!! ')
temp2 = [w for w in temp if (w != ' ') & (len(re.findall('[a-zA-Z]', w)) ==0)]
temp3 = [key for key, _group in groupby(temp2)]


Counter(temp2), Counter(temp3)
