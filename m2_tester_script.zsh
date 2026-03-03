#!/usr/bin/env zsh

python m1_tester.py > m1_tester_output.txt
python m1_tester_new.py > m1_tester_new_output.txt


# add remove & extended test cases
rm -rf CT M2 MT ECS165 && python m2_extended.py > m2_extended_output.txt
rm -rf CT M2 MT ECS165 && python m2_tester_part1.py > mt2_tester_part_1_output.txt
python m2_tester_part2.py > mt2_tester_part_2_output.txt