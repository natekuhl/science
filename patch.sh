#!/bin/bash


sed -e "/^\tinsert_patch_here;$/ {
    r ./patch.txt
    d
}" $DOT_FILE > ./generated_dot/generated_${DOT_FILE}












