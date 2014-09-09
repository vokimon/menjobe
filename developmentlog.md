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
- Una persona anònima vol saber l'origen (productor/explotació) de les patates _de pagés_ que es venen a la fruiteria del costat de casa seva
- Una persona anònima vol saber si les patates que està venent la cooperativa agrària són d'agricultura ecològica, integrada o industrial
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

### Sistema de testos

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

### Restriccions

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



### Punts de distribució

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

### Productes als punts de distribució

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

### Convertint una relació 1:N en N:N

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

#### Duplicar

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


#### Farcir

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

#### Recolzar-se

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

#### Netejar

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

#### Activem el test

Després d'haver fet tot el refactor,
ho tenim preparat per passar el test molt ràpid.
L'activem, comprovem que encara falla i el passem només treient la linia del clear.

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

És interessant veure que el mateix procediment que ens permet
fer el refactor, sense trencar en cap moment el codi,
és el mateix procés que ens permet fer una migració exitosa
d'una base de dades en producció.


### Interficie d'administració

És interessant poder tenir dades per treballar.
Per introduir les dades del sistema farem servir la interficie `admin`.

Per poder entrar-hi, si es que no hem entrat abans cal crear una compte de superusuari:

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
Es pot personalitzar molt, però, la visió per defecte és suficient de moment.
Encara no hem entregat res.

### Adaptem l'admin per a mobils

La interficie `admin` està prou bé però no està gens adaptada a interfícies mòbils.

Hi ha una aplicació django que canvia la interfície per fer servir
el framework bootstrap de Twitter.

```bash
	$ pip install django-admin-bootstrapped
```

I afegim les applicacions al `devsite/settings.py`.
Les hem d'afegir al inici, fins ara ho feiem al final.

```python
	 INSTALLED_APPS = (
		 'django_admin_bootstrapped.bootstrap3',
		 'django_admin_bootstrapped',
		 'django.contrib.admin',
		 'django.contrib.auth',
		 ...
		 'menjobe',
		 )

```

Magicament l'admin ha canviat i funciona igual de bé a escritori com a mòbils.

### Fixtures

Un cop que tinguem dades, cal anar amb molta més cura quan fem les migracions.

De fet, convé tenir un parell de fixtures de dades que anem mantenint
per construir escenaris més o menys complexos per fer testos interactius.

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

### Vinculem URL's als serveis


Volem mapejar els serveis a les següents urls:

- `/json/allproducts`
- `/json/productretailers/<productid>`

Per a les urls de la nostra aplicació crearem un fitxer `urls.py` propi.
Primer farem una redirecció a `devsite/urls.py`:

```python
	from django.conf.urls import patterns, include, url
	from django.contrib import admin

	urlpatterns = patterns('',
		url(r'^admin/', include(admin.site.urls)),
		url('^', include('menjobe.urls', namespace='menjobe')), # <-- Changed
	)
```

I ara creem el fitxer `menjobe/urls.py`:

```python
	from django.conf.urls import patterns, include, url
	urlpatterns = patterns('',
		url(r'^json/allproducts$',               'menjobe.views.allProducts'),
		url(r'^json/productretailers/([0-9]+)$', 'menjobe.views.retailersForProduct'),
	)
```

Comprovem que el server encara esta funcionant a l'altre terminal
i adrecem el navegador a <http://localhost:8001/json/allproducts>.
Veurem una llista buida, es clar, no hem afegit dades.


### Web mockup

Ara farem un mockup de la web que farà servir aquests serveis web.
Serà lletja, els dissenyaires estan treballant en un disseny.

Concentrem-nos de moment en la funcionalitat.
Crearem una pagina amb un desplegable que carregarem amb els productes disponibles.
Quan canvii el valor del desplegable, cridarem a l'altre servei
i amb el resultat farcirem una llista de punts de distribució.

Primer afegirem una entrada en a les urls de `menjobe/urls.py`

```python
	from django.views.generic.base import TemplateView

	urlpatterns = patterns('',
		...
		url(r'^productsearch$',
			TemplateView.as_view(
				template_name='menjobe/productsearch.html')),
	)
```

Creem un nou directori per posar el template:

```bash
	$ mkdir -p menjobe/templates/menjobe/
```

Django recopila tots els directoris de les applicacions.
per aixo es convenient fer servir un subdirectori amb el nom de la nostra,
per evitar col·lisions.

