<!--
	This is a markdown document. You can generate other formats with pandoc:
	$ pandoc developmentlog.md -o developmentlog.html --toc -s
	$ pandoc developmentlog.md -o developmentlog.pdf --toc -s
-->

<style>
#TOC {
	font-size: smaller;
	float: right;
}
</style>

# Bitàcola: Menjo bé, Menjo del Baix

[This development log is written in Catalan to be used for my teaching duties. Sorry guys.]

Exemple de com treballar de forma àgil amb Django i
testos,
migracions de bases de dades,
sistema de control de versions,
integració continuada...
L'excusa és fer una applicació que faci de directori de botigues d'alimentació de kilometre zero.

## Anàlisis de requeriments preliminar

Fem un petit anàlisis previ dels requeriments.
No ha de ser pas un anàlisis gaire exhaustiu,
però ha de servir per fer-nos una mínima planificació del que farem.
Els requeriments són sempre modificables.

Volem fer una aplicació per a que
la gent del Baix Llobregat sapiga on pot comprar fruita i verdura de kilómetre zero.
És a dir, productes que no vinguin de fora i que no hagin passat pel MercaBarna.

No és pas un nou canal de distribució, sinó, de moment,
merament un lloc neutre per recopilar tots aquests canals existents.

### Glossari del domini

Els conceptes claus que identifiquem al domini serien:

- **Productor:** Pagés o societat de pagesos (cooperativa, SL...) que fa activitat agrícola a la zona.
- **Punt de distribució:** Una localització on els consumidors poden adquirir els productes agrícoles.
	- **VentaDirecta:** Cotxera o parada on els mateixos pagesos venen els seus productes
	- **CooperativaConsum:** Comunitats de consumidors que fan compres conjuntes
	- **CooperativaProductors:** Comunitats de productors que venen els seus productes directament
	- **Establiment:** Establiments minoristes que venen productes portats directament de pagés
	- **Fira:** Fira periódica es deixa als productors i distribuidors vendre els seus productes
- **Denominació:** Es el nom legal de la varietat del producte
- **Clase:** Fruita, Llegums, Tomàquets, Enciams
- **Varietat:** Differents varietats
- **Mètode de producció:** Condicions en les que se ha produït el producte.
- **Explotació:** Un camp on un productor produeix els productes

Legalment cal etiquetar la província d'origen,
a nosaltres ens preocupa més identificar directament el municipi o fins i tot l'explotació d'origen.

- TODO: Diagrama estàtic de relacions entre conceptes
- TODO: Anar posant aquí altres restriccions
- TODO: Revisar amb pagesos els canals de distribució existents
- TODO: Revisar amb pagesos els diferents mètodes de cultiu
- TODO: Revisar amb pagesos varietats, especies...
- TODO: Revisar amb pagesos temporades

### Casos d'ús

Les histories d'usuari que s'ens acudeixen d'entrada són:

- Una persona anònima vol saber a quins punts de distribució del poble pot trobar patates de kilometre zero
- Una persona anònima vol explorar quins distribuidors hi ha al poble i quins productes tenen
- Una persona registrada vol enviar un comentari sobre
	- un productor
	- un punt de distribució
- Una persona registrada vol dir que li agrada
	- un productor
	- un punt de distribució
- Una persona registrada vol rebre notificacions de quins productes hi ha disponibles cada setmana
- Una persona registrada vol afegir un productor nou
- Una persona registrada vol vol cambiar els productes disponibles a un punt de distribució

No les intentarem cobrir totes d'entrada sinó que anirem incorporant-les iterativament
amb el criteri de que el programari sigui útil des de les primeres iteracions.

## Establint l'entorn de treball

### El projecte i el sistema de control de versions

Per fer el control de versions farem servir `git`.
Un sistema de control de versions és vital per no perdre l'_oremus_.
Ens permet anar portant el seguiment dels canvis que anem fent i
sincronitzar diferents linies de desenvolupament, o el treball de diferents desenvolupadors.

Només explicitarem aquí les comandes fer portar el control de versions local,
normalment cal sincronitzar-ho amb un repositori extern (`push`, `pull`).
Internet n'està ple de tutorials sobre `git` als que et pots referir.
Per instalar-ho a Ubuntu/Debian:

```bash
	$ sudo apt-get install git
```

