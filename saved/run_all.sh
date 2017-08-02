#!/bin/bash


# SET DOT FILE NAME
dot_file='graph11.dot'


# SET PNG GRAM NAME 
png_file='graph11.png'


##############################
##############################
##############################


# Build dot graph

python organize.py ${dot_file}


# Copy patch mappings into a more readable format

#sed 's/\/\*.*\*\///g' patch.txt > ./generated_dot/clean_patch.txt
#
#sed -i -e '/^\s*$/d' ./generated_dot/clean_patch.txt
#
#sed -i -e '/^\/\/.*$/d' ./generated_dot/clean_patch.txt


# Insert patch mappings

sed -e "/insert_patch_here;/ {
    r ./generated_dot/clean_patch.txt
    d
}" ./generated_dot/${dot_file} > ./generated_dot/patched_${dot_file}


# Build a separate composite patch file without the dot syntax

#sed '/^.*[{}].*$/d' ./generated_dot/patched_${dot_file} > ./generated_dot/clean_patched_${dot_file}


# Unflatten and build PNG graph

unflatten -l100 -f -o ./generated_dot/unflattened_${dot_file} ./generated_dot/patched_${dot_file}

dot -Gdpi=3750 -Gsize=9,15\! -Tpng ./generated_dot/unflattened_${dot_file} -o img/${png_file}