Ara fem el template per a la nostra pàgina.
De template no tendrà gaire perquè ens basem en serveis AJAX
i la part dinàmica serà en JavaScript en el client.
L'avantatge d'aquesta forma de funcionar és que la interacció
serà més suau, evitant les càrregues de pàgina.

`menjobe/templates/menjobe/productsearch.html`.

```html
	{% load staticfiles %}
	<!doctype html>
	<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en"> <![endif]-->
	<!--[if IE 7]> <html class="no-js ie7 oldie" lang="en"> <![endif]-->
	<!--[if IE 8]> <html class="no-js ie8 oldie" lang="en"> <![endif]-->
	<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<title>Menjo Bé: Cerca per producte</title>
		<meta name="description" content="">
		<meta name="author" content="GuifiBaix SCCL">
		<meta name="viewport" content="width=device-width,initial-scale=1">
		<script src='//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'></script>
		<script src='{% static 'menjobe/js/productsearch.js' %}'></script>
	</head>
	<body>

	<select id='productSelect'>
	</select>
	<ul id='retailersList'>
	</ul>

	</body>
	</html>
```

Aquest és el nostre esquelet si l'executem, no és gaire espectacular.
Cal afegir el codi JavaScript per a omplir
primer el desplegable amb la llista de productes,
i, quan canvii el desplegable, els items de la llista amb els distribuidors.

Creem el directori per tenir fitxers estatics:

```bash
	$ mkdir -p menjobe/static/menjobe/{css,js,images}
```

I editem a `menjobe/static/menjobe/js/productsearch.js`:

```javascript
	$(function () {
		$.ajax({
			type: 'GET',
			datatype: 'json',
			url: '/json/allproducts',
			success: function(data) {
				var html = []
				var firstItemText = (data.length==0)?
					"No hi ha productes disponibles" :
					"Escull un producte";
				html.push(
					'<option disabled selected>'+firstItemText+'</option>\n');
				for (var i=0; i<data.length; i++) {
					var row=data[i];
					html.push(
						'<option value='+row[0]+'>'+row[1]+'</option>\n');
				}
				$('#productSelect').html(html.join(''));
			},
		});
		$('#productSelect').change(function (ev) {
			var productId = $(this).val();
			$.ajax({
				type: 'GET',
				datatype: 'json',
				url: '/json/productretailers/'+productId,
				success: function(data) {
					console.log(data);
					html=[]
					if (data.length==0)
						html.push(
							"<li>"+"No hi ha punts de venda pel producte"+'</li>');
					for (var i=0; i<data.length; i++) {
						var row=data[i];
						html.push(
							"<li>"+row[1]+"</li>\n");
						}
				$('#retailersList').html(html.join(''));
				},
			});
		})
	});
```

### Els serveis retornen diccionaris

Tot i que les dades json en array són més compactes que en diccionari,
quan referim a `row[1]` potser de moment sabem que ens referim al nom.
Pero en un futur, quan comencem a afegir més informació, això té pinta de no ser gaire mantenible.
Cal canviar els serveis per fer servir diccionaris, objectes en vocabulari javascript.

- Canviem els testos de les vistes perque esperin diccionaris (amb claus 'id' i 'name') i els fallem.
- Canviem les vistes perque realment generin els diccionaris
- Adaptem el javascript per que faci servir els atributs.


### Plantilla Bootstrap

I amb això tenim la funcionalitat que voliem.
Tot i que no és gaire maco.

Els dissenyaires s'han currat una maqueta per la pàgina principal fent servir bootstrap.
Bé, de fet he estat jo amb un barret de disenyaire, per això el resultat és modestet.

El disseny depén d'un seguit de recursos externs: imatges, javascripts i estils.
Ja vam crear els directoris corresponents (`images`, `js` i `css`) a `menjobe/static/menjobe/`.
Hi copiarem els recursos.

I per a que la maqueta es pugui carregar com a template localitzant aquest recursos
caldrà afegir, com vam fer amb l'altre template.
Primer, a dalt de tot, la directiva:

```html
	{% load staticfiles %}
```

I cal substituir les ocurrències de les imatges per:

```html
	{% static 'menjobe/images/pagesia.png' %}
```

Eliminant de l'encaminament `menjobe/static/`.

Comprovem esquena amb esquena que el que ens han enviat pinta i interactua igual i seguim.

