#!python

import pandas
import glob
import os
import argparse
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default='sample_names.csv', help="the name of the mapping file left behind by gpas-uploader or the Electron Client.")
    parser.add_argument("--output", default='results.csv.gz', help="the name of the output CSV file")
    options = parser.parse_args()

    # this CSV let's us map from local UID to GPAS UID
    sample_names = pandas.read_csv(options.input)

    # as long as the filenames only contain a single underscore, we can find the stem which contains metatdata when testing
    def find_stem(row):
        return(row['local_sample_name'].split('_')[0])

    sample_names['filestem'] = sample_names.apply(find_stem, axis=1)

    def find_characteristics(row):

        cols = row['filestem'].split('-')

        snps = int(cols[4].split('snps')[0])
        depth = int(cols[5].split('d')[0])
        error = float(cols[6].split('e')[0])

        if cols[7][0] == 'a':
            dropped_amplicons = cols[7]
            repeat = int(cols[8].split('.fasta')[0])
        else:
            dropped_amplicons = None
            repeat=int(cols[7].split('.fasta')[0])

        return pandas.Series([cols[0], cols[1], cols[2][1:], cols[3], snps, depth, error, dropped_amplicons, repeat])

    sample_names[['tech', 'primer_scheme', 'target_lineage', 'lineage_definition', 'snps', 'depth', 'error', 'dropped_amplicons', 'repeat']] = sample_names.apply(find_characteristics,axis=1)

    def read_fasta(filename):

        if os.path.exists(filename):
            INPUT = open(filename, 'r')
            INPUT.readline()
            genome=''
            for i in INPUT:
                genome += i.rstrip()
        else:
            print(filename+ " does not exist! Check you have gunzipped the downloaded FASTA files.")
            genome = ''

        return(genome)

    def compare_genomes(row):

        in_genome = read_fasta(row['filestem'] + '.fasta')
        out_genome = read_fasta(row['local_sample_name'] + '.fasta')

        # only mark as correctly assembled if the length of the output string is >29000 and it is found in the input string
        match = out_genome in in_genome
        length = True if len(out_genome) > 29000 else False
        result = match and length

        return(pandas.Series([result, len(in_genome), len(out_genome), in_genome, out_genome]))

    sample_names[['assembled_correct', 'len_in', 'len_out', 'in_genome', 'out_genome']]=sample_names.apply(compare_genomes,axis=1)

    print("Assembled correctly:\n", sample_names.assembled_correct.value_counts())

    def read_pango(row):

        json_file =row['local_sample_name'] + '.json'

        if os.path.exists(json_file):

            INPUT = open(json_file, 'r')
            a = json.load(INPUT)

            pango_lineage = a[row['gpas_sample_name']]['pango']['lineage']
            pango_conflict = a[row['gpas_sample_name']]['pango']['conflict']
            aln2type_lineage = list(a[row['gpas_sample_name']]['aln2type'].keys())[0]
            scorpio_call = a[row['gpas_sample_name']]['pango']['scorpio_call']
            scorpio_conflict = a[row['gpas_sample_name']]['pango']['scorpio_conflict']

            return pandas.Series([pango_lineage, pango_conflict, scorpio_call, scorpio_conflict, aln2type_lineage])

        else:

            return pandas.Series([None, None, None, None, None])

    sample_names[['pango_lineage', 'pango_conflict', 'scorpio_call', 'scorpio_conflict', 'aln2type_label']] = sample_names.apply(read_pango, axis=1)
    print()
    print("Do we recover the target_lineage?")
    print(pandas.crosstab(sample_names.target_lineage, sample_names.pango_lineage))

    sample_names.to_csv(options.output, index=False)
