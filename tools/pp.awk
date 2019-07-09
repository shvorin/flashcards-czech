#!/usr/bin/awk -f
# FIXME: vanilla awk may not have rand(); nawk, gawk, etc to be used instead

BEGIN {
    srand()
    # for historical reason the separator is comma
    FS = ", "
    form_names[1] = "infinitiv"
    form_names[2] = "3.os.jed.č."
    form_names[3] = "rozkaz"
    form_names[4] = "minulý"
}
{
    if(NF != 4)
        next

    nForms = 0
    for(i = 1; i <= 4; ++i) {
        if($i == "_")
            continue
        ++nForms
        form_indices[nForms] = i
    }

    if(nForms <= 1) {
        delete form_indices
        next
    }

    for(j in form_indices) {
        dst_idx = form_indices[j]
        i = rand_n(nForms - 1)
        if(i >= j)
            ++i
        src_idx = form_indices[i]
        # NB: here src_idx is randomly picked not equal to dst_idx

        nVars = split($src_idx, array, " / ")
        if(nVars == 1)
            src = $src_idx
        else
            # take any
            src = array[rand_n(nVars)]

        left = src " |" form_names[dst_idx] ">"
        nVars = split($dst_idx, array, " / ")
        if(nVars == 1)
            right = $dst_idx
        else {
            left = left " (" nVars " variants)"
            # NB: Quizlet uses comma for unsorted form_indices
            right = join(", ", nVars, array)
        }
        printf("%s\t%s\n", left, right)
    }

    delete form_indices
}

# picks a random integer from {1, ..., n}
function rand_n(n) {
    res = int(rand() * n) + 1
    if(res < 1 || res > n)
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
