"""
Signal and opportunity detection.
"""

from gridportfolio.signals.cross_team import (
    build_signal_narrative,
    identify_team_roles,
)

from gridportfolio.signals.detector import (
    detect_cross_functional_signals,
)

from gridportfolio.signals.opportunities import (
    detect_procurement_opportunities,
)

__all__ = [
    "build_signal_narrative",
    "detect_cross_functional_signals",
    "detect_procurement_opportunities",
    "identify_team_roles",
]