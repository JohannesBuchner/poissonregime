=============
poissonregime
=============

Poisson error bars for low count statistics, detection significances.

.. image:: https://img.shields.io/pypi/v/poissonregime.svg
        :target: https://pypi.python.org/pypi/poissonregime

.. image:: https://api.travis-ci.com/JohannesBuchner/poissonregime.svg?branch=master&status=started
        :target: https://travis-ci.com/github/JohannesBuchner/poissonregime

.. image:: https://img.shields.io/badge/docs-published-ok.svg
        :target: https://johannesbuchner.github.io/poissonregime/
        :alt: Documentation Status

About
-----

Low count statistics is not that hard. It's just not Gaussian.

This package can answer the following questions:

* Given k detected objects, what are the uncertainties on the true number of objects? (`poissonregime.uncertainties_rate`)
* Given k "hits" out of a sample of n tries, what is the fraction and its uncertainty? (`poissonregime.uncertainties_fraction`)
* What is the significance of k detections, given that I expect B background events? (`poissonregime.significance`)
  * what if I measure the background events from counts in a "off" region?
  * what if I have additional systematic uncertainty?
* What is the probability distribution on the event rate, given a measured background rate? (`poissonregime.posterior`)

You can help by testing poissonregime and reporting issues. Code contributions are welcome.
See the `Contributing page <https://johannesbuchner.github.io/poissonregime/contributing.html>`_.

Usage
^^^^^

Read the full documentation at:

https://johannesbuchner.github.io/poissonregime/


Licence
^^^^^^^

MIT.


Other projects
^^^^^^^^^^^^^^

See also:

 * https://github.com/giacomov/gv_significance
 * https://github.com/mahnen/gamma_limits_sensitivity
