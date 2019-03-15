# flashcards-czech
Cards for flashcard services like quizlet.com or memrise.com; this repo contains Czech language cards. 

## Flashcard format
...TODO

## Isomorphisms
The idea is to find isomorphic subset in Czech and Russian respectively. The main sources of isomorphism are:
 1. verb tenses
 2. (pro)noun declination
 3. ...

However, there are some cases of broken isomorphisms:
 * Homonyms. For example, _vidí_ represents two forms. To cope with it, it is possible to expoit flashcard application feature to give extra information in parenthesis:
> vidí (jed. č.) — видит

> vidí (mn. č.) — видят

In both cases the correct answer would be "vidí", no need to type parenthetic stuff.
 * Synonyms. For example, _mohu, můžu_ are two versions of the same form. FIXME: it is unclear what to do in such case, maybe do not include them into "isomorphic" sets.
 * Non-existing forms. Such forms should be dropped.
