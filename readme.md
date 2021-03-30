# Cars
## Short description.

Simple REST application providing access to data about cars, and system for rating them.

## How to run?

### Prerequisites
1. You have to have installed [docker](https://www.docker.com/)
   and [docker-compose](https://docs.docker.com/compose/install/) on your computer.

### Starting
1. Rename **.env-default** file to **.env**.
2. Type command `docker-compose up --build` in terminal in project root directory.
3. Open browser with url `http://0.0.0.0:8000` or `http://127.0.0.1:8000` on Windows.
4. Enjoy!

### Endpoints
1. `https://capirs.herokuapp.com/cars/` GET and POST cars.
2. https://capirs.herokuapp.com/cars/<pk> DELETE a car.
3. https://capirs.herokuapp.com/popular/ GET information about cars popularity.
4. https://capirs.herokuapp.com/rate/ POST raring for the car.

## API description.
You can check documentation for API [here](https://capirs.herokuapp.com/swagger/).
## Tests (coverage)

### Run tests and coverage.
1. Start application.
2. To run tests, type command `docker-compose exec backend coverage run manage.py test` in terminal in project root directory.
3. To run coverage, type command `docker-compose exec backend python manage.py test` in terminal in project root directory.
4. To view coverage report in command line, type command `docker-compose exec backend coverage report` in terminal in project root directory.
<dl>
    <table class="index">
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th class="name left headerSortDown shortkey_n">Module</th>
                <th class="shortkey_s">statements</th>
                <th class="shortkey_m">missing</th>
                <th class="shortkey_x">excluded</th>
                <th class="right shortkey_c">coverage</th>
            </tr>
        </thead>
        <tfoot>
            <tr class="total">
                <td class="name left">Total</td>
                <td>77</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="77 77">100%</td>
            </tr>
        </tfoot>
        <tbody>
            <tr class="file">
                <td class="name left"><a href="cars_models_py.html">cars/models.py</a></td>
                <td>16</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="16 16">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="cars_serializers_py.html">cars/serializers.py</a></td>
                <td>39</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="39 39">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="cars_urls_py.html">cars/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="cars_views_py.html">cars/views.py</a></td>
                <td>18</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="18 18">100%</td>
            </tr>
        </tbody>
    </table>
</dl>

## Licence
```text
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <phk@FreeBSD.ORG> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.  Poul-Henning Kamp
 * ----------------------------------------------------------------------------
 ```