"""An optional smoke test for the CNA engine-layer extension.

Deliberately small, deliberately separate, and deliberately device-free. The
starter's own 60- and 600-frame runs must not need the engine layer at all: it
is a CNA-only rendering vocabulary, and a game drawing sprites never touches it.
Making basic startup depend on it would be a claim that it does.

What this proves, in well under a second and with no renderer, is that
`cna.extensions.engine` is importable, that this CNA build's engine layer is
present and reports the revision the binding was written against, that a value
type reads its defaults from CNA rather than from a transcription, and that a
pure shading function answers what the physics says it should. Four assertions,
each exact.

**A build with no engine layer is a result, not a failure.** CNA can be
configured without one, and every route then reports itself unavailable rather
than answering with a plausible number. This says so and exits cleanly, because
"the extension is absent" and "the extension is broken" are different facts and
a smoke test that conflated them would be worse than none.
"""

from __future__ import annotations

import argparse

from Microsoft.Xna.Framework import Vector3
from cna.extensions import engine


def verify() -> str:
    """Checks the engine layer without a device, and returns a one-line result."""
    if not engine.is_available():
        return ("ENGINE_VERIFICATION=absent this CNA build has no engine layer, "
                "which is a supported configuration")

    revision = engine.layer_version()
    if revision != engine.HEADER_LAYER_VERSION:
        raise RuntimeError(
            f"this CNA build reports engine layer {revision}; the binding was "
            f"written against {engine.HEADER_LAYER_VERSION}")
    if str(revision) not in engine.layer_version_string():
        raise RuntimeError(
            f"the engine layer's own version string {engine.layer_version_string()!r} "
            f"does not mention revision {revision}")

    # A value type, read from CNA rather than transcribed. A default a binding
    # wrote down would survive CNA changing its mind, which is the whole reason
    # these are read.
    light = engine.ClusteredLight.default()
    if not light.range_ > 0.0:
        raise RuntimeError(f"a default clustered light has range {light.range_}")
    if not light.is_usable:
        raise RuntimeError("CNA's own default clustered light is not usable")

    # A pure shading function, against the physics rather than against itself.
    # Beer-Lambert: a medium that leaves half the light in one attenuation
    # distance leaves a quarter in two.
    attenuation = engine.volume_attenuation(Vector3(0.5, 0.5, 0.5), 1.0, 2.0)
    if abs(attenuation.X - 0.25) > 1e-5:
        raise RuntimeError(
            f"two attenuation distances of a half-transmitting medium should leave "
            f"0.25, got {attenuation.X}")

    return (f"ENGINE_VERIFICATION=ok engine layer {revision}, "
            f"default light range {light.range_}, "
            f"two-thickness transmission {attenuation.X}")


def run() -> str:
    """Runs the check and prints its one-line result.

    Separate from :func:`main` so the starter can call it without a second
    argument parser seeing the starter's own flags.
    """
    line = verify()
    print(f"cna-python-template: {line}")
    return line


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check the CNA engine layer through cna.extensions.engine")
    parser.parse_args()
    run()


if __name__ == "__main__":
    main()