Creem doncs el directori del nostre projecte:

```bash
	$ mkdir menjodelbaix
	$ cd menjodelbaix
	$ git init    # per inicialitzar el control de versions
```

Això crea un directori `.git` ocult que va portant les dades del seguiment.

Hi ha un seguit d'arxius que normalment no voldrem afegir al seguiment de versions.
Perque no ens facin nosa, els afegirem a un arxiu anomentat `.gitignore`:

```bash
	$ echo '*~' >> .gitignore
	$ echo '*.bak' >> .gitignore
	$ echo '*.sw?' >> .gitignore
	$ echo '*.pyc' >> .gitignore
	$ echo __pycache__ >> .gitignore
	$ git add .gitignore    # afegim l'arxiu al seguiment
	$ git commit .gitignore -m 'Added .gitignore'  # confirmem els canvis
```

Ara creem alguns fitxers bàsics pel projecte.

La llicència va normalment al directori arrell a un fitxer anomenat `COPYING`.
Si es vol garantir les llibertats dels usuaris,
recomano fer servir la llicència GNU-Affero GPL.
La llicència GNU-GPL clàssica, garanteix les llibertats que garanteix en el moment que el programari es distribueix.
Però amb les aplicacions web, hi ha ús sense distribució, per aixó,
si volem garantir les llibertats de l'usuari, és necessària la llicència Affero.
La podem descarregar directament:

```bash
	$ wget https://www.gnu.org/licenses/agpl-3.0.txt -O COPYING
```

I un README que ben segur faràs més llarg:

```bash
	$ echo "# MenjoDelBaix" >> README.md
	$ echo >> README.md
	$ echo "Zero kilometer groceries directory" >> README
```

Afegim els dos fitxers al control de versions:

```bash
	$ git add README.md COPYING
	$ git commit -a -m 'COPYING and README added'
```


### L'entorn virtual de Python

Treballarem en un entorn virtual de Python.
Un entorn virtual ens permet:

- instal·lar paquets Python sense permisos d'administrador
- instal·lar paquets Python o versions diferents de les que hi ha instal·lades o disponibles per instal·lar al sistema
- tenir controlats quins paquets hi ha en aquest entorn

Això és molt convenient quan treballem a un hosting on no tenim accés d'administrador
i ens permet tenir molt controlades les dependències del nostre projecte.

Suposem que estem en una Ubuntu moderneta.
Els unics paquets que instal·larem al sistema com administradors seran:
```bash
	$ sudo apt-get install python3 python-virtualenv
```

Nota: Treballarem amb Python 3 però el virtualenv d'Ubuntu és el de Python 2.
No hi ha problema. Funciona igual.

Creem l'entorn virtual de Python:
```bash
	$ virtualenv --no-site-packages -p /usr/bin/python3 env
```

Això crea un subdirectori `env` amb una instal.lació propia de Python 3.
Tots els paquets de Python que fem servir han d'instalar-se a aquest directori.
L'opció `--no-site-packages` és per forçar que no faci servir els paquets del sistema,
així podrem estar segurs de que no ens falta cap.

Donat que no volem comitejar l'entorn, l'afegirem al `.gitignore`:
```bash
	$ echo env >> .gitignore
	$ git commit .gitignore -m 'env ignored'
```


Important: A partir d'ara, a cada terminal que volguem treballar amb aquest entorn Python virtual, cal executar:

	$ source env/bin/activate

Podem veure que un terminal està dintre de l'entorn perqué al prompt del shell
hi ha un prefix amb el nom del directori que el conté:

```bash
	(env)$
```

Ignorare aquest prefix en endavant i suposarem que totes les comandes s'executen dintre d'un terminal a l'entorn.

Dintre de l'entorn, el Python per defecte sera Python 3 i
tots els paquets Python que instal·lem s'instal·lara dintre d'aquest entorn virtual.

En producció cal dir-li a l'Apache que faci servir l'entorn virtual.
Pots trobar com dir-li a:
<http://www.saltycrane.com/blog/2009/05/notes-using-pip-and-virtualenv-django/>

Amb això ja tenim un entorn virtual preparat on
instal·lar els paquets amb la versió que volguem sense permisos d'administrador.
Lo bo d'aquesta aproximació és que no cal tenir gaires permisos al hosting.

### Instal·lem els paquets django

