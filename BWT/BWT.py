import subprocess

class BWT:

    """
    This class provides functions for constructing and manipulating the Burrows-Wheeler Transform (BWT) of a given sequence. 
    It includes methods to create and sort the BWT matrix, search for patterns using the BWT, and reconstruct the original sequence from the BWT.

    Parameters
    ----------
    seqOriginal : str
        The original sequence from which the BWT is to be constructed.

    Attributes
    ----------
    seqOriginal : str
        Stores the original sequence.
    listaSequenciaOriginal : list[str]
        Used to reconstruct the original sequence from the BWT.

    """

    def __init__(self, seqOriginal : str) -> None:

        self.seqOriginal = seqOriginal
        self.listaSequenciaOriginal = []
        
    def criarMatriz(self, seq : str) -> list[str]:
        """
        Creates the matrix used to generate the BWT from the provided sequence.

        Parameters
        ----------
        seq : str
            The sequence from which the matrix is generated.

        Returns
        -------
        list[str]
            A list of strings representing the cyclically rotated forms of the input sequence.
        """

        matriz = []
        for indice in range(len(seq)):

            matriz.append(seq)

            seq = seq[-1] + seq[:len(seq)-1]

        return matriz

    def ordenarMatriz(self, matriz : list[str]) -> list[str]:
        """
        Sorts the matrix generated by criarMatriz.

        Parameters
        ----------
        matriz : list[str]
            The matrix of cyclically rotated sequences to be sorted.

        Returns
        -------
        list[str]
            A sorted list of the cyclic permutations of the sequence.
        """

        return sorted(matriz)

    
    def imprimirMatriz(self, matriz : list[str]) -> None:
        """
        Prints each line of the matrix.

        Parameters
        ----------
        matriz : list[str]
            The matrix to be printed.
        """

        for linha in matriz:

            print(linha)

    def construirBWT(self, matriz : list[str]) -> str:
        """
        Constructs the BWT from the sorted matrix.

        Parameters
        ----------
        matriz : list[str]
            A sorted matrix of cyclic permutations of the sequence.

        Returns
        -------
        str
            The Burrows-Wheeler Transform of the sequence.
        """

        bwt = ""

        for linha in matriz:

            bwt += linha[-1]

        return bwt

    def criarPrimeiraColuna(self, bwt : str) -> list[str]:
        """
        Generates the first column of the BWT matrix from the BWT string.

        Parameters
        ----------
        bwt : str
            The Burrows-Wheeler Transform string.

        Returns
        -------
        list[str]
            A list containing the sorted characters of the BWT string.
        """

        return sorted(bwt)

    def criarUltimaColuna(self, bwt : str) -> list[str]:
        """
        Generates the last column of the BWT matrix from the BWT string.

        Parameters
        ----------
        bwt : str
            The Burrows-Wheeler Transform string.

        Returns
        -------
        list[str]
            A list containing the characters of the BWT string.
        """

        lista = []

        for item in bwt:

            lista.append(item)

        return lista

    def criarDicionarioOcorrencias(self, bwt : str) -> None:
        """
        Creates a dictionary to keep track of character occurrences in the BWT string.

        Parameters
        ----------
        bwt : str
            The Burrows-Wheeler Transform string.
        """
        
        self.dicionarioOcorrencias = {letra: -1 for letra in bwt}
        
    def decidirCaracter(self, item : str, chave: str, lista : list[str]) -> None:
        """
        Decides and records occurrences of characters in a list based on the BWT string.

        Parameters
        ----------
        item : str
            The character to be checked.
        chave : str
            The character key in the dictionary.
        lista : list[str]
            The list to which the concatenated character and its occurrence count are added.
        """

        if item == chave:

            self.dicionarioOcorrencias[chave] += 1
            lista.append(item + str(self.dicionarioOcorrencias[chave]))
            
        

    def preencherLista(self, listaSequencias : list[str], listaConcatenada : list[str]) -> None:
        """
        Fills a list with concatenated sequences and their occurrences.

        Parameters
        ----------
        listaSequencias : list[str]
            A list of sequences.
        listaConcatenada : list[str]
            A list to which the sequences with concatenated occurrence counts are added.
        """
        
        for item in listaSequencias:
            
            for chave in self.dicionarioOcorrencias.keys():

                self.decidirCaracter(item, chave, listaConcatenada)

        for chave in self.dicionarioOcorrencias.keys():

            self.dicionarioOcorrencias[chave] = -1
        
                
    def obterSequenciaOriginal(self, letra : str, comprimentoUltimaColuna : int, primeiraColuna : list[str], ultimaColuna : list[str]) -> None:
        """
        Recursively reconstructs the original sequence from the BWT using the first and last columns.

        Parameters
        ----------
        letra : str
            The starting letter for reconstruction.
        comprimentoUltimaColuna : int
            The length of the last column, used to stop the recursion.
        primeiraColuna : list[str]
            The first column of the BWT matrix.
        ultimaColuna : list[str]
            The last column of the BWT matrix.
        """
        
        indice= -1

        for item in ultimaColuna:

            indice += 1
            
            if item == letra:

                self.listaSequenciaOriginal.append(letra[0])

                letra = primeiraColuna[indice]
            
            if len(self.listaSequenciaOriginal) == comprimentoUltimaColuna:
                
                return

        self.obterSequenciaOriginal(letra, comprimentoUltimaColuna, primeiraColuna, ultimaColuna)

    def SequenciaOriginalEmString(self) -> str:
        """
        Converts the list of the original sequence into a string format.

        Returns
        -------
        str
            The original sequence reconstructed from the BWT.
        """

        seqOriginal = ''.join(self.listaSequenciaOriginal)

        seqOriginal = seqOriginal[1:len(seqOriginal)] + seqOriginal[0]

        return seqOriginal

    def suffix_array(self, seq : str) -> list[int]:
        """
        Generates a suffix array for the sequence.

        Parameters
        ----------
        seq : str
            The sequence for which the suffix array is generated.

        Returns
        -------
        list[int]
            The suffix array representing sorted indices of all suffixes of the sequence.
        """

        self.suffix_array = sorted(range(len(seq)), key=lambda i: seq[i:])

        return self.suffix_array

    
    def procuraPadraoBWT(self, pattern : str) -> list[int]:
        """
        Searches for a pattern within the sequence using the Burrows-Wheeler Transform (BWT) and an FM-index based approach,
        returning the positions of the pattern's occurrences within the original sequence.

        Parameters
        ----------
        pattern : str
            The pattern to be searched within the BWT.

        Returns
        -------
        list[int]
            A list of starting positions within the original sequence where the pattern was found. If no occurrences are found, returns an empty list.

        """

        bwt = self.construirBWT(self.ordenarMatriz(self.criarMatriz(self.seqOriginal)))
        sorted_bwt = sorted(bwt)
        suffix_array = self.suffix_array
        
        # Criação do array de contagem
        count = {char: [0] * (len(bwt) + 1) for char in set(bwt)}
        for i in range(1, len(bwt) + 1):
            for char in count:
                count[char][i] = count[char][i - 1]
            count[bwt[i - 1]][i] += 1

        # Criação do array de primeira ocorrência
        first_occurrence = {}
        for i, char in enumerate(sorted_bwt):
            if char not in first_occurrence:
                first_occurrence[char] = i

        # Algoritmo de pesquisa FM
        top = 0
        bottom = len(bwt) - 1
        while top <= bottom:
            if pattern:
                symbol = pattern[-1]
                pattern = pattern[:-1]
                if count[symbol][bottom + 1] > count[symbol][top]:
                    top = first_occurrence[symbol] + count[symbol][top]
                    bottom = first_occurrence[symbol] + count[symbol][bottom + 1] - 1
                else:
                    return []
            else:
                return sorted([suffix_array[i] for i in range(top, bottom + 1)])

        return []
    

