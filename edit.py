with open('data.csv', "r", encoding='utf-8') as fh:
    lines = fh.readlines()
with open('new_data.csv', "w", encoding='utf-8') as fh:
    #lines = fh.readlines()
    count = 0
    for line in lines:
        if not line:
            break
        
        line_list = line.split(';')
        if len(line_list) == 25:
            fh.write(line)
