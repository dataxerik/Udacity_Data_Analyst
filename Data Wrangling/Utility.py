temp = list()
with open('words.txt', 'r', encoding='utf-8') as fout:
    for line in fout:
        temp.append(line.strip())

print("<table>")
for row in temp:
    print('\t<tr>')
    for cell in row.split(','):
        print('\t\t<td>' + cell + '</td>')
    print('\t</tr>')
print("</table>")