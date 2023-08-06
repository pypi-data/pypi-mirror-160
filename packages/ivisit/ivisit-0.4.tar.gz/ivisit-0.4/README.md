IVisit 0.4
-------------------------
Ein Interaktives VIsuelles SImulation Tool
für Python-basierte generische Modell-Simulation und Optimierung von Modell-Parametern
(c) Andreas Knoblauch, HS Albstadt-Sigmaringen

Aktivierung/Sichtbarkeit
-------------------------
Der folgende Shell-Befehl macht das IVisit Verzeichnis global sichtbar,
indem es vorne in PYTHONPATH und PATH gestellt wird (ggf. auch in .bashrc einfügen...):

source /home/ak/projects/experimental/IVisit/python/BashSrc


Versionskontrolle mit Git/GitHub
---------------------------------
Unter Versionskontrolle stehen die folgenden Dateien/Verzeichnisse:
python: Python Sources von IVisit
documentation: Kurz-Doku zu IVisit
demos: Demo-Skripte zu IVisit
design: Entwurf-Dokumente zu IVisit
README.txt: this file
ToDo.txt: Weitere Planung

Nicht unter Versionskontrolle stehen:
shipping: Packages prepared for shipping

Einrichten eines GitHub Repositories (wie hier bei IVisit):
------------------------------------------------------------
1) Im Basisverzeichnis (IVisit): git init
2) In Unterverzeichnissen geeignete .gitignores definieren (Kopiere von alten Repos)
3) git status
4) Alle relevanten Dateien zum Repository hinzufügen: git add ...
5) Initial commit: git commit -m "Some Message"
6) Auf GitHub ein Remote-Repository einrichten: Einloggen, "New Rpository" etc.
   --> HTTPS-Adresse kopieren (z.B. https://github.com/aknoblauch/IVisit.git)
7) Link local repository to GitHub repository: git remote add origin https://github.com/aknoblauch/IVisit.git
8) Push to GitHub: git push origin master

Packaging:
-----------
see                        : https://packaging.python.org/en/latest/tutorials/packaging-projects/
build package              : python3 -m build
upload package to test-repo: python3 -m twine upload --repository testpypi dist/*
upload package to PyPI     : python3 -m twine upload dist/*
install from test-repo     : pip3 install --index-url https://test.pypi.org/simple/ --no-deps ivisit
install from PyPI          : pip3 install ivisit
