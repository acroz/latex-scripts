#!/usr/bin/env python

import sys
import re

if len(sys.argv) < 2:
    print('Usage: {} TEXFILE [TEXFILE [...]]'.format(sys.argv[0]))
    sys.exit(1)

# Define a regular expression matching all possible cite commands
regex = re.compile(r'\\(?:my)?cite[pt]?\{(\S+?)\}')

# Define a regex matching a placeholder in a potential citation macro definition
placeholder = re.compile(r'#\d')

# Data structure to store citation counts
count = {}
total = 0

# Process all files on command line
for fname in sys.argv[1:]:

    # Parse this file
    with open(fname) as fp:
        for line in fp:

            # Skip commented lines
            if line.lstrip().startswith('%'):
                continue

            # Loop over all matches of citation command
            for match in regex.findall(line):

                # Skip placeholders
                if placeholder.match(match):
                    continue
                
                # Split up multiple references
                for ref in match.split(','):

                    # Clean any whitespace
                    ref = ref.strip()
                    
                    # Increment counter for this reference
                    try:
                        count[ref] += 1
                    except KeyError:
                        count[ref] = 1
                    
                    # Increment total counter
                    total += 1

# Find out the length of the longest reference
extras = ['Citation Key', 'Unique References', 'Total Citations']
maxlen = max([len(k) for k in count.keys()] + [len(s) for s in extras])

# Construct a pattern for output
pattern = '{:' + str(maxlen) + 's} {:>5}'
sep = pattern.format('=' * maxlen, '=====')


# Print the report

# Header
print(sep)
print(pattern.format('Citation Key', 'Count'))
print(sep)

# Reference counts
# Sort by frequency, then alphabetically
for ref, c in sorted(sorted(count.items()), key=lambda e: e[1]):
    print(pattern.format(ref, c))
print(sep)

# Summary stats
print(pattern.format('Unique References', len(count)))
print(pattern.format('Total Citations', total))
print(sep)