El Django és el marc de treball per la nostra aplicació web.
És qui orquestra els elements de la nostra aplicació.
Des del shell, dintre de l'entorn, instal·lem el Django:

```bash
	$ pip install django
```

Quan estic escrivint aquest tutorial, la versió 1.7 que necessitarem encara és una _release candidate_.
Ho he instalat del git de Django amb:

```bash
	$ pip install git+git://github.com/django/django.git@stable/1.7.x
```

El `pip` va guardant els paquets de Python que anem instal·lant i les seves versions.
Podem treure la llista amb:

```bash
	$ pip freeze
	Django==1.7c3
```

Aquesta llista la podem fer servir per instal·lar els mateixos paquets en un altre entorn.
Si aboquem la llista a un fitxer `requirements.txt`, ho instal·lem tot de cop a un altre entorn fent:

```bash
	$ pip install -r requirements.txt
```

Procedim amb la resta de paquets, volem fer test driven development aixi que necessitarem alguns paquets per fer-ho:

```bash
	$ pip install yaml         # format yaml per serialitzar les dades
	$ pip install django-mptt  # implementació òptima de jerarquies a bases de dades
	$ #pip install selenium # per testejar interficies web
	$ #pip install mock # per simular objectes pels testos
	$ #pip install python_social_auth # per permetre logins des de comptes de Facebook, Google, Github...
```

### Creem el projecte Django

- Un projecte a Django representa un lloc web.
- Aquest lloc web pot combinar diferents mòduls, que Django anomena aplicacions.
- Algunes aplicacions les escriurem nosaltres per cobrir la nostra funcionalitat particular
- Moltes altres funcionalitats les poden cobrir aplicacions
	- que ja venen incorporades amb el Django o,
	- son paquets de tercers que es poden instalar amb el pip.
	- Per exemple:
		- Administració de dades
		- Comentaris, valoracions, categories...
		- Login amb diversos sistemes
		- Geoposicionament
		- ...

Per crear el projecte web ho fem així:

```bash
	$ django-admin startproject devsite '.'
```

Això crea uns quants fitxers:

```
	manage.py             # script que llença operacions comunes del projecte
	devsite/__init__.py   # fitxer buit que defineix devsite com a paquet
	devsite/wsgi.py       # punt d'entrada que executarà el servidor web
	devsite/settings.py   # paràmetres de configuració de Django
	devsite/urls.py       # correspondències entre urls i el codi Python que s'executa
```

Ho afegim tot al sistema de control de versions:

```bash
	$ git add manage.py devsite/
	$ git commit -a -m 'project as created by django-admin'
```

### Inicialitzar la base de dades

Primer cal inicialitzar la base de dades amb la subcomanda `migrate` del `manage.py`

```bash
	$ ./manage.py migrate
	Operations to perform:
	  Apply all migrations: admin, auth, sessions, contenttypes
	Running migrations:
	  Applying contenttypes.0001_initial... OK
	  Applying auth.0001_initial... OK
	  Applying admin.0001_initial... OK
	  Applying sessions.0001_initial... OK
```

Encara que no hem fet res, el nostre projecte ve amb 4 applicacions
per defecte (admin, auth, sessions, contenttypes) que explicarem més endavant.

La base de dades l'ha creada a un fitxer sqlite anomenat `db.sqlite3`.
Podríem fer servir un altre tipus de base de dades com mysql o postgresql configurant apropiadament els settings.
Per començar, ja ens esta bé.

El que no volem es afegir aquest fitxer al git així que l'excloem:

```bash
	$ echo 'db.sqlite3' >> .gitignore
	$ git commit .gitignore -m 'ignorant db.sqlite3'
```


### Executant el servidor de proves

Aquest projecte buit el podem executar en un servidor de proves.
El servidor de proves no serveix per producció, però és molt convenient per desenvolupar.
Normalment el tenim executant-se a un terminal, per veure els missatges d'error,
mentres treballem en un altre.

Recorda que tots els terminals on treballem amb Python han d'estar
executant l'entorn virtual.
Així que d'es d'un terminal nou executem:

```bash
	$ cd menjodelbaix/
	$ source env/bin/activate
	$ ./manage.py runserver 8001
```

Podem accedir a la nostra applicació, de moment buida, a la url <http://localhost:8001>.


### Creem la nostra applicació

