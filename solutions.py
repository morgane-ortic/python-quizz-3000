# recursive 3
def print_with_o_upper(txt, index=0):
    if index == len(txt):
        return
    else:
        if txt[index] == 'o':
            print(txt[index].upper(), end='')
        else:
            print(txt[index], end='')
        print_with_o_upper(txt, index + 1)

txt = "Look, good code is almost like a good song"
print_with_o_upper(txt)