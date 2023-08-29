# Fissione nucleare
Alcuni ingegneri stanno ultimando il progetto di una nuova centrale a fissione nucleare,
e hanno bisogno di un software per testare il processo di fissione.

I moduli e le classi vanno sviluppati nel package *nuclear*.
Non spostare o rinominare moduli e classi esistenti e non modificare le signature dei metodi.

In *main.py* viene fornito del semplice codice, da voi modificabile, che testa le funzionalità base.
Esso mostra esempi di uso dei metodi principali ed esempi dei controlli richiesti.

Tutte le eccezioni, se non altrimenti specificato, sono di tipo *ReactorException* definita nel modulo *errors*.


## R1: Materiali (5/21)
La classe astratta *Material* del modulo *materials* rappresenta un materiale che prende parte alla fissione nucleare.
Essa definisce le property astratte:
- ```name(self) -> str```
- ```energy(self) -> float```
- ```info(self) -> str```

Esse forniscono, rispettivamente, il nome, l'energia prodotta dalla fissione **DI UN GRAMMO** di materiale, e altre informazioni legate al materiale che dipendono dalla sua tipologia.

La classe *ReactorSimulator* del modulo *nuclear* permette di aggiungere diverse tipologie di materiali.

Il metodo
```add_fuel(self, name: str, energy: float, price: int) -> None```
permette di definire un nuovo carburante per la fissione,
specificandone il nome, l'energia prodotta dalla fissione **PER GRAMMO DI MATERIALE**, e il prezzo al grammo.

Il metodo
```add_waste(self, name: str, energy: float, disposal_cost: int) -> None```
permette di aggiungere una scoria nucleare,
specificandone il nome, l'energia prodotta dalla sua fissione **PER GRAMMO DI MATERIALE**,
e il costo di smaltimento della scoria **PER GRAMMO DI MATERIALE**.

Il metodo
```add_auxiliary(self, name: str) -> None```
permette di aggiungere un materiale ausiliario, specificandone il nome.
La property ```energy(self) -> float``` per un materiale ausiliario restituisce sempre 0.

Il metodo
```get_material(self, name: str) -> Material```
permette di ottenere l'oggetto rappresentante un materiale dato il nome.

La property ```info(self) -> str```, per un carburante, restituisce il suo prezzo, preceduto dalla parola *Price* e separati da uno spazio.
Per una scoria, restituisce la parola *Disposal* seguita dal costo di smaltimento, separati da uno spazio.
Esempi:
- *Price 22*
- *Disposal 5*

Per un materiale ausiliario, la property ```info(self) -> str``` restituisce una stringa vuota.


## R2: Reazione (5/21)
La classe astratta *Material* possiede ulteriori metodi astratti, che servono per definire il processo di fissione.
Il processo di fissione parte da un materiale (solitamente un carburante) che si divide in diversi carburanti e scorie.
I carburanti e scorie prodotti si dividono a propria volta, finché si raggiungono scorie o carburanti non più scomponibili.

Il metodo ```add_product(self, product: "Material", quantity: float) -> None``` permette di aggiungere a un materiale un prodotto della sua fissione,
ovvero uno dei materiali in cui il materiale originale si scompone durante la reazione.
Il secondo parametro permette di specificare i grammi di prodotto che si generano per ciascun grammo del materiale originario.
Se il metodo viene invocato su un materiale ausiliario, viene lanciata un'eccezione.

La property ```products(self) -> List[Tuple["Material", float]]```, restituisce una lista contenente, per ciascuno dei prodotti di fissione,
l'oggetto rappresentante il materiale generato, e la rispettiva quantità in grammi generata per ciascun grammo del materiale originario.
**PER TUTTI I TIPI** di materiale su cui è eseguito il metodo (**ANCHE** quelli ausiliari),
se non sono presenti prodotti di fissione, il metodo deve restituire una lista vuota.

Il metodo ```set_auxiliary(self, material: "Material") -> None``` permette di settare un materiale ausiliario,
necessario affinché avvenga la reazione di fissione del materiale.
Il metodo lancia un'eccezione se viene chiamato su un materiale ausiliario.

La property ```auxiliary(self) -> Optional["Material"]```, permette di ottenere il materiale ausiliario di un altro materiale.
**PER TUTTI I TIPI** di materiale su cui è eseguito il metodo (**ANCHE** quelli ausiliari),
se non è presente un materiale ausiliario, deve essere restituito ```None```.

**IMPORTANTE:** si assuma che la struttura del processo di fissione abbia la struttura di un albero,
in cui ciascuna scoria o carburante può comparire al massimo una volta.


## R3: Prodotti intermedi (3/21)
Il metodo ```add_intermediate(self, product: str, intermediate: str, quantities: Tuple[float, float]) -> Optional[List[str]]```
della di *ReactorSimulator*, permette di aggiungere un prodotto intermedio prima di un prodotto di fissione.
Il nome del prodotto di fissione che deve essere preceduto da quello intermedio è fornito come primo parametro.
 Il nome del prodotto intermedio da aggiungere, invece, è fornito come secondo parametro.

Ad esempio, se il materiale *mat* produceva il prodotto *prod*,
ora il materiale *mat* deve produrre il prodotto intermedio *int* e il prodotto intermedio *int* produrrà a sua volta il prodotto *prod*.

Le quantità in grammi del prodotto intermedio per ciascun grammo del materiale di partenza, e la quantità in grammi di prodotto data la quantità in grammi del prodotto intermedio, sono forniti come tupla tramite il terzo parametro.

**ATTENZIONE**: in quanto il processo di fissione ha una struttura ad albero, ogni materiale ha al più un padre.


## R4: Analisi inconsistenze (4/21)
Il metodo ```find_inconsistency(self, fuel: str, auxiliary: Set[str]) -> Optional[str]``` di *ReactorSimulator*,
accetta come parametri il nome di un carburante e un set di nomi di materiali ausiliari introdotti nel reattore.
Il metodo simula la reazione fino ad arrivare a materiali non più scomponibili, controllando se, per ciascun materiale che si scompone,
il suo materiale ausiliario, **QUANDO RICHIESTO**, è disponibile tra quelli introdotti nel reattore.
Se si trova un materiale ausiliario mancante il metodo ne restituisce il nome, altrimenti restituisce ```None```.

**IMPORTANTE** si assuma che ci sia al più un materiale ausiliario mancante.

## R5: Simulazione (4/21)
Il metodo ```simulate_reaction(self, fuel, quantity) -> Tuple[List[Tuple[str, float]], float, float]``` di *ReactorSimulator*,
permette di simulare l'esito di una reazione.
Il metodo accetta come parametri il nome di un carburante e la sua quantità in grammi.
Il metodo deve simulare la reazione, assumendo che i materiali ausiliari siano sempre disponibili,
fino a ottenere materiali non più scomponibili.

**ATTENZIONE**: Si assuma che i materiali non più scomponibili siano *SEMPRE* delle scorie.

Il metodo deve restituire un tupla composta da tre elementi:
- una lista di tuple, ciascuna contenente il nome della scoria non più scomponibile e della sua quantità.
- l'energia totale prodotta da tutti gli elementi che si scompongono.
- il costo di smaltimento di tutte le scorie non più scomponibili.

**ATTENZIONE**: Si ricorda che l'energia e il costo di smaltimento dipendono dalla quantità di materiale.


