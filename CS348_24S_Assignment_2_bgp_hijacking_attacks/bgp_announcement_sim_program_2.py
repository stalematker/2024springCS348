# Copyright (C) 2024 Min Suk Kang
# All rights reserved.
#
# This simulator script is proprietary and intended for educational use only. It is provided 
# to undergraduate students at KAIST solely for use in the course CS348. By using this 
# simulator, students agree to adhere to the university's academic integrity guidelines 
# and not to share, distribute, copy, modify, or use this simulator outside of the designated 
# course activities.
#
# Unauthorized sharing or distribution of this software, or any part of it, is not allowed 
# and may be subject to academic disciplinary actions. Please respect the terms of use.
#
# For additional permissions or inquiries, please contact minsukk@kaist.ac.kr.

import sys, hashlib, re, random
from copy import deepcopy

providers = dict()
customers = dict()
peers = dict()
neighbors = dict()
asns = set()
tier1 = set()
tier2 = set()
tier3 = set()
rpki_db = {}

def classify_asn():
    global tier1, tier2, tier3
    for asn in asns:
        if asn not in customers:
            tier3.add(asn)
        elif asn not in providers:
            tier1.add(asn)
        else:
            tier2.add(asn)

def generate_graph_from_caida_file(date):
    global customers, providers, peers, neighbors
    with open(str(date) + ".as-rel.txt", 'r') as f:

        for line in f:
            if line.startswith("#"):
                continue
            segs = line.split('|')
            asn1 = int(segs[0])
            asn2 = int(segs[1])
            rel = int(segs[2])

            # add to asns
            asns.add(asn1)
            asns.add(asn2)

            # asn2 is a customer of asn1
            if rel == -1:
                # initialize if needed
                if asn1 not in customers:
                    customers[asn1] = set()
                # add asn2 
                customers[asn1].add(asn2)

                # initialize if needed
                if asn2 not in providers:
                    providers[asn2] = set()
                # add asn1 
                providers[asn2].add(asn1)

            # asn1 is a peer
            if rel == 0:
                # initialize if needed
                if asn1 not in peers:
                    peers[asn1] = set()
                # add asn2 
                peers[asn1].add(asn2)

                # initialize if needed
                if asn2 not in peers:
                    peers[asn2] = set()
                # add asn1 
                peers[asn2].add(asn1)

            # initialize if needed
            if asn1 not in neighbors:
                neighbors[asn1] = set()
            neighbors[asn1].add(asn2)
            # initialize if needed
            if asn2 not in neighbors:
                neighbors[asn2] = set()
            neighbors[asn2].add(asn1)

def get_rel(asn, prev_asn):
    if prev_asn in customers.get(asn, []):
        return 1
    elif prev_asn in peers.get(asn, []):
        return 0
    elif prev_asn in providers.get(asn, []):
        return -1
    else:
        return 

def get_cheaper_path(asn, path1, path2):
    prev_asn1 = path1[-1]
    prev_asn2 = path2[-1]
    rel1 = get_rel(asn, prev_asn1)
    rel2 = get_rel(asn, prev_asn2)
    # if prev_asn1 == prev_asn2:
    #     return get_cheaper_path(prev_asn1, path1[:-1], path2[:-1]) + [prev_asn1]
    #compare rel
    if rel1 > rel2:
        return path1
    elif rel2 > rel1:
        return path2
    else:
        #compare len
        if len(path1) < len(path2):
            return path1
        elif len(path1) > len(path2):
            return path2
        else:
            #compare hash
            hash1 = int(hashlib.sha1(str(path1[-1]).encode()).hexdigest(), 16)
            hash2 = int(hashlib.sha1(str(path2[-1]).encode()).hexdigest(), 16)
            return path1 if hash1 < hash2 else path2


