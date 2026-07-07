"""
Evolution Engine — Genetic optimisation of belief systems.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from .exceptions import PopulationExtinctError


@dataclass
class Gene:
    trait: str
    fitness: float
    mutation_rate: float
    generation: int
    lineage: List[str] = field(default_factory=list)
    
    @property
    def id(self) -> str:
        data = f"{self.trait}_{self.generation}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


@dataclass
class Genome:
    genes: List[Gene]
    generation: int
    fitness_score: float = 0.0
    
    @property
    def id(self) -> str:
        data = "".join(g.id for g in self.genes)
        return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]
        
    def mutate(self, rate: float) -> None:
        for gene in self.genes:
            if random.random() < rate:
                gene.mutation_rate = min(1.0, gene.mutation_rate * random.uniform(0.5, 1.5))

    def crossover(self, other: Genome) -> Genome:
        new_genes = []
        for g1, g2 in zip(self.genes, other.genes):
            chosen = g1 if random.random() < 0.5 else g2
            new_genes.append(Gene(
                trait=chosen.trait,
                fitness=0.0,
                mutation_rate=chosen.mutation_rate,
                generation=self.generation + 1,
                lineage=chosen.lineage + [self.id, other.id]
            ))
        return Genome(genes=new_genes, generation=self.generation + 1)


@dataclass
class GenerationStats:
    generation: int
    best_fitness: float
    avg_fitness: float
    diversity: float
    population_size: int


class EvolutionEngine:
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.01, crossover_rate: float = 0.7):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population: List[Genome] = []
        self.stats: List[GenerationStats] = []
        self.current_generation = 0

    def initialize_population(self, seed_traits: List[str]) -> List[Genome]:
        self.population = []
        for _ in range(self.population_size):
            genes = [Gene(trait=t, fitness=0.0, mutation_rate=self.mutation_rate, generation=0) for t in seed_traits]
            self.population.append(Genome(genes=genes, generation=0))
        return self.population

    def evaluate_population(self, fitness_fn: Callable[[Genome], float]) -> None:
        if not self.population:
            raise PopulationExtinctError("No population to evaluate")
            
        total_fitness = 0.0
        for genome in self.population:
            genome.fitness_score = fitness_fn(genome)
            total_fitness += genome.fitness_score
            
        self.population.sort(key=lambda g: g.fitness_score, reverse=True)
        
        # Diversity estimation (mocked as distinct genomes count / total)
        distinct = len(set(g.id for g in self.population))
        diversity = distinct / self.population_size
        
        self.stats.append(GenerationStats(
            generation=self.current_generation,
            best_fitness=self.population[0].fitness_score,
            avg_fitness=total_fitness / self.population_size,
            diversity=diversity,
            population_size=self.population_size
        ))

    def select_parents(self) -> List[Genome]:
        # Tournament selection
        parents = []
        for _ in range(self.population_size):
            tournament = random.sample(self.population, min(3, len(self.population)))
            winner = max(tournament, key=lambda g: g.fitness_score)
            parents.append(winner)
        return parents

    def evolve_generation(self) -> List[Genome]:
        parents = self.select_parents()
        next_gen = []
        
        # Elitism: keep best
        next_gen.append(self.population[0])
        
        for i in range(1, self.population_size):
            p1 = parents[i]
            p2 = parents[(i + 1) % self.population_size]
            
            if random.random() < self.crossover_rate:
                child = p1.crossover(p2)
            else:
                child = Genome(genes=[Gene(g.trait, 0.0, g.mutation_rate, g.generation+1, g.lineage) for g in p1.genes], generation=self.current_generation + 1)
                
            child.mutate(self.mutation_rate)
            next_gen.append(child)
            
        self.population = next_gen
        self.current_generation += 1
        return self.population

    def summary(self) -> str:
        if not self.stats:
            return "EvolutionEngine(Not initialized)"
        best = self.stats[-1].best_fitness
        return f"EvolutionEngine(Gen={self.current_generation}, BestFitness={best:.4f})"
