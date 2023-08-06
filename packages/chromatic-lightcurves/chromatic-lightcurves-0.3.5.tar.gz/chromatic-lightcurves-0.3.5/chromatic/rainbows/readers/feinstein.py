"""
This module serves as a template for creating a new Rainbow
reader. If you want to add the ability to read chromatic
light curves from a new kind of file format, a good process
would be to do something like the following

    1. Copy this `template.py` file into a new file in the
    `readers/` directory, ideally with a name that's easy
    to recognize, such as `readers/feinstein.py` (assuming
    `feinstein` is the name of your format)

    2. Start by finding and replacing `feinstein` in this
    template with the name of your format.

    3. Edit the `from_feinstein` function so that it will
    load a chromatic light curve file in your format and,
    for some Rainbow object `rainbow`, populate at least:

        + rainbow.timelike['time']
        + rainbow.wavelike['wavelength']
        + rainbow.fluxlike['flux']

    You'll need to replace the cartoon functions on each
    line with the actual code needed to load your file.

    (This template assumes that only one file needs to be
    loaded. If you need to load multiple segments, or each
    time point is stored in its own file or something, then
    check out `stsci.py` for an example of loading and
    stitching together multiple input files. You'll probably
    want to change `filepath` to accept a glob-friendly string
    like `my-neato-formatted-files-*.npy` or some such.)

    4. Edit the `readers/__init__.py` file to import your
    `from_feinstein` function to be accessible when people
    are trying to create new Rainbows. Add an `elif` statement
    to the `guess_reader` function that will help guess which
    reader to use from some aspect(s) of the filename.

    (This `guess_reader` function also accepts a `format=`
    keyword that allows the user to explicitly specify that
    the feinstein reader should be used.)

    5. Submit a pull request to the github repository for
    this package, so that other folks can use your handy
    new reader too!
"""

# import the general list of packages
from ...imports import *

# define list of the only things that will show up in imports
__all__ = ["from_feinstein"]


def from_feinstein(rainbow, filepath):
    """
    Populate a Rainbow from a file in the feinstein format.

    Parameters
    ----------

    rainbow : Rainbow
        The object to be populated. This function is meant
        to be called during the initialization of a Rainbow
        object. You can/should assume that the `rainbow` object
        being passed will already contain the four core
        dictionaries `timelike`, `wavelike`, `fluxlike`, and
        `metadata`. This function should, at a minimum, add
        the following items
            + `rainbow.timelike['time']`
            + `rainbow.wavelike['wavelength']`
            + `rainbow.fluxlike['flux']`
        and optionally, additional entries like
            + `rainbow.metadata['some-useful-parameter']`
            + `rainbow.fluxlike['uncertainty']`
            + `rainbow.fluxlike['ok']`

    filepath : str
        The path to the file to load.
    """

    wavelength, spectra, err, time = np.load(filepath, allow_pickle=True)

    rainbow.wavelike["wavelength"] = wavelength * u.micron * 1

    # populate a 1D array of times (with astropy units of time)
    times = time * u.day
    rainbow.timelike["time"] = times * 1

    # populate a 2D (row = wavelength, col = array of fluxes
    flux = np.zeros((len(wavelength), len(times)))
    uncertainty = np.zeros_like(flux)

    rainbow.fluxlike["flux"] = spectra.T * 1
    rainbow.fluxlike["uncertainty"] = err.T * 1
