package org.philosophers;

import org.philosophers.model.PhilosopherV6;
import org.philosophers.simulation.*;

public class Main {
    static void main() {
        /* Example usage */
        Simulation<PhilosopherV6> simulation = new Simulation<>(15, PhilosopherV6.class);
        simulation.simulate();
    }
}
