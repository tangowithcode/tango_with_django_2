# Use this script to order people by their first name.
# Watch for UNICODE

f = open('chapter-summary.md', 'r')
in_acks_list = False

people = []


for line in f:
    line = line.strip()
    
    if '%% BEGIN ACKNOWLEDGEMENTS LIST' in line:
        in_acks_list = True
        continue
    
    if '%% END ACKNOWLEDGEMENTS LIST' in line:
        in_acks_list = False
        break
    
    if in_acks_list and line != "":
        if line.startswith('['):
            name = line[1:line.index(']')]
        elif line.startswith('**['):
            name = line[3:line.index(']')]
            line = line[3:]
        elif line.startswith('**'):
            name = line[2:]
            line = line[2:]
        else:
            name = line
        
        if name[-1] == ',':
            name = name[:-1]
        
        if line[-2:len(line)] == '**':
            line = line[0:len(line)-2]
        
        if ']' in line:
            if not line.startswith('['):
                line = '[{0}'.format(line)
        
        name = name.lower()
        people.append((name, line))

# Sort
sorted_people = sorted(people, key=lambda x: x[0])

print

count = 0

for person in sorted_people:
    if count % 2 == 0:
        print '**{person}**'.format(person=person[1])
    else:
        print person[1]
    
    count = count + 1

print

f.close()