if __name__ == "__main__":
    seq = 'TAGACAGAGA$'
    print('Calcular a Bwt a partir de ' + seq)
    print()
    print('Matriz desordenada')
    print()
    classe = BWT(seq)
    matriz_nao_ordenada = classe.criarMatriz(seq)
    classe.imprimirMatriz(matriz_nao_ordenada)
    print()
    print('Matriz Ordenada')
    print()
    matriz_ordenada = classe.ordenarMatriz(matriz_nao_ordenada)
    classe.imprimirMatriz(matriz_ordenada)
    print()
    bwt = classe.construirBWT(matriz_ordenada)
    print('BWT = ' + bwt)
    
    classe.criarDicionarioOcorrencias(bwt)
    print()
    print('Calcular a sequencia original a partir de ' + bwt)
    print()
    primeiraColuna = classe.criarPrimeiraColuna(bwt)
    print('Primeura Coluna: ' + str(primeiraColuna))
    print()
    ultimaColuna = classe.criarUltimaColuna(bwt)
    print('Última Coluna: ' + str(ultimaColuna))
    print()
    listaConcatenadaPrimeiraColuna = []
    classe.preencherLista(primeiraColuna, listaConcatenadaPrimeiraColuna)
    print('Primeira Coluna Numerada: \n\n' + str(listaConcatenadaPrimeiraColuna))
    print()
    listaConcatenadaUltimaColuna = []
    classe.preencherLista(ultimaColuna, listaConcatenadaUltimaColuna)
    print('Ultima Coluna Numerada: \n\n' + str(listaConcatenadaUltimaColuna))
    print()
    comprimentoUltimaColuna = len(listaConcatenadaUltimaColuna)
    classe.obterSequenciaOriginal('$0', comprimentoUltimaColuna, listaConcatenadaPrimeiraColuna, listaConcatenadaUltimaColuna)
    sequenciaOriginal = classe.SequenciaOriginalEmString()
    print('SequenciaOriginal: ' + sequenciaOriginal)
    print()
    padrao = 'AGA'
    print('Procurar o padrão: ' + padrao)
    print()
    arraySufixos = classe.suffix_array(seq)
    print(arraySufixos)
    print()

    print(classe.procuraPadraoBWT(padrao))

    print("Metricas de Codigo:")
    print("\nMetrica cyclomatic complexity:")
    print(subprocess.call(["radon","cc","BWT/BWT.py", "-s"]))
    print("\nMetrica maintainability index:")
    print(subprocess.call(["radon","mi","BWT/BWT.py", "-s"]))
    print("\nMetrica raw:")
    print(subprocess.call(["radon","raw","BWT/BWT.py", "-s"]))