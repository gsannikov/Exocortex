"""
Backward-compatible CLI entrypoint that delegates to services.search_service.
"""

from .services.search_service import *  # noqa: F401,F403

if __name__ == "__main__":  # pragma: no cover
    from .services.search_service import main

    raise SystemExit(main())
