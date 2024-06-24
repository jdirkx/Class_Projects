"""Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2023.
Author:  Jacob Dirkx
Credits: Myself
"""
import doctest
import csv


def read_csv_column(path: str, field: str) -> list[str]:
    """Reads strings from "Majors" column in CSV file into a list 
    """
    major_list=[]
    with open(path,"r") as roster:
        reader=csv.DictReader(roster)
        for line in reader:
            major=line[field]
            major_list.append(major)
    return(major_list)

def counts(major_list: list[str]) -> dict[str, int]:
    """Creates dict with majors and # of times each appears
    """
    M_Counts={}
    for line in major_list:
        if line in M_Counts:
            M_Counts[line]+=1
        else:
            M_Counts[line]=1
    return(M_Counts)

def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]:
    """Read a CSV with column headers into a dict for major codes and their full names.
    """
    programcodes={}
    with open(path,"r") as programlist:
        reader=csv.DictReader(programlist)
        for line in reader:
            key_field=line["Code"]
            value_field=line["Program Name"]
            programcodes[key_field]=value_field
        return(programcodes)

def items_v_k(major_counts:dict) -> dict[int,str]:
    """Creates new list of majors sorted by number enrolled
    """
    by_count = []
    for code, count in major_counts.items():
        pair = (count, code)
        by_count.append(pair)
    return by_count

def main():
    doctest.testmod()
    majors=read_csv_column("data/roster_selected.csv", "Major")
    major_counts=counts(majors)
    program_names=read_csv_dict("data/programs.csv", "Code", "Program Name")
    by_count = items_v_k(major_counts)
    by_count.sort(reverse=True)
    for count, code in by_count:
        program = program_names[code]
        print(count, program)

if __name__ == "__main__":
    main()