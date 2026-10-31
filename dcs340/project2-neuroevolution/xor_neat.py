"""
Evolve a neural network that solves XOR using NEAT (neat-python).

XOR is the classic test: output 1 when exactly one input is 1.
A network with no hidden neurons CANNOT solve it, so NEAT has to
grow at least one hidden neuron. Watch for that in the output.

Run:  python xor_neat.py
"""
import os
import pickle

import matplotlib
matplotlib.use("Agg")  # save plots to files instead of opening windows
import matplotlib.pyplot as plt
import neat

# The four XOR cases: (input1, input2) -> correct output
XOR_INPUTS = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
XOR_OUTPUTS = [0.0, 1.0, 1.0, 0.0]


def eval_genomes(genomes, config):
    """Give every genome a fitness score. NEAT calls this once per generation.

    Fitness starts at 4 (one point per XOR case) and loses the squared
    error on each case, so a perfect network scores 4.0.
    No gradients anywhere: evolution only ever sees this one number.
    """
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 4.0
        for xi, xo in zip(XOR_INPUTS, XOR_OUTPUTS):
            output = net.activate(xi)
            genome.fitness -= (output[0] - xo) ** 2


def plot_fitness(stats, path):
    """Save a line chart of best and average fitness per generation."""
    gens = range(len(stats.most_fit_genomes))
    best = [g.fitness for g in stats.most_fit_genomes]
    avg = stats.get_fitness_mean()
    plt.figure(figsize=(7, 4))
    plt.plot(gens, best, label="best")
    plt.plot(gens, avg, label="average")
    plt.xlabel("generation")
    plt.ylabel("fitness (4.0 = perfect)")
    plt.title("NEAT on XOR")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def run(config_path, generations=300, out_dir="results"):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))  # prints progress + species each generation
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(eval_genomes, generations)

    # Show what evolution found
    print("\nBest genome:\n", winner)
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    print("\nOutputs of the best network:")
    for xi, xo in zip(XOR_INPUTS, XOR_OUTPUTS):
        print(f"  input {xi}  expected {xo}  got {net.activate(xi)[0]:.3f}")

    hidden = [k for k in winner.nodes if k not in config.genome_config.output_keys]
    print(f"\nHidden neurons NEAT added: {len(hidden)}")

    os.makedirs(out_dir, exist_ok=True)
    plot_fitness(stats, os.path.join(out_dir, "xor_fitness.png"))
    with open(os.path.join(out_dir, "xor_winner.pkl"), "wb") as f:
        pickle.dump(winner, f)
    print(f"Saved fitness plot and winning genome to {out_dir}/")
    return winner


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    run(os.path.join(here, "config-xor.ini"), out_dir=os.path.join(here, "results"))
