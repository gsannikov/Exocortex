"""
Backward-compatible CLI entrypoint that delegates to services.index_service.
"""

from .services.index_service import *  # noqa: F401,F403

if __name__ == "__main__":  # pragma: no cover
    from .services.index_service import main

    raise SystemExit(main())
