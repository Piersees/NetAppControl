fr = open('../data/appGroups.data', 'r')
if True:
    if True:
        actions = fr.readlines()
        fr.close()
        dic = {}

        for action in actions:
            action = action.rstrip()
            try:
                line = action.split('|')
                if(line[0] not in dic):
                    dic[line[0]] = [line[1]]
                else:
                    dic[line[0]].append(line[1])
            except:
                pass

        print(dic)