TODO: Que ve que seria tenir un test aqui, oi?


### Integrem la cerca a la plantilla

Ara, unifiquem el prototip que teniem, `menjobe/templates/menjobe/productsearch.html`,
amb el format de la nova pagina d'inici, `menjobe/templates/menjobe/home.html`.
Per això jo recomano un editor de diferències.
Jo faig servir el `vimdif`, pero requereix estar habituat al `vim`.

És important anar passant coses poc a poc i comprovar que la plantilla funcional funciona.

TODO: aquí ens hauria anat molt bé tenir testos amb selenium, oi?

Un cop tenim a cada costat només les diferències que han d'haver-hi,
definim al `home.html` blocs amb nom per les parts que canvien.

En concret:

- Tot el que va a sota del menu fins a peu de pàgina serà el block `content`
- Farem un bloc buit `extraheadercss` al final dels css de la capcelera
- Farem un bloc buit `extraheaderjs` al dinal dels js de la capcelera

Podríem extreure una base comuna a partir d'aquí, però, de moment, no cal.
Esforç mínim, derivarem directament de `home.html`.

Un cop definits els blocs divergents, podem reescriure `productsearch.html`
només amb la part variable:

```html
	{% extends "menjobe/home.html" %}
	{% load staticfiles %}

	{% block extraheaderjs %}
		<script src='{% static 'menjobe/js/productsearch.js' %}'></script>
	{% endblock extraheaderjs %}

	{% block content %}
		<select id='productSelect'>
		</select>
		<ul id='retailersList'>
		</ul>
	{% endblock content %}
```

### Cerca amb components de Bootstrap

TODO: Migracio a bootstrap + bootstrap-select2


## Desplegament

### Creating the subdomain

I decided to deploy the application on DreamHost.
Dreamhost support for Django is quite limited,
in the sense that it is not as nice than the support other platforms.
Instead of using `mod_wsgi` or a similar wsgi implementation
it uses Passenger, Ruby on Rails, launcher.

You have to activate Passenger in your subdomain/domain.
But be careful! if you activate it in an existing one you will lose your data.

I created a subdomain for the aplication,
say `http://menjobe.canvoki.net` from my domain `canvoki.net`.
This implies that DreamHost will create a `~/menjobe.canvoki.net` folder.
Within that folder you will find a `public` subdir, with a dummy website.

That `public` subdir will be your website root.
Any URL matching a file will be served as raw files.
If no file inside `public` matches the URL, Passenger will be triggered.
All the python code goes then at the upper level.


### Cloning our app

We will clone our app on the subdomain directory.
I cloned it without a subdirectoy with the repository name.

```bash
	$ git clone https://github.com/vokimon/menjobe.git ~/menjobe.canvoki.net/
```

You might need to temporary move `public` and any other content outside to make the clone,
and then move them back.


### Installing Python3


There is no Python 3 in DreamHost so you must to compile it from sources.

We are downloading and uncompressing all the sources appart at `~/sources`.

```bash
	$ mkdir ~/sources
	$ cd ~/sources
	$ wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tgz --no-check-certificate
	$ md5sum Python-3.4.1.tgz
	$ tar xvfz Python-3.4.1.tgz
	$ cd Python-3.4.1
	$ ./configure --prefix=$HOME/local
	$ make
	$ make install
```

Note: for some reason wget at dreamhost does no play well with certificates,
so that's why we ignore the certificate, and we later check the md5sum and compare it
with the one at the website.


### Setting up the virtual environment

Dreamhost installed virtualenv does not work with Python3. Lets install it.

```bash
	$ cd ~/sources
	$ wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.6.tar.gz --no-check-certificat
	$ md5sum virtualenv-1.11.6.tar.gz
	$ tar xvfz virtualenv-1.11.6.tar.gz
	$ cd virtualenv-1.11.6
	$ ~/local/bin/python3 setup.py install
```

Now we can set the virtual environment:

```bash
	$ cd ~/menjobe.canvoki.net/
	$ ~/local/bin/virtualenv --no-site-packages env
```

From now on all the commands are launched from `~/menjobe.canvoki.net/` and inside the environment.
Let's install the dependencies:

```bash
	$ pip install git+git://github.com/django/django.git@stable/1.7
	$ pip install django-admin-bootstrapped
	$ pip install pyyaml
```

