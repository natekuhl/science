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


# Insert patch mappings

sed -i -e "/insert_patch_here;/ {
    r ./patch.txt
    d
}" ./generated_dot/${dot_file} 


# Unflatten and build PNG graph

unflatten -l100 -f -o ./generated_dot/unflattened_${dot_file} ./generated_dot/${dot_file}

dot -Gdpi=3750 -Gsize=9,15\! -Tpng ./generated_dot/unflattened_${dot_file} -o img/${png_file}
