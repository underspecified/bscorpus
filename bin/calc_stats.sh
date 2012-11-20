#!/bin/bash

tr A-Z a-z < $< | \
sort -t'	' | \
uniq -c | \
sort -t'	' -nr
