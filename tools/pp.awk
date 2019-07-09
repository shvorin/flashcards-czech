#!/usr/bin/awk -f

BEGIN {
# for historical reason the separator is comma
    FS = ", "
    srand()
}
{
    if (NF != 4)
        next

    src_idx = get_src_idx()
    n = split($src_idx, array, " / ")
    if (n == 1)
        src = $src_idx
    else
        # take any
        src = array[rand_n(n)]

    for(dst_idx = 1; dst_idx <= 4; ++dst_idx) {
        if(dst_idx == src_idx)
            continue
        if($dst_idx == "_")
            continue
        left = "put <" src "> into " dst_idx
        n = split($dst_idx, array, " / ")
        if (n == 1)
            right = $dst_idx
        else {
            left = left " (" n " variants)"
            # NB: Quizlet uses comma for unsorted variants
            right = join(", ", n, array)
        }
        printf("%s\t%s\n", left, right)
    }
}

function get_src_idx() {
    i = rand_n(4)
    i0 = i
    while($i == "_") {
        i = i + 1
        if (i == i0)
            next
        if (i > 4)
            i = 1
    }
    return i
}

# picks a random integer from {1, ..., n}
function rand_n(n) {
    res = int(rand() * n) + 1
    if (res < 1 || res > n)
        # WTF?
        res = 1

    return res
}

function join(sep, n, array) {
    res = array[1]
    for(i = 2; i <= n; ++i)
        res = res sep array[i]

    return res
}
