# Cars
## Short description.

Simple REST application providing access to data about cars, and system for rating them.

## How to run?

### Starting
1. Rename **.env-default** file to **.env**.
2. Type command `docker-compose up --build` in terminal in project root directory.
3. Open browser with url `http://0.0.0.0:8000` or `http://127.0.0.1:8000` on Windows.
4. Enjoy!

## Tests (coverage)
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
                <td>57</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="57 57">100%</td>
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
                <td>41</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="41 41">100%</td>
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