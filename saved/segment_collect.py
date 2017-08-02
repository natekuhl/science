import re


with open('generated_dot/clean_patched_graph11.dot') as f:
    lines = f.readlines()
    segments = []
    for line in lines:
        line = re.sub(';', '', line)
        line = re.sub('"', '', line)
        segments.append(line)
segments = [x.strip().split(" -- ") for x in segments]


print(segments)