Es pot entendre una aplicació de Django com a un conjunt de dades i el codi que les manega.
En el nostre cas, nosaltres tenim els productes, les explotacions agràries, els productors...
Agrupem les dades en applicacions segons com veiem que es podem fer reutilitzar de
forma independent.

Creem l'aplicació que contrindrà els nostres productors, camps, productes...

```bash
	$ ./manage.py startapp menjobe
	$ find menjobe
	menjobe/
	menjobe/__init__.py
	menjobe/admin.py
	menjobe/models.py
	menjobe/tests.py
	menjobe/views.py
	menjobe/migrations/
	menjobe/migrations/__init__.py

	$ git add menjobe
	$ git commit menjobe -m 'menjobe app as created by django-admin'
```

- `models.py`: La definició del model de dades
- `views.py`: El codi de control que serveix les peticions de la web
- `test.py`: Els testos unitaris de l'applicació
- `admin.py`: Com es veuen els models des de l'applicació d'administració
- `migrations`: Paquet que contrindrà scripts de migració entre diferents versions de la base de dades

Afegim a continuacio la nostra aplicació `'menjobe'` a la llista
`INSTALLED_APPS` del fitxer `devsite/settings.py`.

```python
	INSTALLED_APPS = [
		...
		'menjobe',
		]
```

Veiem que a aquesta llista ja hi ha d'altres aplicacions afegides per defecte:

- django.contrib.auth: l'autentificacio d'usuaris
- django.contrib.admin: edició de dades en mode administrador
- django.contrib.session: manegament de sessions
- django.contrib.contenttypes: manegament de tipus de fitxers
- django.contrib.messages: transmisió d'estat entre pàgines
- django.contrib.staticfiles: servei òptim de contingut no generat dinàmicament (imatges, css, js...)

Altres applicacions incloses, malgrat que no estan actives per defecte, són:

