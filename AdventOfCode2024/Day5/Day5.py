def part1():
    puzzle_input_file = open("day5_input.txt", "r")

    rules_dict = {}

    result = 0

    for line in puzzle_input_file:
        line = line.replace('\n', '')
        if not line:
            break
        couple = line.split('|')
        #print(couple)
        if couple[0] in rules_dict:
            rules_dict[couple[0]].append(couple[1])
        else:
            rules_dict[couple[0]] = [couple[1]]

    for line in puzzle_input_file:
        line = line.replace('\n', '')
        pages = line.split(',')
        already_seen = set()
        correct = True
        for p in pages:
            l = rules_dict.get(p, None)
            if l is not None:
                for c in l:
                    if c in already_seen:
                        correct = False
                        break
            already_seen.add(p)
        if correct:
            #print(line)
            result = result + int(pages[len(pages) // 2])

    print(result)

def part2():
    puzzle_input_file = open("day5_input.txt", "r")

    rules_dict = {}

    result = 0

    for line in puzzle_input_file:
        line = line.replace('\n', '')
        if not line:
            break
        couple = line.split('|')
        #print(couple)
        if couple[0] in rules_dict:
            rules_dict[couple[0]].append(couple[1])
        else:
            rules_dict[couple[0]] = [couple[1]]

    for line in puzzle_input_file:
        line = line.replace('\n', '')
        pages = line.split(',')
        already_seen = {}
        correct = True
        print(pages)
        for i in range(0, len(pages)):
            l = rules_dict.get(pages[i], None)
            if l is not None:
                for c in l:
                    c_index = already_seen.get(c, None)
                    if c_index is not None:
                        tmp = pages[i]
                        pages[i] = c
                        pages[c_index] = tmp
                        print("   {0}".format(pages))
                        result = result + int(pages[len(pages) // 2])
                        correct = False
                        break
            if not correct:
                break
            already_seen[pages[i]] = i
    print(result)

part2()