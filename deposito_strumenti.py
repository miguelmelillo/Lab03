class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.__responsabile = responsabile
        self._strumenti = {}
        self._prestito = {}

    @property
    def responsabile(self):
        return self.__responsabile
    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self.__responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            fr = open(file_path, "r")
            for riga in fr:
                riga = riga.rstrip()
                campo =  riga.split(',')
                marca = campo[2]
                if marca in self._strumenti:
                    self._strumenti[marca].append(campo)
                else:
                    self._strumenti[marca] = [campo]
            self._strumenti = dict(sorted(self._strumenti.items()))
            fr.close()
            return self._strumenti
        except FileNotFoundError:
            raise FileNotFoundError("File non trovato")


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        oldCodes = []
        strumenti = self._strumenti
        for m in strumenti:
            for i in range(0, len(strumenti[m])):
                oldCodes.append(int(strumenti[m][i][0][1:])) # utilizzo oldCodes per salvare i digiti degli codici già esistenti
        oldCodes.sort()
        lastCode = oldCodes[-1]
        newCode = 'S' + str(lastCode+1) #codice nuovo, prendendo il più grande esistente e sommando 1
        dati = [newCode, tipo, marca, anno_acquisto, valore]
        if marca not in strumenti:
            strumenti[marca] = [dati]
        else:
            strumenti[marca].append(dati)
        return newCode

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        for m in self._strumenti: # quando ho salvato i dati, ho già salvato come un dizionario dove ogni chiave è la marca, e ho anche ordinato alfabeticamente
            print(f"{m}: {self._strumenti[m][0]} - {self._strumenti[m][1]} - {self._strumenti[m][2]} - {self._strumenti[m][3]}")


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        oldPCodes = []
        SCodes = [] #codici degli strumenti per vedere se id_strumento è valido --- in seguito
        for m in self._strumenti:
            for i in range (0, len(self._strumenti[m])):
                SCodes.append(self._strumenti[m][i][0])
        if id_strumento not in SCodes:
            raise Exception("Strumento non trovato") # caso non si valido/non è presente in SCodes
        if self._prestito == {}: # Se non è stato fatto nessun prestito ancora
            newPCode = "P1"
            self._prestito[newPCode] = id_strumento
            return newPCode
        else: # se ci sono dei prestiti
            for p in self._prestito:
                oldPCodes.append(p)
            oldPCodes.sort()
            lastPCode = oldPCodes[-1]
            newPCode = 'P' + str(int(lastPCode[1:])+1) #simile a quello che ho fatto per aggiungere degli strumenti, però in oldPCodes non ci sono solo dei numeri, ma tutto il codice
            for pr in self._prestito:
                if self._prestito[pr] == id_strumento:
                    raise Exception("Strumento già in prestito") # caso dove lo strumento è già in prestito
                else:
                    self._prestito[newPCode] = id_strumento
                    return newPCode

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        trovato = False
        for p in self._prestito:
            if p == id_prestito:
                self._prestito[p] = "Finito"
                trovato = True
        if not trovato:
            raise Exception("Prestito non trovato") # variabile trovato creata per verificare che esista is prestito, nel caso non sia presente sul sistema, ritorna la exception
        else:
            return True

