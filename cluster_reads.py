#!/usr/bin/env python

import sys

# Check that the correct number of command-line arguments was provided
if len(sys.argv) not in [2, 3]:
  # If not, print usage message and exit
  print("Usage: python cluster_reads.py <cluster_size> [--same-strand] < input.bed > output.bed")
  sys.exit(1)

# Check if the --same-strand flag was provided
if len(sys.argv) == 3 and sys.argv[2] == "--same-strand":
  same_strand = True
else:
  same_strand = False

# Set cluster size
cluster_size = int(sys.argv[1])

# Initialize variables
current_chrom = ""
current_cluster = 0
cluster_start = 0
cluster_end = 0
current_strand = ""

# Read input BED file from standard input
for line in sys.stdin:
  # Parse fields from line
  fields = line.strip().split()
  chrom = fields[0]
  start = int(fields[1])
  end = int(fields[2])
  strand = fields[5]

  # Check if line is from a new chromosome or strand
  if chrom != current_chrom or (same_strand and strand != current_strand):
    # If so, reset cluster and start a new cluster with this line
    current_cluster += 1
    cluster_start = start
    cluster_end = end
    current_chrom = chrom
    current_strand = strand
  else:
    # If line is from the same chromosome and strand (if applicable), check if it is within cluster_size bp of the current cluster
    if start <= cluster_end + cluster_size:
      # If so, extend cluster to include this line
      cluster_end = end
    else:
      # If not, start a new cluster with this line
      current_cluster += 1
      cluster_start = start
      cluster_end = end

  # Print line with cluster number added
  print("{}\t{}\t{}\t{}\t{}\t{}".format(chrom, start, end, fields[3], current_cluster, strand))
