from codonDict import codon_aa_dict
def findPromoter(sequence: str) -> int | None: 
    
    """
    Function:
        Find the index of the first promoter being "TATAAT"
    Parameter:
        sequence - the dna sequence
    Returns:
        the index where "TATAAT" starts or None
    """

    if len(sequence) == 0:
        return None
    for i in range(len(sequence) -5):
        if sequence[i:i+6] == "TATAAT":
            return i
    return None

def transcribe(sequence: str, promoter_index: int) -> str:

    """
    Function:
        Transcribe a DNA sequence into mRNA starting 16 x's after the start of the promoter
    Parameters:
        sequence - DNA sequence 
        promoter_index - the initial index of where the promoter DNA
    Returns:
        The mRNA sequence
    """
    
    start = promoter_index + 16 
    mrna = ""
   
    maps = {"A":"U", "T":"A", "C":"G", "G":"C"}
    for i in range(start, len(sequence)):
        mrna += maps[sequence[i]]
    return mrna 

def findStartCodon(mrna: str) -> int | None:
    """
    Function:
        Finds the index of the first AUG in the mRNA sequence 
    Parameter:
        mrna -  the mRNA sequence 
    Funtion:
        The index of the first AUG or None
    """
   
    if len(mrna) == 0:
        return None 

    for i in range(len(mrna) - 2):
        if mrna[i:i+3] == "AUG":
            return i 
    return None

def translate(mrna: str, start_codon_starts: int) -> str:
    """
    Function:
        Translates mRNA into a string of proteins after the AUG and stops after a stop codon (UAA UAG or UGA)
    Parameters:
        mrna - the mRNA
        start_codon_starts - The index of the AUG codon
    Returns:
        The sequence of amino acid
        """
    
    start = start_codon_starts + 3 
    final = ""

    for i in range(start, len(mrna) - 2, 3):
        codon = mrna[i:i+3]

        if codon == "UAA" or codon == "UAG" or codon == "UGA":
            return final

        if codon in codon_aa_dict:
            final += codon_aa_dict[codon]
        else:
            return final

    return final

def findMutations(wild_type: str, mutated: str) -> list[int]:
    """
    Function:
        Finds where there is a mutation in DNA 
    Parameters:
        wild_type - the original sequence
        mutated - the mutated DNA 
    Returns:
        A list of the index where there are different sequences i.e. mutations"""

    final = []
    diff = ""
    
    if len(wild_type) < len(mutated):
        limit = len(wild_type)
    else:
        limit = len(mutated)
    for i in range(limit):
        if wild_type[i] != mutated[i]:
            final.append(i)
            diff += "*"
        else:
            diff += " "

    print(wild_type)
    print(diff)
    print(mutated)
    return final 

def readFASTAFile(fasta_filename: str) -> list[str]:
    """
    Function:
        reads a file and returns a list of DNA from the file 
    Parameter:
        fasta_filename - the file name 
    Returns:
        A list of DNA sequences from the file 
        """

    final = []
    sequence = ""
    infile = open(fasta_filename, "r")
    line = infile.readline()

    while line != "":
        line = line.strip()

        if line != "" and line[0] == ">":
            if sequence != "":
                final.append(sequence)
                sequence = ""
        elif line != "":
            sequence += line

        line = infile.readline()

    if sequence != "":
        final.append(sequence)

    infile.close()

    return final

def transcribeAndTranslate(filename: str) -> None:
    """
    Function:
        Reads the DNA sequences from the FASTA file and prints the protein
    Parameter:
        the filename
    Returns:
        None
    """

    sequences = readFASTAFile(filename)

    if len(sequences) == 0:
        return 
    
    proteins = []

    for i in range(len(sequences)):
        sequence = sequences[i]
        promoter = findPromoter(sequence)

        if promoter != None:
            mrna = transcribe(sequence, promoter)
            start = findStartCodon(mrna)

            if start != None:
                protein = translate(mrna, start)
            else:
                protein = ""
        else:
            protein = ""

        proteins.append(protein)
    
    mutated = proteins[0]
    for i in range(1, len(proteins)):    
        mutations = findMutations(mutated, proteins[i])

        print("Mutations at:", mutations)
        print("=" * 40)

def main():

    print(findPromoter("xxxxTATAATxxxx"), "expected:", 4)
    print(findPromoter("TATAATxxxx"), "expected:", 0)
    print(findPromoter("xxxxxxxxxxxx"), "expected:", None)

    dna = "xxxxxxxxTATAATxxxxxxxxxxAAAACCCCGGGGTTTT"
    promoter = findPromoter(dna)
    print(transcribe(dna, promoter), "expected:", "UUUUGGGGCCCCAAAA")
    dna = "TATAATxxxxxxxxxxTTTT"
    p = findPromoter(dna)
    print(transcribe(dna, p), "expected:", "AAAA")
    dna = "xxxxTATAATxxxxxxxxxxCCCC"
    p = findPromoter(dna)
    print(transcribe(dna, p), "expected:", "GGGG")
    dna = "xxxxTATAATxxxxxxxxxxGGGG"
    p = findPromoter(dna)
    print(transcribe(dna, p), "expected:", "CCCC")

    print(findStartCodon("CGAUGGAUG"), "expected:", 2)
    print(findStartCodon("AUGXXXX"), "expected:", 0)
    print(findStartCodon("XXXXAUG"), "expected:", 4)
    print(findStartCodon("CCCCCCC"), "expected:", None)
    print(findStartCodon("AUGAUGAUG"), "expected:", 0)

    mrna = "AUGGCUAAA"
    start = findStartCodon(mrna)
    print(translate(mrna, start), "expected:", "AK")

    mrna = "AUGGCUACCGAA"
    start = findStartCodon(mrna)
    print(translate(mrna, start), "expected:", "ATE")

    mrna = "AUGUAA"
    start = findStartCodon(mrna)
    print(translate(mrna, start), "expected:", "")

    print(findMutations("ACGT", "AGGT"), "expected:", [1])
    print(findMutations("AAAA", "AAAA"), "expected:", [])
    print(findMutations("ACGT", "TCGA"), "expected:", [0,1,2,3])

    print(readFASTAFile("dna_sequences_test.txt"))
    print(readFASTAFile("dna_sequences_test.txt"), "expected: list of sequences")
    print(len(readFASTAFile("dna_sequences_test.txt")), "expected: > 0")

    print(transcribeAndTranslate(("dna_sequences_test.txt")))
    transcribeAndTranslate("dna_sequences_test.txt")
    transcribeAndTranslate("dna_sequences_test.txt")    

main()