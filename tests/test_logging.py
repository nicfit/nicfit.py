import pytest
import logging
from nicfit._logging import *
from nicfit import _logging


def test_log():
    # No handlers by default
    mylog = getLogger("test")
    assert isinstance(mylog, _logging.Logger)
    assert mylog.name == "test"
    assert len(mylog.handlers) == 0


    pkglog = getLogger("nicfit")
    assert isinstance(mylog, _logging.Logger)
    assert pkglog.name == "nicfit"

    for logger in [mylog, pkglog]:
        #assert(logger.getEffectiveLevel() == logging.NOTSET)
        assert(logger.propagate)
        assert(isinstance(logger, _logging.Logger))

    return
    for ll in [logging.NOTSET] + LEVELS:
        simpleConfig(ll)
        assert(pkglog.getEffectiveLevel() == ll)
        assert(len(pkglog.handlers) == 1)
        assert(isinstance(pkglog.handlers[0], logging.StreamHandler))
        assert(pkglog.handlers[0].formatter._fmt == LOG_FORMAT)

    assert("DEFAULT_LOGGING_CONFIG" in dir(log))

    with patch.object(pkglog, "log") as mock_log:
        pkglog.verbose("Honey's Dead")
        mock_log.assert_called_with(logging.VERBOSE, "Honey's Dead")