My version of `django-admin-bootstrapped`, downgrades django to 1.6 (no migrations).
I reinstall the django 1.7 and all works perfectly.

### Setting up the application

At the end of the `devsite/settings.py` file add:

```python
	STATIC_ROOT = os.path.join(BASE_DIR,'public/static/')
```

Then we collects all the static files and put them under `public/static/`.

```bash
	$ ./manage.py collectstatic
```

You have to run the previous command every time the static files change.

Then you have to create the database.

```bash
	$ ./manage.py migrate
```

And, just the first time, to create the superuser:

```bash
	$ ./manage.py createsuperuser
```


And last but not least, you have to tell Passenger there is a lot to run here.
Create a file named `passenger_wsgi.py`, with the followin content:

```python
	import sys, os

	project = 'devsite'
	python = 'python3.4'
	hexversion = 0x3040000

	cwd = os.path.dirname(os.path.abspath(__file__))

	sys.path.append(cwd)

	#Switch to new python
	if sys.hexversion < hexversion : os.execl(cwd+"/env/bin/"+ python, python, *sys.argv)

	sys.path.insert(0,cwd+'/env/lib/'+python+'/site-packages')

	os.environ['DJANGO_SETTINGS_MODULE'] = project+".settings"

	from django.core.wsgi import get_wsgi_application
	application = get_wsgi_application()
```

And we add execution permissions:

```bash
	$ chmod a+x passenger_wsgi.py
```


WARNING: The equivalent script provided by DreamHost gave me lot of headaches.
It included too many directories on `sys.path`, included `django` package and
you project folder. Having that many directories in path creates
collisions which namespaces should have avoided.


- Having problems at this stage can be tricky as the errors are not shown on any log you can access.
- Using an wsgi error middleware won't help if the results are set as response content. Try to catch any error that comes from `start_response` and write the backtrace into an error file.
- To reload the scripts on the server, run `touch ~/menjobe.canvoki.net/tmp/restart.txt` (change your domain).



## Segona iteracio: Afegim més informació i edició integrada

### Rebent reaccions dels usuaris

Després de posar l'aplicació a disposició d'alguns usuaris per que la provin amb algunes dades de prova,
no és sorpresa que els usuaris ens indiquin que la següent cosa a afegir hauria de ser:

- més informació sobre els distribuidors (on trobar-ho)
- informació d'origen i tipus de cultiu dels productes
- poder afegir informació nova

### Afegint un nou camp de descripció

Decidim començar pel camp de descripció.
Ara ja tenim dades que migrar, és important que les mantinguem consistents.

En el cas d'afegir un camp nou, la clau de la migració de dades és decidir
quin valor pendran pel camp els objectes que ja existeixen.
En aquest cas és fàcil perquè tots poden inicialitzar-se,
d'entrada, amb una descripció en blanc.

Volem un test que falli:

```python
	class RetailPoint_Test :
		...
		def test_description_defaultTrue(self) :
			r = RetailPoint(name="A retailer")
			self.assertMultiLineEqual(r.description(), "")
```

Fem servir `assertMultiLineEqual`
perquè pels textos llargs és molt més informatiu.

Per fer-ho fallar afegim la següent linia al model entre el `name`i `retailedProduct`:

```python
	class RetailPoint(models.Model) :
		...
		description = models.TextField(default="bad string")
```

```bash
	$ ./manage makemigration
	Migrations for 'menjobe':
	  0009_retailpoint_description.py:
	    - Add field description to retailpoint

```

Això ens falla el test que és el que volem.





-------------------------------------------------

# Enllaços guardats

- http://www.virtuosoft.eu/code/bootstrap-duallistbox/ -- Selecció múltiple passant d'una llista a l'altre
- http://thegoods.aj7may.com/django-bootstrap-markdown/ -- Editar text amb markdown amb vista previa
- http://goratchet.com/ -- Componentes para mobil tipo bootstrap, mismos autores, similar sintaxi
- http://wiki.dreamhost.com/Django -- Notes de com configurar Django amb dreamhost
- https://github.com/etianen/django-reversion --- Control de versiones para los cambios
- http://pythonhosted.org/django-markdown/ --- Markdown fields
- http://blog.grapii.com/2010/08/how-to-build-a-simple-search-filter-with-jquery/ --- jquery based div filter

-------------------------------------------------



