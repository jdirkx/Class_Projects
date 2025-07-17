"""
Script created for UO's LING415/Semantics course
Takes XMLs from folder in wd (as downloaded from MICASE website via bs4) -> 
finds 10x instances of 'because/since' in each and appends context + metadata
for environment/semantic analysis
"""

import xml.etree.ElementTree as ET
import os
import csv
import re

DIR = 'XMLs' #Assumes existence of directiry in cwd 'XMLs' - this is created by MICASE_Webscraper.py or manually
OUTPUT_FILE = 'LING415_HW3_Data.csv'

def write_to_csv(file_name, **kwargs):

    try:
        with open(file_name, 'r') as f:
            has_header = f.readline() != ''
    except FileNotFoundError:
        has_header = False

    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=kwargs.keys())
        if not has_header:
            writer.writeheader()
        writer.writerow(kwargs)

def extract_context(text, keyword, before=3, after=3):
    "Extracts environment form occurs in"
    words = re.split(r'\s+', text)
    matches = []
    for idx, word in enumerate(words):
        if word.lower() == keyword:
            start = max(0, idx - before)
            end = min(len(words), idx + after + 1)
            context = ' '.join(words[start:end])
            matches.append(context)
    return matches

def process_utterance(utterance, output_file, filename, text_type, interactivity, counter):
    "Extracts data/metadata associated with occurnence of form"
    sp_status = utterance.attrib.get('NSS', 'NA')
    text = utterance.text.strip() if utterance.text else ''

    for keyword in ['because', 'since']:
        contexts = extract_context(text, keyword)
        for context in contexts:
            if counter <= 0:
                return counter
            write_to_csv(output_file,
                         filename=filename,
                         keyword=keyword,
                         context=context,
                         speaker_status=sp_status,
                         text_type=text_type,
                         interactivity=interactivity)
            counter -= 1
    return counter

def parseXML(xmlfile, filename, output_file):
    "Parses a single file in XMLs directory"
    try:
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        text_type = root.find('.//TERM[@TYPE="SPEECHEVENT"]').text or 'NA'
        interactivity = root.find('.//TERM[@TYPE="INTERACTIVITYRATING"]').text or 'NA'

        counter = 10
        for utterance in root.findall('.//BODY/*'):
            if counter <= 0:
                break
            if utterance.tag.startswith('U') and utterance.text:
                counter = process_utterance(utterance, output_file, filename, text_type, interactivity, counter)

        print(f'Processed file: {filename}')
    except ET.ParseError as e:
        print(f"Parse error in file {filename}: {e}")

def main():

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    for filename in os.listdir(DIR):
        filepath = os.path.join(DIR, filename)
        if os.path.isfile(filepath) and filename.endswith('.xml'):
            parseXML(filepath, os.path.splitext(filename)[0], OUTPUT_FILE)

    print(f'Results written to {OUTPUT_FILE}')

if __name__ == '__main__':
    main()