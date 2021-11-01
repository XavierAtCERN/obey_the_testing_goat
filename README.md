# Obey the Testing Goat

Follows the [Test-Driven Development with Python: Obey the Testing Goat book](https://www.amazon.fr/Test-Driven-Development-Python-Selenium-JavaScript/dp/1491958707/) in order to move to better practices in the context of the Django based [ML Playground project](https://github.com/XavierAtCERN/MLplayground).

## Setting up

Setting up using conda rather than virtualenv.

```
conda create -n superlists
conda activate superlists
conda install pip
pip install "django<1.12" "selenium<4"

# installing geckodriver and moving it into /bin of the conda environment
```

At this stage, we should be good to go. Initial function_tests.my run fails as expected, but works after:
```
django-admin.py startproject superlists
python manage.py runserver
```
(runserver running in a parallel console)

Time for first commit as per the book instructions.



