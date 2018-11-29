import re
from collections import defaultdict

p5 = re.compile("(\S+)", re.MULTILINE|re.I)
def length_in_words(sub_element):
    tmp2 = p5.findall(sub_element)
    return len(tmp2)

f = open("756109104-10-K-19960321.txt")
#f = open("test.txt", 'r')
x = ""
for line in f:
    x += line

p1 = re.compile("([^\"])(item\s+7[^0-9a-z\"]*management(?:[^0-9a-z]{0,3}s)?\s+discussions?\s+and\s+analysis\s+of\s+(?:financial\s+conditions?\s+|results\s+of\s+operations?)(?:\s+and\s+results\s+of\s+operations?|\s+and\s+financial\s+conditions?)?)", re.I|re.DOTALL|re.MULTILINE)
p2 = re.compile("([^\"])(item\s+7[^0-9a-z\"]*a[^0-9a-z\"]*(?:quantitative\s+and\s+(?:qualitative|qualification)\s+disclosures?\s+about\s+)?market\s+risk)", re.I|re.DOTALL|re.MULTILINE)
p3 = re.compile("([^\"])(item\s+8[^0-9a-z\"]*.{0,40}financial\s+statements[^\.])", re.I|re.DOTALL|re.MULTILINE)
x = p1.sub("\1#######ITEM7:\2#######", x)
x = p2.sub("\1#######ITEM7A:\2#######", x)
x = p3.sub("\1#######ITEM8:\2#######", x)

#x = "#######   abc ####### abc #########"

x_list = x.split("#######")  # <== we can not use regular exp!!
y_list = []
z_list = []
p4 = re.compile("^(ITEM(?:7|7A|8)):(.*)$", re.MULTILINE)
for i in range(len(x_list)):
    tmp = p4.findall(x_list[i])
    if(len(tmp) != 0):
        z_list.append(tmp[0][1])
        y_list.append(str(i) + ':' + tmp[0][0])
    else:
        z_list.append(x_list[i])
        y_list.append(str(i) + ':' + str(length_in_words(x_list[i])))
        
#print(y_list)
y = ' '.join(y_list)
#print y
p6 = re.compile("((?:\d+:ITEM7 \d+:\d+ )+(?:\d+:ITEM7A \d+:\d+ )*)(?:\d+:ITEM8 \d+:\d+\s*)+")
M_list = p6.findall(y)

p7 = re.compile("\d+:")
p8 = re.compile("^\d+$")


best = 0
bestseq = ""
for i in range(len(M_list)):
    m = M_list[i]
    m = p7.sub("", m)
    m_list = m.split(" ")
    v = 0
    for j in range(len(m_list)):
        q = m_list[j]
        t_list = p8.findall(q)
        if (len(t_list) != 0):
            v += int(q)
    if (v > best):
        best = v
        bestseq = M_list[i]
        
# v, best, bestseq
# 1071    57633  3895:ITEM7 3896:57628 3897:ITEM7 3898:5

p9  = re.compile(":\S+")
p10 = re.compile("\s*$")
kept = defaultdict(lambda: 0)
if(bestseq != ""):
    bestseq = p9.sub("", bestseq)
    mm_list = bestseq.split(" ")
    print mm_list
    for i in range(len(mm_list)):
        mm = mm_list[i]
        if mm == '':
            continue
        z_list[int(mm)] = p10.sub("\n", z_list[int(mm)])
        print z_list[int(mm)]
        kept[int(mm)] = 1
else:
    print "no match"
    
p11 = re.compile("\b\d+:", re.MULTILINE)
y = p11.sub("", y )
#print y
yy_list = y.split(" ")
print(yy_list)
for i in range(len(yy_list)):
    if kept[i] != 0:
        print "*"
    print yy_list[i]+" "
print "\n"
        
    

#print(m_list)

   
#print(x)
#print y  
#item_list = p.findall("hello")
#for item in item_list[:]:
#    print(item)
