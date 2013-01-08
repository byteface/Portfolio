*** UTVECKLINGSPORTFOLIO *** README.TXT *** SYSTEMDOKUMENTATION ***
Per Jonsson, Linda Jansson, Linköpings universitet 2012

--- TESTNING AV SYSTEMET ---
Vid det sista seminarietillfället i kursen fick tredje person möjlighet att systemtesta portfolion. Vi observerade användarnas beteenden och noterade detta, de kunde även komma med kritik, påtala brister samt ge tips på förbättringar.  Särskilt användbart är denna testning om fel upptäcks, vi hade dock inga sådana brister i systemet som gjorde att det uppträdde oväntat eller oförklarligt, eller kraschade.

De korrigeringar som föreslogs var:
- En designmiss på projektöversiktsidan där radbrytningar hade letat sig in i koden på fel ställe. (Åtgärdat)
- Förslag till fler sökfält på söksidan. Vi tyckte att det var relevant att integrera precis alla i en sökning.
- Förslag till att lägga menyn i tekniköversiktsidan på vänster sida istället för höger sida. Vi har dock ingen vänsterkolumn i vår layout, så det är inte aktuellt att åtgärda.
- Vi använde oss av en redirect-funktion till startsidan när användaren skrev in fel projekt-ID. Den generella feedbacken vi fick var att redirecta till 404-sidan istället.
- Några menade att sökfunktionen som filtrerar på tekniker ska implementeras annorlunda men då förlorar den sitt ursprungliga syfte; att kolla om en specifik uppsättning av gemensamma tekniker finns i ett projekt. 


--- INSTALLATION ---
För att kunna testa och använda portfolion behöver du installera Flask, då portfolion använder Flask som webbramverk.

Du kan öppna en terminal i Ubuntu och köra följande kommando:

$ sudo apt-get install python-setuptools 
$ sudo easy_install Flask

Eller ännu enklare:

$ sudo pip install Flask

För att köra portfolion räcker det med att navigera till mappen med python-scipten och köra portfolio-scriptet i Python 2.x; det kommer inte att fungera i Python 3.x, eftersom det inte är skrivet i Python 3. Skriv då exempelvis följande:

$ python2 portfolioserver.py 

Öppna nu URL:en http://127.0.0.1:5000 i din webbläsare.  Då bör webbportfolion öppnas och du kan då använda den som vilken webbsajt som helst.


--- PAKETERING ---
Katalogstrukturen ser ut enligt följande:

Utvecklingsportfolio/ 
    portfolioserver.py
    data.py
    data.json    

    doc/ 
	README.txt
	Portfoliomanual.pdf 
    static/ 
	images/ 
	        *.jpg
	style/ 
            	*.css, *.gif 
    templates/ 
	        *.html

I botten av strukturen återfinns pythonscripten och databasen. Dokumentation finns i doc/, i static/ hittas stilmallar, bildfiler och i templates/ html-filer.

--- MER ---
För vidare läsning och utförligare beskrivning av hur man använder portfolion, se filen: ”Portfoliomanual.pdf”
