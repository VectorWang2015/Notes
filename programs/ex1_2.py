"""
| space 1 | space 2 | space 3 |
|---------+---------+---------|
| a       | d       | g       |
| b       | e       | h       |
| c       | f       | i       |
| *       | *       | *       |
"""
all_nodes_name = []


def parse_name(name):
    return name.split("_")


def generate_name(params):
    name = ""
    for param in params:
        name += "_"
        name += param

    # remove the "_" at the begining
    return name[1:]


def is_direct_child(father_name, child_name):
    cnt = 0
    father_params = parse_name(father_name)
    child_params = parse_name(child_name)

    for i in range(len(father_name)):
        if father_params[i] == "*" and child_params[i] != "*":
            cnt += 1
        elif father_params[i] != child_params[i]:
            return False

    if cnt == 1:
        return True
    else:
        return False


def is_child(father_name, child_name):
    cnt = 0
    father_params = parse_name(father_name)
    child_params = parse_name(child_name)

    for i in range(len(father_params)):
        if father_params[i] == "*" and child_params[i] != "*":
            cnt += 1
        elif father_params[i] != child_params[i]:
            return False

    if cnt > 0:
        return True
    else:
        return False


def list_children(father_name):
    father_params = parse_name(father_name)
    space1 = ['*','a','b','c']
    space2 = ['*','d','e','f']
    space3 = ['*','g','h','i']
    if father_params[0] != '*':
        space1 = [father_params[0],]
    if father_params[1] != '*':
        space2 = [father_params[1],]
    if father_params[2] != '*':
        space3 = [father_params[2],]

    children = []
    for i in space1:
        for j in space2:
            for k in space3:
                children.append(generate_name((i,j,k)))
    children.remove(father_name)
    return children


def init_all_nodes_name():
    global all_nodes_name
    space1 = ['*','a','b','c']
    space2 = ['*','d','e','f']
    space3 = ['*','g','h','i']
    for i in space1:
        for j in space2:
            for k in space3:
                all_nodes_name.append(generate_name((i,j,k)))


def count_recursively(candidates, k):
    if k==0 or len(candidates)==0:
        return 0
    head_element = candidates[0]
    new_candi = candidates[1:]
    rm_candi = list_children(head_element)
    for candi in rm_candi:
        if candi in new_candi:
            new_candi.remove(candi)
    # nums with the head element
    # without the head element
    # or null
    return count_recursively(candidates[1:], k) + count_recursively(new_candi, k-1) + 1


def count_k(candidates, k):
    # 1 for NULL
    return count_recursively(candidates, k)+1


def main():
    global all_nodes_name
    init_all_nodes_name()
    for i in range(15):
        num = count_k(all_nodes_name, i)
        print("{} elements, {} patterns".format(i, num))


if __name__ == "__main__":
    main()
