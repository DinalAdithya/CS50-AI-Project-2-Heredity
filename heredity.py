import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def calculate_inheritance(gene_count):
    """The function considers the probability of mutation and applies different rules
        depending on whether the person has zero, one, or two copies of the gene"""
    if gene_count == 2:
        return 1 - PROBS["mutation"]
    elif gene_count == 1:
        """Mutations are not considered here because the inherent chance 
                    of passing the gene is already balanced at 50%"""
        return 0.5
    else:
        return PROBS["mutation"]


def joint_probability(people, one_gene, two_genes, have_trait):

    gene_count = {}

    for person in people:
        if person in one_gene:
            gene_count[person] = 1
        elif person in two_genes:
            gene_count[person] = 2
        else:
            gene_count[person] = 0

    joint_prob = 1

    for person, info in people.items():
        mother = info["mother"]
        father = info["father"]

        if mother is not None and father is not None:  # parants listed

            prob_mother = calculate_inheritance(gene_count[mother])
            prob_father = calculate_inheritance(gene_count[father])
            
            if gene_count[person] == 2:
                prob_person = prob_mother * prob_father
            elif gene_count[person] == 1:
                prob_person = prob_mother * (1 - prob_father) + (1 - prob_mother) * prob_father
            else:
                prob_person = (1 - prob_mother) * (1 - prob_father)
        else:
            prob_person = PROBS["gene"][gene_count[person]] # no parents listed

        # adjusts probability of a person based on they have trait or not
        if person in have_trait:
            prob_person *= PROBS["trait"][gene_count[person]][True]
        else:
            prob_person *= PROBS["trait"][gene_count[person]][False]

        joint_prob = joint_prob * prob_person

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):


    for person in probabilities:
        if person in one_gene:
            gene_count = 1
        elif person in two_genes:
            gene_count = 2
        else:
            gene_count = 0

        has_trait = person in have_trait

        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        tot_val = 0

        for key in probabilities[person]["gene"]:
            tot_val += probabilities[person]["gene"][key]# get all probabilities and add them togather

        for key in probabilities[person]["gene"]:
            probabilities[person]["gene"][key] /= tot_val # divide all probabilities by that added value


        tot_val_trait = probabilities[person]["trait"][True] + probabilities[person]["trait"][False] # get both probabilities and add them togather
        probabilities[person]["trait"][True] /= tot_val_trait # divide each probability by that added value
        probabilities[person]["trait"][False] /= tot_val_trait # divide each probability by that added value



if __name__ == "__main__":
    main()
