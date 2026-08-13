def split_string(s):
    mid = len(s) // 2
    left = s.rfind(" ", 0, mid)  # last space before mid, or -1
    right = s.find(" ", mid)  # first space at/after mid, or -1

    if left == -1 and right == -1:  # only 1 word
        return s
    elif left == -1:
        i = right
    elif right == -1:
        i = left
    else:
        i = left if (mid - left) <= (right - mid) else right

    return s[:i] + "\n" + s[i + 1 :]