def simulate_bgp(dest_prefix_pairs):
    global providers, customers, peers, asns, tier1, tier2, tier3, asns_list

    # initialize the global bgp_table[asn][prefix] = [path]
    bgp_table = dict()

    for dest, prefix, default_path in dest_prefix_pairs:
        # initialize the tick and the queue
        tick = 0
        queue = dict()
        future_queue = dict()

        # print overview of (dest, prefix)
        print("dest (", dest, ") annonces prefix (", prefix, ")")

        # simulate BGP updates from dest to all ASes until convergence
        while True:
            # initialize for each tick
            num_updates = 0
            future_queue = dict()

            # initial update from dest
            if tick == 0:
                for neighbor in neighbors[dest]:
                    # path is defined as [prefix, asn1, asn2, ...]
                    path = list()
                    path.append(prefix)
                    path.extend(default_path)
                    if neighbor not in future_queue:
                        future_queue[neighbor] = list()
                    future_queue[neighbor].append(path)
                    num_updates = num_updates + 1

            # loop for all ASes
            for asn in asns:

                # if queue is empty, then skip
                if asn not in queue or len(queue[asn]) == 0:
                    continue

                # if queue has some updates (from last tick), process them!
                for path in queue[asn]:
                    # debug: print asn and queue[asn]
                    # print("DEBUG: ", asn, queue[asn])

                    will_propagate = False

                    if asn in tier1:
                        origin_as = path[1]
                        authorized_prefixes = rpki_db.get(origin_as, [])
                        if prefix not in authorized_prefixes:
                            continue

                    # Check if the ASN exists in the bgp_table
                    if asn not in bgp_table:
                        bgp_table[asn] = {prefix: path}  # Add new ASN and prefix with its path
                        will_propagate = True
                    else:
                        # Check if the prefix exists for this ASN
                        if prefix not in bgp_table[asn]:
                            bgp_table[asn][prefix] = path  # Add new prefix with its path under the existing ASN
                            will_propagate = True
                        else:                            
                            existing_path = bgp_table[asn][prefix]
                            # if existing next asn is the same as the new one, ignore
                            if existing_path == path:
                                continue

                            # if the new path is cheaper, update it
                            cheaper_path = get_cheaper_path(asn, existing_path, path)
                            if cheaper_path == path:
                                bgp_table[asn][prefix] = path
                                will_propagate = True

                    # propagate (update) to other ASes
                    if will_propagate:
                        incoming_asn = path[-1]
                        path_to_update = deepcopy(path)
                        path_to_update.append(asn)
                        if incoming_asn in customers.get(asn, []): # TASK 1
                            for neighbor in neighbors.get(asn, []): # TASK 1
                                if neighbor == incoming_asn: 
                                    continue
                                if neighbor not in future_queue:
                                    future_queue[neighbor] = list()
                                future_queue[neighbor].append(path_to_update)
                                num_updates = num_updates + 1
                        else:
                            if incoming_asn in peers.get(asn, []) or incoming_asn in providers.get(asn, []): # TASK 1
                                for customer in customers.get(asn, []):
                                    if customer == incoming_asn:
                                        continue
                                    if customer not in future_queue:
                                        future_queue[customer] = list()
                                    future_queue[customer].append(path_to_update)
                                    num_updates = num_updates + 1

            # print summary of this tick
            print("tick: ", tick, ", no of updates: ", num_updates)

            # deepcopy future_queue -> queue
            queue = deepcopy(future_queue)

            # if no updates (i.e., convergence), then end the loop
            if num_updates == 0:
                break

            # go to the next tick
            tick = tick + 1

        # end of the loop for (dest, prefix)
        print("end of announcment from dest (", dest, ") for prefix (", prefix, ")")

    # return the final result (bgp_table)
    return bgp_table
           
def write_to_file(bgp_table):
    # Open the file for writing
    with open("./bgp_table.txt", "w") as f:
        # Create a sorted list of all (asn, prefix) pairs
        sorted_entries = []
        for asn in bgp_table:
            for prefix in bgp_table[asn]:
                sorted_entries.append((asn, prefix))
        sorted_entries.sort()  # Sort the list by ASN first, then by prefix

        # Write each entry to the file
        for asn, prefix in sorted_entries:
            path = bgp_table[asn][prefix]

            # First element is the prefix, so remove it
            path = path[1:]

            # Convert path list to a string with relationships
            path_str = ''
            for i in range(len(path)-1):
                if path[i] in providers and path[i+1] in providers[path[i]]:
                    path_str += str(path[i]) + ">"
                elif path[i] in peers and path[i+1] in peers[path[i]]:
                    path_str += str(path[i]) + "-"
                elif path[i] in customers and path[i+1] in customers[path[i]]:
                    path_str += str(path[i]) + "<"
                else:  # should not happen
                    path_str += str(path[i]) + "?"
            path_str += str(path[-1])
            
            # Write the sorted ASN, prefix, and path to the file
            f.write(str(asn) + "\t" + prefix + "\t" + path_str + "\n")

def read_from_input_file(input_filename):
    asn_prefix_path_pairs = []  # Initialize an empty list to hold (ASN, prefix, path) tuples
    # Open and read the input file
    try:
        with open(input_filename, 'r') as file:
            for line in file:
                # Assuming each line contains 'ASN prefix'
                parts = line.strip()
                parts = re.split(r'\s+|\[|\]', parts)  # Split the line into parts on whitespace
                parts = [element for element in parts if element]
                default_path = []
                if len(parts) >= 2:  # Make sure there are at least two parts
                    asn, prefix = parts[0], parts[1]
                    if len(parts) == 2:
                        default_path = [int(asn)]  # Convert ASN to integer and put in a list
                    elif len(parts) > 2:
                        # Extract additional numbers as part of default_path
                        default_path = [int(p) for p in parts[2:]]  # Convert each to int
                    asn_prefix_path_pairs.append((int(asn), prefix, default_path))
        return asn_prefix_path_pairs
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        sys.exit(1)

def load_rpki_database(filename):
    global rpki_db
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')  # Assuming tab-separated values
            if len(parts) >= 2:
                asn, prefix = parts
                rpki_db[int(asn)] = rpki_db.get(int(asn), []) + [prefix]

def main(arg):
    input_filename = sys.argv[1]  # The input filename is the first command line argument

    # Initialize an empty list to hold (destination ASN, prefix) pairs
    asn_prefix_path_pairs = read_from_input_file(input_filename)

    print(asn_prefix_path_pairs)

    load_rpki_database('20240301.asn-prefix-database.txt')

    date = 20240301
    generate_graph_from_caida_file(date)
    classify_asn()
    print('total # ASes :', len(asns))
    asns_list = list(asns)


    print ("SIM START")

    bgp_table = simulate_bgp(asn_prefix_path_pairs)

    print("Write to file")
    write_to_file(bgp_table)

    print("SIM END")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bgp_announcement_sim_program_2.py bgp_announcement_list.txt")
        sys.exit(1)
    main(sys.argv[1])