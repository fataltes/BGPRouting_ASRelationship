from validator import Validator

class Relationship_finder:
    def __init__(self, as_file):
        self.as_dic = {}
        self.as_paths = [] # a list of all paths of ASes. Each path is itself a list of ASes in the same order they were traced
        self.transit = []
        self.degree = {}
        self.edge = {}
        self.as_max_in_path = []
        self.read(as_file)
        #print self.as_paths

    """
    Reads output file containing the sequence of ASes and creates a list of paths seen among those ASes
    """
    def read(self, as_file):
        temp_ases = {}
        path_dic = {}
        f = open(as_file)
        as_cntr = 0
        for line in f:
            line_splitted=line.split()
            if len(line_splitted) > 0:
                path = []
                key = ''
                for part in line_splitted:
                    if part.lower().startswith("as"):
                        if part.lower() not in temp_ases:
                            temp_ases[part.lower()] = as_cntr
                            as_indx = as_cntr
                            as_cntr += 1
                        else:
                            as_indx = temp_ases[part.lower()]
                        self.as_dic[as_indx] = part.lower()
                        key = key + "_" + str(as_indx)
                        path.append(as_indx)
                # remove duplicates
                if key not in path_dic:
                    self.as_paths.append(path)
                    path_dic[key] = 1
        print "num of path : " + str(len(self.as_paths))
        print "num of ASes : " + str(len(self.as_dic))

    """
    Computes degree of each AS
    Degree of each AS is the number of ASes connected to that AS (either way, in and out)
    """
    def compute_degree(self):
        neighbor = {}
        # I just used dic to implement set!
        # Each AS in the neighbor has a dictionary of its neighbors!
        for path in self.as_paths:
            for i in range(len(path)-1):
                if path[i] not in neighbor:
                    neighbor[path[i]] = {}
                if path[i+1] not in neighbor:
                    neighbor[path[i+1]] = {}
                neighbor[path[i]][path[i+1]] = 1
                neighbor[path[i+1]][path[i]] = 1
        for key in neighbor:
            self.degree[key] = len(neighbor[key])

    """
    Computes transit
    """
    def compute_transit(self):
        self.transit = [[0 for j in range(len(self.as_dic))] for i in range(len(self.as_dic))]
        for path in self.as_paths:
            # First find index of AS with maximum degree in the path
            # And save it for future use (finding peer to peer relationships)
            as_max_index = ""
            as_max_degree = 0
            for i in range(len(path)):
                if self.degree[path[i]] > as_max_degree:
                    as_max_index = i
                    as_max_degree = self.degree[path[i]]
            self.as_max_in_path.append(as_max_index)
            # For all pairs (i, i+1) appear before the AS with max degree, (i+1) transits data for (i)
            if as_max_index > 0:
                for i in range(as_max_index - 1): # Last transit says (as_max) transits data for (as_max-1)
                    self.transit[path[i]][path[i+1]] = 1
            # For all pairs (i, i+1) appear after the AS with max degree, (i) transits data for (i+1)
            if as_max_index < len(path):
                for i in range(as_max_index, len(path)-1):
                    self.transit[path[i+1]][path[i]] = 1 # First transit says (as_max+1) transits data for (as_max)

    """
    Compute relationships
    """
    def assign_relationships(self):
        # Assign Sibling2Sibling and Provider2Customer Relationships
        for as_1 in self.as_dic:
            for as_2 in self.as_dic:
                #print str(as_1) + "," + str(as_2)
                if as_1 not in self.edge:
                    self.edge[as_1] = {}
                if self.transit[as_1][as_2] == 1 and self.transit[as_2][as_1] == 1:
                    self.edge[as_1][as_2] = "s2s"
                elif self.transit[as_2][as_1] == 1:
                    self.edge[as_1][as_2] = "p2c"
                #elif self.transit[as_2][as_1] == 1:
                #    self.edge[as_1][as_2] = "c2p"

        # Assign Peer2Peer Relationships
        # I've changed some parts because I thought it's not correct (We should discuss it together)
        # We can change it to a simpler implementation.
        # But I just implemented the same as in paper for the sake of trusteeship
        not_peering = [[0 for j in range(len(self.as_dic))] for i in range(len(self.as_dic))]
        path_counter = 0
        for path in self.as_paths:
            j = self.as_max_in_path[path_counter]
            for i in range(j-2):
                not_peering[path[i]][path[i+1]] = 1
            for i in xrange(j+1, len(path)-1):
                not_peering[path[i]][path[i+1]] = 1
            if j-1 >= 0 and j+1 < len(path) and path[j] in self.edge[path[j-1]] and path[j+1] in self.edge[path[j]]:
                if self.edge[path[j-1]][path[j]] == "s2s" and self.edge[path[j]][path[j+1]] != "s2s":
                    not_peering[path[j]][path[j+1]] = 1
                elif self.edge[path[j-1]][path[j]] != "s2s" and self.edge[path[j]][path[j+1]] == "s2s":
                    not_peering[path[j-1]][path[j]] = 1
                else:
                    if self.degree[path[j-1]] > self.degree[path[j+1]]:
                        not_peering[path[j]][path[j+1]] = 1
                    else:
                        not_peering[path[j-1]][path[j]] = 1
            path_counter += 1
        for path in self.as_paths:
            for j in range(len(path)-1):
                if not_peering[path[j]][path[j+1]] != 1:
                    max_degree = max(self.degree[path[j]], self.degree[path[j+1]])
                    min_degree = min(self.degree[path[j]], self.degree[path[j+1]])
                    if max_degree/min_degree < 2:
                        self.edge[path[j]][path[j+1]] = "p2p"
                        self.edge[path[j+1]][path[j]] = "p2p"

    """
    Print relationships
    """
    def print_relationships(self):
        print "\n****** RELATIONSHIPS ******"
        for as_1 in self.as_dic:
            if len(self.edge[as_1]) > 0:
                print str(as_1) + ": " + str(self.edge[as_1])
        print "***************************\n\n\n"


"""
MAIN
"""
relationship_finder = Relationship_finder('data/output')
relationship_finder.compute_degree()
relationship_finder.compute_transit()
relationship_finder.assign_relationships()
relationship_finder.print_relationships()
validor = Validator('data/20160401.as-rel.txt')
validor.validate(relationship_finder.edge, relationship_finder.as_dic)