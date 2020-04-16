# ISN Bembeleyo Project
## William BRISA et Baptiste CRESPIN

### Instruction de démarrage de l'application
1. *dézippez* le fichier contenant notre application dans un dossier autorisant l'écriture;

2. assurez-vous d'avoir *python3* et *pip* installés;

3. démarrez l'environnement virtuel (en cas d'erreur `pip install vrtualenv`)
  - sous Windows: `. .\venv\Scripts\activate.ps1`;
  - sous Linux/Mac?: `venv/Scripts/activate`;


4. le démarrage de notre app nécessite des *modules supplémentaires* à installer : `pip install -r requirements.txt`;

// note: la base de donnée est au format sqlite donc elle sera utilisée par l'application sans intervention supplémentaire de votre part;


5. lancez l'application avec `flask run` ou `python -m flask run` (voir sources.md : *installing flask* en cas d'erreur).