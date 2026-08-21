"""Domain generator, forLexOps problem statement."""

from .base import DocSpec, DomainSpec, EvalCase
from .lexops import LexOps

REGISTRY: dict[str, type[DomainSpec]] = {
       LexOps.key: LexOps
    }

__all__ = [
    "DocSpec",
    "DomainSpec",
    "EvalCase",
    "REGISTRY",
    "LexOps",    
]