- django.contrib.comments: comentaris associats a objectes
- django.contrib.flatpages: pàgines html enmagatzemades a la base de dades (i editables des de l'admin)
- django.contrib.sitemap: generates a sitemap.xml file to hint search engines about your site
- django.contrib.humanize: template filters to convert numbers and dates to something more human bearable
- django.contrib.syndication: generates rss/atom sindication files
- django.contrib.formtools.formpreview: formularis amb vista previa
- django.contrib.formtools.formwizard: formularis encadenats
- django.contrib.sites: utilitats per mantenir més d'un site a la vegada compartint dades
- django.contrib.webdesign: (deprecat)
- django.contrib.gis: informació geogràfica
- django.contrib.redirects: redireccions mantingudes a la base de dades
- ...

### Primer els testos!!

Els testos del projecte els executem fent:

```bash
	$ ./manage.py test
```

En teoría, Django explora totes les aplicacions no instal·lades buscant testos.
Pero com podem estar segurs de que ha agafat el nostre `menjobe/tests.py`?
Fiquem-hi un test que falli:

```python
	from django.test import TestCase

	class AFailingTest(TestCase) :
		def test_failing(self) :
			self.fail("It works!!")
```

Si falla, funciona!
Ja ho tenim funcionant.
Esborrem el test, i seguim.


## Primer cas d'ús

### Planifiquem com adreçar el primer cas d'ús

Adrecem primer el cas d'ús més principal
però en la forma més simple possible que ens sigui útil.

> On puc comprar tomaquets?

No cal que sigui complert i ja sabem que caldrà millorar-ho.
Hem fet tot un desplegament que ens permetrà evolucionar una primera solució imperfecta.

Per poder implementar aquest cas d'ús simplificat ens cal:

- Poder oferir una llista de productes a escollir a un desplegable o similar
- Un cop que l'usuari selecciona un producte en concret, retornar els punts de distribució que el tenen.

Per això cal diverses coses:

- Les categories de productes
- Els punts de distribució
- Les relacions entre totes dues

### Productes amb nom

El primer el farem poc a poc per veure que pot passar quan fem que.

Plantejem el següent test a `menjobe/tests.py:

```python
	from .models import Product

	def Product_Test(TestCase) :

		def test_withName(self) :
			p = Product(name="Carxofa")
			self.assertEqual(p.name, "Carxofa")
			p.save()
			self.assertNotEqual(p.id, None)
```

Executem el test sense fer res:

```bash
	$ ./manage.py test
	...
	ImportError: cannot import name 'Product'
	...
```

Ens demana el model `Product`, el creem a `menjobe/models.py`:

```python
	class Product(models.Model) :
		pass
```
Executem:

```bash
	$ ./manage.py test
		....
	django.db.utils.OperationalError: no such table: menjobe_product
```

Això vol dir que la taula corresponent al model no està creada a la base de dades.

Per crearla farem la nostra primera migració i l'aplicarem:

```bash
	$ ./manage.py makemigrations
	Migrations for 'menjobe':
	  0001_initial.py:
		- Create model Product

	$ ./manage.py migrate
	Operations to perform:
	  Apply all migrations: contenttypes, sessions, admin, menjobe, auth
	Running migrations:
	  Applying menjobe.0001_initial... OK

```

Tornem a executar el test:

```bash
	$ ./manage.py test
	Creating test database for alias 'default'...
	E
	======================================================================
	ERROR: test_name (menjobe.tests.Product_Test)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "/home/vokimon/borrame/spikes/menjodelbaix/menjobe/tests.py", line 8, in test_name
		p = Product(name="Tomato")
	  File "/home/vokimon/borrame/spikes/menjodelbaix/env/lib/python3.4/site-packages/django/db/models/base.py", line 453, in __init__
		raise TypeError("'%s' is an invalid keyword argument for this function" % list(kwargs)[0])
	TypeError: 'name' is an invalid keyword argument for this function

	----------------------------------------------------------------------
	Ran 1 test in 0.013s

	FAILED (errors=1)
	Destroying test database for alias 'default'...
```

Falta el nom, afegim l'atribut `name` al model:

```python
	class Product(models.Model) :
		name = models.CharField(max_length=200, default='')
```

Si intentem executar-ho així, sense actualitzar la BD:

```bash
	$ ./manage.py test
		...
	django.db.utils.OperationalError: no such column: menjobe_product.name
```

Un altre cop, creem una migració i l'apliquem:

```bash
	$ ./manage.py makemigrations 
	Migrations for 'menjobe':
	  0002_product_name.py:
		- Add field name to product

	$ ./manage.py migrate
	Operations to perform:
	  Apply all migrations: contenttypes, admin, menjobe, auth, sessions
	Running migrations:
	  Applying menjobe.0002_product_name... OK

	$ ./manage.py test
	Creating test database for alias 'default'...
	.
	----------------------------------------------------------------------
	Ran 1 test in 0.001s

	OK
	Destroying test database for alias 'default'...

```

Ja passem el test que ens havíem plantejat. Confirmem els canvis, afegint les migracions.

```bash
	$ git add menjobe/migrations/*py
	$ git commit . -m 'Products with name'
```

## Restriccions

Analitzant el codi segur que has tingut la temptació d'afegir
paràmetres al camp `name`.
Els paràmetres sovint impliquen funcionalitat,
si bé el `default` l'haviem de posar per poder fer la migració,
altres restriccions podem justificar-les amb un test.

El test per assegurar-nos de que els noms son únics:

```python
	def test_name_unique(self) :
		p = Product(name="Tomato")
		p.save() 
		p2 = Product(name="Tomato")
		with self.assertRaises(IntegrityError) as cm :
			p2.save()
		self.assertEqual(str(cm.exception),
			"UNIQUE constraint failed: menjobe_product.name")
```

Es passa a verd afegint `unique=True` al camp.

El test per assegurar-nos de que ens donen un valor:

```python
	def test_name_notGivenRaises(self) :
		p = Product()
		with self.assertRaises(IntegrityError) as cm :
			p.save()
		self.assertEquals(str(cm.exception),
			"NOT NULL constraint failed: menjobe_product.name")
```

Es passa a verd canviant `default=None`.
No he aconseguit que casqui quan sigui buit (blank=False no funciona).
Ho deixo pendent.

Aprofitem i fem el test per tenir una representació util de l'objecte.

```python
    def test_str(self) :
        p = Product(name="Tomato")
        self.assertEqual(str(p), "Tomato")

```

Es passa afegit aquest metode a `models.Product`:

```python
    def __str__(self) :
		return self.name
```



## Punts de distribució

Repetim exactament el mateix procés per crear un model de _punts de distribució_ (`RetailPoint`)
amb un atribut `name` i les mateixes restriccions.

La temptació és copiar-ho tot de `Product` i substituir noms.
Cal problema amb copiar,
però, cal anar amb cura, perquè copiant sovint no substituim algun identificador
als testos, i cobrim dues vegades `Product` i deixem sense cobertura `RetailPoint`.
Per això, es important **fallar els testos** un a un, tot i que després
copiem la implementació de `Product`.

Al final, tindrem als testos:

```python
from .models import RetailPoint

class RetailPoint_Test(TestCase) :

	def test_withName(self) :
		r = RetailPoint(name="Can Xavi")
		self.assertEqual(r.name, "Can Xavi")
		r.save()
		self.assertNotEqual(r.id, None)

	def test_str(self) :
		r = RetailPoint(name="Can Xavi")
		self.assertEqual(str(r), "Can Xavi")

	def test_name_nullRaises(self) :
		r = RetailPoint()
		with self.assertRaises(IntegrityError) as cm :
			r.save()
		self.assertEquals(str(cm.exception),
			"NOT NULL constraint failed: menjobe_retailpoint.name")

	def test_name_unique(self) :
		r = RetailPoint(name="Can Xavi")
		r.save()
		r2 = RetailPoint(name="Can Xavi")
		with self.assertRaises(IntegrityError) as cm :
			r2.save()
		self.assertEqual(str(cm.exception),
			"UNIQUE constraint failed: menjobe_retailpoint.name")
```

I la implementació:

```python
	class RetailPoint(models.Model) : 
		name = models.CharField(max_length=200, default=None, unique=True)
		def __str__(self) :
			return self.name
```

## Els punts de distribució poden tenir productes

Podem representar al model que cada punt de venda al public disposa d'un conjunt productes
amb una relació N:N, que al Django es representa amb un camp `ManyToManyField`.

Per a testejar la relació, farem servir un helper que donada un iterable
construeix una cadena amb la representació de cada element:

```python
class ProductsInRetailPoints_Test(TestCase) :

    def collect(self, iterable) :
        return "".join("{}\n".format(o) for o in iterable)
            
    def test_collect(self) :
        rows = [1,2,3,4]
        self.assertEqual(self.collect(rows),
            "1\n"
            "2\n"
            "3\n"
            "4\n"
        )   
```

També ens simplificarà el codi de test una utilitat per a desar un conjunt d'objectes de cop:

```python
	def save(self, *args) :
		return [ a.save() for a in args ]
```

Primer ens centrem nomsées en un dels costats de la relació.
Plantejem el test mirant la relació de que un producte pot tenir més d'un punt de distribució.
Implementant-ho amb una ForeignKey,
cada punt de distribució podra tenir només un producte,
però de moment no ens preocupem.

```python
    def test_productRetailPoints_manyRetailers(self) :
        r1 = RetailPoint(name="Retailer 1")
        r2 = RetailPoint(name="Retailer 2")
        p = Product(name="a product")
        self.save(p, r1, r2)

        r1.sells(p)
        r2.sells(p)

        self.assertEqual(
            self.collect(p.retailPoints()),
				"Retailer 1\n"
				"Retailer 2\n"
            )
```

Al test, no fem servir l'API relacional directament,
sino que fem servir mètodes propis.
Això ens dona una certa independència per canviar com implementem la relació.

```python
	class Product(models.Model) :
		...
		def retailPoints(self) :
			return self.retailpoint_set.all()

	class RetailPoint(models.Model) :
		....
		retailedProduct = models.ForeignKey(Product, default=None, null=True)

		def sells(self, product) :
			self.retailedProduct = product
```

Deiem que amb la ForeignKey un punt de distribució només pot tenir un producte.
Doncs plantejem un test amb aquest cas que no podem representar.

```python
    def test_productList_whenMany(self) :
        r = RetailPoint(name="a retail point")
        p1 = Product(name="Product 1")
        p2 = Product(name="Product 2")
        self.save( r, p1, p2 )

        r.sells(p1)
        r.sells(p2)

        self.assertEqual(
            self.collect(r.availableProducts()),
            "Product 1\n"
            "Product 2\n"
            "")
```

El test no el podem passar directament aixi que el comentem per fer un refactor.
El refactor te quatre etapes:

- **Duplicar** l'estructura, es a dir, crear la nova relació sense esborrar l'anterior
	- Aquí generem una migració d'esquema per afegir la nova
- **Farcir** l'estructura nova cada vegada al codi que es farceix de dades l'estructura vella
	- Vol dir que haurem de **duplicar** els **accesos d'escriptura** perque modifiquin ambdues estructures, la vella i la nova
	- És molt bo tenir els accessos centratiltzats perque aquests canvis no siguin massa extensos o dispersos
	- Aquí generarem una migració de dades per copiar les dades de la estructura vella a la nova
- **Recolzar-nos** a l'estructura nova en comptes de la vella
	- Vol dir anar **substituint** progressivament els **accessos de lectura**, perque facin servir l'estructura nova en comptes de la vella
	- Ho fem progressivament perque aquí sovint apareixen errors comesos a l'etapa de farcir, i progressivament és més fàcil identificar l'origen, parem, corregim i seguim.
- **Netejar** els usos que encara queden de la vella (haurien de ser setters) i l'estructura vella en sí.
	- Aquest pas es fa eventualment pero cal posar-li data.
	- Aqui generarem una migració per la eliminació de l'estructura vella
	- Sovint, treure la vella dona peu a renombrar la nova, si els renombrats afecten al model, cal fer migració

### Duplicar

```python
	class Product(models.Model) :
		...
		def retailPoints(self) :
			return self.retailpoint_set.all()

	class RetailPoint(models.Model) :
		....
		retailedProduct = models.ForeignKey(Product, default=None, null=True)

		retailedProducts = models.ManyToManyField(Product, related_name='renameme_set') # <-- Changed

		def sells(self, product) :
			self.retailedProduct = product
```

Fixa't que hem especificat un `related_name` per evitar colisió amb l'atribut reverse manager de la relació vella.

TODO: Migració esquema: afegir relació


### Farcir

```python
	class Product(models.Model) :
		...
		def retailPoints(self) :
			return self.retailpoint_set.all()

	class RetailPoint(models.Model) :
		....
		retailedProduct = models.ForeignKey(Product, default=None, null=True)

		retailedProducts = models.ManyToManyField(Product, related_name='renameme_set')

		def sells(self, *product) :
			self.retailedProduct = product
			self.retailedProducts.clear()       # <-- Changed
			self.retailedProducts.add(product)  # <-- Changed
```

Fixa't que hem afegit un `clear`, per que tot i que es una relació múltiple,
durant el refactor el comportament es mantingui igual.
Quan tornem a activar el test, i el tinguem en vermell, treurem aquesta linia per anar a verd.

TODO: Migració dades: duplicar dades relació

### Recolzar-se

```python
	class Product(models.Model) :
		...
		def retailPoints(self) :
			return self.renameme_set.all()   # <-- Changed

	class RetailPoint(models.Model) :
		....
		retailedProduct = models.ForeignKey(Product, default=None, null=True)

		retailedProducts = models.ManyToManyField(Product, related_name='renameme_set')

		def sells(self, *product) :
			self.retailedProduct = product
			self.retailedProducts.clear()
			self.retailedProducts.add(product)
```

### Netejar

```python
	class Product(models.Model) :
		...
		def retailPoints(self) :
			return self.retailpoint_set.all()   # <-- Changed

	class RetailPoint(models.Model) :
		....
		# retailedProduct = models.ForeignKey(Product, default=None, null=True) <-- Removed

		retailedProducts = models.ManyToManyField(Product)

		def sells(self, *product) :
			# self.retailedProduct = product <-- Removed
			self.retailedProducts.clear()
			self.retailedProducts.add(product)
```

TODO: Migració esquema eliminar relació

### Activem el test

Després d'haver fet tot el refactor,
ho tenim preparat per passar el test molt ràpid només treient el clear.

Al final ens queda el codi així:

```python
	class Product(models.Model) :
		...
		def retailPoints(self) :
			return self.retailpoint_set.all()


	class RetailPoint(models.Model) :
		....
		retailedProducts = models.ManyToManyField(Product)

		def sells(self, *products) :
			self.retailedProducts.add(*products)

		def availableProducts(self) :
			return self.retailedProducts.all()
```


I amb això ja tenim prou model implementat pel nostre cas d'ús.


### Vistes per a una API JSON

El cas d'ús que ens hem plantejat te dues necessitats de dades bàsiques:

- La llista de productes per que l'usuari en trii un
- La llista de punts de venda on es pot trobar un producte

Si les dades les oferim amb una API JSON ens dona molta flexibilitat
per desenvolupar independentment la interfície.

Com testejem les vistes?
Per fer-ho independentment de la url farem servir el `RequestFactory`,
que ens construeix una request tal qual la rebria la vista.

Crearem un nou fitxer de test, `menjobe/test_views.py` per separar els testos del model dels testos de les vistes.

```python
	from django.test import TestCase
	from django.test import RequestFactory
	from .models import Product
	from .models import RetailPoint
	from .views import *
	import json

	class View_Test(TestCase) :
		def setUp(self):
			self.factory = RequestFactory()

		def test_json_allProducts(self) :                                      
																			   
			Product(name="Product 1").save()
			Product(name="Product 2").save()
																			   
			request = self.factory.get("/booo")
			response = allProducts(request)

			self.assertJSONEqual(response.content.decode("utf-8"),
				json.dumps( [
					[1, 'Product 1'],
					[2, 'Product 2'],
				]))
```

La implementem a `menjobe/views.py`:

```python
	from django.http import JsonResponse
	from .models import Product

	def allProducts(request) :
		data = [
			(p.id, str(p))
			for p in Product.objects.all()
		]
		return JsonResponse(data, safe=False)
```

Per l'altre servei:

```python
	class View_Test(TestCase) :
		...

		def test_json_retailersForProduct(self) :

			p1 = Product(name="Product 1")
			p2 = Product(name="Product 2")
			r1 = RetailPoint(name="Retailer 1")
			for a in p1, p2, r1 : a.save()

			r1.sells(p1)

			request = self.factory.get("/booo")
			response = retailersForProduct(request, p1.id)

			self.assertJSONEqual(response.content.decode("utf-8"),
				json.dumps( [
					[1,"Retailer 1"],
				]))
```

Li passem a mà un paràmetre que s'obrindrà de la url.
I la implementació seria:


```python
	def retailersForProduct(request, productId) :
		product = Product.objects.get(id=productId)
		data = [
			(r.id, str(r) )
			for r in product.retailPoints()
		]
		return JsonResponse(data, safe=False)
```

## Relacionem els serveis amb les urls


Volem mapejar els serveis a les següents urls:

- `/json/allproducts`
- `/json/productretailers/<productid>`

Ho farem al fitcher `devsite/urls.py`

```python
	urlpatterns = patterns('',
		...

		url(r'^json/allproducts$', 'menjobe.views.allProducts'),
		url(r'^json/productretailers/([0-9]+)$', 'menjobe.views.retailersForProduct'),
	)
```

Comprovem que el server encara esta funcionant a l'altre terminal
i adrecem el navegador a <http://localhost:8001/json/allproducts>.
Veurem una llista buida, es clar, no hem afegit dades.

## Admin interface

Les dades les ficarem des de l'admin.

Per poder entrar, si es que no hem entrat abans cal crear una compte de superusuari:

```bash
	$ ./manage.py createsuperuser
```

Accedim a <http://localhost:8001/admin>.
Però només veiem les taules de `Auth`, `Groups` i `Users`.
Cal que fem acessibles les nostres taules a l'admin al fitxer `menjobe/admin.py`:

```python
from django.contrib import admin
from .models import Product
from .models import RetailPoint

admin.site.register(Product)
admin.site.register(RetailPoint)
```

I amb aixo ja podem afegir i editar la informació de productes i punts de servei
amb la interfície `admin`.
Es pot adaptar molt, però no entrarem a això ara.

Compte, per aixó, que un cop que tinguem dades, cal anar amb més cura amb les migracions.

De fet, convé tenir un parell de fixtures de dades que anem mantenint
per construir escenaris més o menys complexos.

## Fixtures

Un cop tenim un parell d'objectes farcits, si volem desar-los com a fixture
per recuperar-los si tornem a buidar la base de dades, cal fer:

```bash
	$ mkdir menjobe/fixtures/
	$ ./manage.py dumpdata --format=yaml menjobe > menjobe/fixtures/una.json
```

Per carregar les dades:

```bash
	$ ./manage.py loaddata --format=yaml  menjobe/fixtures/una.json
```

TODO: Com anar migrant les fixtures






